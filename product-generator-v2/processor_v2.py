import os
import re
import json
import zipfile
import shutil
import logging
from typing import Dict, Any, List

import yaml
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

INBOX_DIR = os.path.join(SCRIPT_DIR, 'inbox')
FAILED_DIR = os.path.join(SCRIPT_DIR, 'failed')

PRODUCT_YAML_DIR = os.path.join(PROJECT_ROOT, 'src', '_data', 'products')
PRODUCTS_CATALOG_FILE = os.path.join(PROJECT_ROOT, 'src', '_data', 'products.yml')
ASSETS_PRODUCT_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images', 'product')


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


def slugify(text: str) -> str:
    if not text:
        return ''
    text = text.strip().lower()
    # replace non-alphanumeric with hyphen
    text = re.sub(r"[^a-z0-9]+", '-', text)
    text = re.sub(r"-+", '-', text)
    return text.strip('-')


def _llm_parse_prompt(markdown: str, product_slug: str) -> str:
    schema = {
        "en": {
            "name": "string",
            "category": "one of: powerbank | loopenergy | gan_charger | flash_disk",
            "description": "string",
            "images": ["filenames only, e.g. photo-1.jpg"],
            "features": ["string"],
            "specs": [{"name": "string", "value": "string"}],
            "detailed_features": {
                "title": "string",
                "subtitle": "string",
                "items": [{
                    "title": "string",
                    "description": "string",
                    "benefits": ["string"],
                    "image": "filename only",
                    "image_alt": "string"
                }]
            },
            "compatibility": {
                "title": "string",
                "subtitle": "string",
                "categories": [{"name": "string", "details": "string"}]
            },
            "package_contents": {
                "title": "string",
                "subtitle": "string",
                "items": [{"name": "string", "details": "string"}]
            }
        }
    }
    instructions = f"""
You are a precise information extraction system. Parse the Markdown into the JSON schema below.

CRITICAL RULES:
1) Return a SINGLE valid JSON object. No prose.
2) Only include keys that are present in the Markdown. Omit missing keys entirely (no null/empty strings).
3) For all image fields, return FILENAMES only (e.g., "main.jpg"). Do NOT include any folder paths or URLs. We'll prefix paths in code.
4) The output MUST include the English block at root key "en". Do not add other languages.
5) If you can infer a product category, map it to one of: powerbank | loopenergy | gan_charger | flash_disk. If unclear, pick the closest.
6) The root object MUST also include a top-level field "slug" with value: {product_slug}

JSON Schema example (values are types not examples):
{json.dumps(schema, indent=2)}

Markdown to parse:
---
{markdown}
---
"""
    return instructions


def _llm_translate_prompt(en_json: Dict[str, Any]) -> str:
    return (
        "Translate values from English to German. Return ONLY a JSON object with the same structure under key 'de'. "
        "Do not translate technical model numbers or images."
        "\nInput (only the 'en' section is provided):\n" + json.dumps(en_json.get('en', {}), ensure_ascii=False)
    )


def call_llm_json(prompt: str, model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def ensure_dirs():
    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)
    os.makedirs(PRODUCT_YAML_DIR, exist_ok=True)
    os.makedirs(ASSETS_PRODUCT_DIR, exist_ok=True)


def _prefix_images(slug: str, filenames: List[str]) -> List[str]:
    out = []
    for f in filenames or []:
        f = f.strip().lstrip('/')
        out.append(f"assets/images/product/{slug}/{f}")
    return out


def _map_to_yaml(en_block: Dict[str, Any], de_block: Dict[str, Any], slug: str) -> Dict[str, Any]:
    def map_one(block: Dict[str, Any]) -> Dict[str, Any]:
        if not block:
            return {}
        mapped: Dict[str, Any] = {}
        mapped['name'] = block.get('name')
        mapped['category'] = block.get('category')
        mapped['description'] = block.get('description')
        # images
        mapped['images'] = _prefix_images(slug, block.get('images', []))
        # simple features/specs
        if block.get('features'):
            mapped['features'] = block['features']
        if block.get('specs'):
            mapped['specs'] = block['specs']
        # detailed features
        if block.get('detailed_features'):
            df = block['detailed_features']
            mapped_df = {
                'title': df.get('title'),
                'subtitle': df.get('subtitle'),
                'items': []
            }
            for it in df.get('items', []) or []:
                mapped_df['items'].append({
                    'title': it.get('title'),
                    'description': it.get('description'),
                    'benefits': it.get('benefits'),
                    'image': f"assets/images/product/{slug}/{it.get('image')}" if it.get('image') else None,
                    'image_alt': it.get('image_alt')
                })
            mapped['detailed_features'] = mapped_df
        # compatibility
        if block.get('compatibility'):
            mapped['compatibility'] = block['compatibility']
        # package contents
        if block.get('package_contents'):
            mapped['package_contents'] = block['package_contents']
        return mapped

    return {
        'en': map_one(en_block),
        'de': map_one(de_block)
    }


def _load_yaml(path: str) -> Any:
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _save_yaml(path: str, data: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, Dumper=NoAliasDumper, allow_unicode=True, sort_keys=False)


def _append_to_catalog(slug: str, en_name: str, de_name: str, category: str, image_rel: str):
    # normalize category to our keys
    cat_map = {
        'powerbank': 'powerbank',
        'loopenergy': 'loopenergy',
        'gan_charger': 'gan_charger',
        'gan charger': 'gan_charger',
        'gan': 'gan_charger',
        'flash_disk': 'flash_disk',
        'flash disk': 'flash_disk',
        'memory': 'flash_disk',
    }
    key = cat_map.get((category or '').strip().lower(), 'gan_charger')

    catalog = _load_yaml(PRODUCTS_CATALOG_FILE) or {}
    # Ensure base structure
    for lang in ['en', 'de']:
        catalog.setdefault(lang, {})
        catalog[lang].setdefault('categories', {})
    # Our products.yml structure uses nested groups under categories.<group>.products
    def ensure_group(lang_key: str, title_en: str, title_de: str):
        cats = catalog[lang_key].setdefault('categories', {})
        # ensure tabs array exists
        tabs = catalog[lang_key].setdefault('tabs', [
            {'id': 'powerbank', 'title': 'Powerbank Series' if lang_key == 'en' else 'Powerbank Serie'},
            {'id': 'loopenergy', 'title': 'Loopenergy Series' if lang_key == 'en' else 'Loopenergy Serie'},
            {'id': 'gan-charger', 'title': 'GaN Charger Series' if lang_key == 'en' else 'GaN Ladegerät Serie'},
            {'id': 'flash-disk', 'title': 'Memory Series' if lang_key == 'en' else 'Speicher Serie'},
        ])
        # map id
        group_key = key if key != 'gan_charger' else 'gan_charger'
        cats.setdefault(group_key, {}).setdefault('products', [])
    ensure_group('en', '', '')
    ensure_group('de', '', '')

    def append_item(lang_key: str, name: str):
        group_key = key
        products_list = catalog[lang_key]['categories'][group_key]['products']
        url = f"/{lang_key}/products/{slug}/"
        # de-dup by url
        products_list[:] = [p for p in products_list if p.get('url') != url]
        products_list.append({
            'name': name,
            'description': '',
            'details': '',
            'image': image_rel,
            'url': url,
        })

    append_item('en', en_name)
    append_item('de', de_name)
    _save_yaml(PRODUCTS_CATALOG_FILE, catalog)


def process_zip_v2(zip_path: str) -> str:
    ensure_dirs()
    slug = os.path.splitext(os.path.basename(zip_path))[0]
    tmp_dir = os.path.join(SCRIPT_DIR, 'tmp', slug)
    os.makedirs(os.path.dirname(tmp_dir), exist_ok=True)

    try:
        # 1) unzip
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmp_dir)

        md_path = os.path.join(tmp_dir, 'product.md')
        if not os.path.exists(md_path):
            raise FileNotFoundError('product.md not found inside zip.')
        with open(md_path, 'r', encoding='utf-8') as f:
            md = f.read()

        # 2) LLM parse (en)
        en_json = call_llm_json(_llm_parse_prompt(md, slug))
        en_json['slug'] = slug

        # 3) LLM translate (de)
        de_json_wrapped = call_llm_json(_llm_translate_prompt({'en': en_json.get('en', {})}))
        de_json = {'de': de_json_wrapped.get('de', {})}

        # 4) map to our YAML
        yaml_data = _map_to_yaml(en_json.get('en', {}), de_json.get('de', {}), slug)

        # ensure minimal required fields
        en_name = yaml_data['en'].get('name') or slug.replace('-', ' ').title()
        de_name = yaml_data['de'].get('name') or en_name
        category = yaml_data['en'].get('category', 'gan_charger')

        # 5) copy images
        src_images_dir = os.path.join(tmp_dir, 'images')
        dst_images_dir = os.path.join(ASSETS_PRODUCT_DIR, slug)
        if os.path.exists(dst_images_dir):
            shutil.rmtree(dst_images_dir)
        if os.path.exists(src_images_dir):
            shutil.copytree(src_images_dir, dst_images_dir)
        else:
            os.makedirs(dst_images_dir, exist_ok=True)

        # 6) save product yaml
        product_yaml_path = os.path.join(PRODUCT_YAML_DIR, f"{slug}.yml")
        _save_yaml(product_yaml_path, yaml_data)

        # 7) update products catalog yaml
        first_image = (yaml_data['en'].get('images') or [None])[0] or f"assets/images/product/{slug}/product-1.jpg"
        _append_to_catalog(slug, en_name, de_name, category, first_image)

        # 8) return URL for EN
        return f"/en/products/{slug}/"

    except Exception as e:
        logging.exception(f"V2 processing failed for {zip_path}: {e}")
        os.makedirs(FAILED_DIR, exist_ok=True)
        if os.path.exists(zip_path):
            shutil.move(zip_path, os.path.join(FAILED_DIR, os.path.basename(zip_path)))
        raise
    finally:
        # cleanup
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
        # remove zip if success
        if os.path.exists(zip_path) and not os.path.exists(os.path.join(FAILED_DIR, os.path.basename(zip_path))):
            os.remove(zip_path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process a product zip into 11ty YAML + assets (V2).')
    parser.add_argument('zip', help='Path to product zip')
    args = parser.parse_args()
    url = process_zip_v2(args.zip)
    print(url)


