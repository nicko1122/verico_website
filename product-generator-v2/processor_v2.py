import os
import re
import json
import zipfile
import shutil
import logging
from typing import Dict, Any, List

import yaml
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI()

SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

INBOX_DIR = os.path.join(SCRIPT_DIR, 'inbox')
FAILED_DIR = os.path.join(SCRIPT_DIR, 'failed')

PRODUCT_YAML_DIR = os.path.join(PROJECT_ROOT, 'src', '_data', 'products')
PRODUCTS_CATALOG_FILE = os.path.join(PROJECT_ROOT, 'src', '_data', 'products.yml')
ASSETS_PRODUCT_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images', 'product')
ASSETS_ICONS_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images', 'icons')
ASSETS_GLOBAL_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images', 'global')


class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


def slugify(text: str) -> str:
    if not text:
        return ''
    text = text.strip().lower()
    # remove dots between alphanumerics (e.g., m.2 -> m2)
    text = re.sub(r'(?<=[a-z0-9])\.(?=[a-z0-9])', '', text)
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
            "catalog_image": "filename only for product catalog card image (optional)",
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
            "hero_background": "filename or 'global/<file>' (optional)",
            "compatibility": {
                "title": "string",
                "subtitle": "string",
                "categories": [{"name": "string", "details": "string", "icon": "filename or 'icons/<file>' (optional)"}]
            },
            "package_contents": {
                "title": "string",
                "subtitle": "string",
                "items": [{"name": "string", "details": "string", "icon": "filename or 'icons/<file>' (optional)"}]
            },
            "variants": [{
                "title": "string",
                "package_image": "filename only",
                "model_name": "string",
                "sku": "string",
                "ean": "string"
            }]
        }
    }
    instructions = f"""
You are a precise information extraction system. Parse the Markdown into the JSON schema below.

CRITICAL RULES:
1) Return a SINGLE valid JSON object. No prose.
2) Only include keys that are present in the Markdown. Omit missing keys entirely (no null/empty strings).
3) For all image fields, return FILENAMES only (e.g., "main.jpg"). Do NOT include any folder paths or URLs. We'll prefix paths in code.
3a) EXCEPTIONS for special fields:\n    - icon fields: you MAY return "icons/<file>.svg" to reference a global shared icon directory\n    - hero_background: you MAY return "global/<file>" to reference a global shared image
4) The output MUST include the English block at root key "en". Do not add other languages.
5) If you can infer a product category, map it to one of: powerbank | loopenergy | gan_charger | flash_disk. If unclear, pick the closest.
6) The root object MUST also include a top-level field "slug" with value: {product_slug}
7) If a section "## Also Available In" exists, parse its subsections (e.g., "### 2 Pack") as array "variants" of objects with keys: title, package_image, model_name, sku, ean. The package image can be provided via an inline directive like: <!-- package_image: filename.jpg -->. Omit any keys not present.
8) If a line like "Catalog Image: filename.ext" exists near the top, include it as key "catalog_image" under the "en" object.

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
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    return json.loads(resp.choices[0].message.content)


def ensure_dirs():
    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(FAILED_DIR, exist_ok=True)
    os.makedirs(PRODUCT_YAML_DIR, exist_ok=True)
    os.makedirs(ASSETS_PRODUCT_DIR, exist_ok=True)
    os.makedirs(ASSETS_ICONS_DIR, exist_ok=True)
    os.makedirs(ASSETS_GLOBAL_DIR, exist_ok=True)


def _prefix_images(slug: str, filenames: List[str]) -> List[str]:
    out = []
    for f in filenames or []:
        f = f.strip().lstrip('/')
        out.append(f"assets/images/product/{slug}/{f}")
    return out


def _map_to_yaml(en_block: Dict[str, Any], de_block: Dict[str, Any], slug: str) -> Dict[str, Any]:
    def resolve_icon_path(slug_local: str, icon_value: Any) -> Any:
        if not icon_value or not isinstance(icon_value, str):
            return None
        raw = icon_value.strip().lstrip('/')
        # global shared icons: icons/<file>
        if raw.startswith('icons/'):
            # normalize to assets/images/icons/<file>
            return f"assets/images/icons/{raw.split('/', 1)[1]}"
        # backward compatibility: if contains a path like images/foo.svg, take the basename
        filename = raw.split('/')[-1]
        return f"assets/images/product/{slug_local}/{filename}"

    def resolve_global_or_product(slug_local: str, value: Any) -> Any:
        if not value or not isinstance(value, str):
            return None
        raw = value.strip().lstrip('/')
        if raw.startswith('global/'):
            return f"assets/images/global/{raw.split('/',1)[1]}"
        filename = raw.split('/')[-1]
        return f"assets/images/product/{slug_local}/{filename}"

    def map_one(block: Dict[str, Any]) -> Dict[str, Any]:
        if not block:
            return {}
        mapped: Dict[str, Any] = {}
        mapped['name'] = block.get('name')
        mapped['category'] = block.get('category')
        mapped['description'] = block.get('description')
        # catalog image (optional)
        if block.get('catalog_image'):
            mapped['catalog_image'] = f"assets/images/product/{slug}/{block.get('catalog_image')}"
        # hero background (optional, allow global/ or product-scoped)
        if block.get('hero_background'):
            mapped['hero_background'] = resolve_global_or_product(slug, block.get('hero_background'))
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
            comp = block['compatibility']
            mapped_comp = {
                'title': comp.get('title'),
                'subtitle': comp.get('subtitle'),
                'categories': []
            }
            for c in comp.get('categories', []) or []:
                mapped_comp['categories'].append({
                    'name': c.get('name'),
                    'details': c.get('details'),
                    'icon': resolve_icon_path(slug, c.get('icon'))
                })
            mapped['compatibility'] = mapped_comp
        # package contents
        if block.get('package_contents'):
            pc = block['package_contents']
            mapped_pc = {
                'title': pc.get('title'),
                'subtitle': pc.get('subtitle'),
                'items': []
            }
            for it in pc.get('items', []) or []:
                mapped_pc['items'].append({
                    'name': it.get('name'),
                    'details': it.get('details'),
                    'icon': resolve_icon_path(slug, it.get('icon'))
                })
            mapped['package_contents'] = mapped_pc
        # variants (Also Available In)
        variants = []
        for v in block.get('variants', []) or []:
            variants.append({
                'title': v.get('title'),
                'package_image': f"assets/images/product/{slug}/{v.get('package_image')}" if v.get('package_image') else None,
                'model_name': v.get('model_name'),
                'sku': v.get('sku'),
                'ean': v.get('ean'),
            })
        if variants:
            mapped['variants'] = variants
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
        # permalink slug must match Eleventy computed slug from product[lang].name
        friendly_slug = slugify(name or '') or slug
        url = f"/{lang_key}/products/{friendly_slug}/"
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
        en_json = call_llm_json(_llm_parse_prompt(md, slug), model="gpt-4.1-mini")
        en_json['slug'] = slug

        # 3) LLM translate (de)
        de_json_wrapped = call_llm_json(_llm_translate_prompt({'en': en_json.get('en', {})}), model="gpt-4.1-mini")
        de_json = {'de': de_json_wrapped.get('de', {})}

        # Determine asset slug based on English product name to keep URL and assets consistent
        en_name_raw = (en_json.get('en', {}) or {}).get('name') or ''
        asset_slug = slugify(en_name_raw) or slug

        # 4) map to our YAML (use asset_slug for all asset paths)
        yaml_data = _map_to_yaml(en_json.get('en', {}), de_json.get('de', {}), asset_slug)

        # ensure minimal required fields
        en_name = yaml_data['en'].get('name') or slug.replace('-', ' ').title()
        de_name = yaml_data['de'].get('name') or en_name
        category = yaml_data['en'].get('category', 'gan_charger')

        # 5) copy images (robust): prefer a folder named images (case-insensitive),
        # otherwise copy all image files found anywhere under tmp_dir to destination.
        dst_images_dir = os.path.join(ASSETS_PRODUCT_DIR, asset_slug)
        if os.path.exists(dst_images_dir):
            shutil.rmtree(dst_images_dir)
        os.makedirs(dst_images_dir, exist_ok=True)

        # find case-insensitive 'images' dir
        images_dir_ci = None
        try:
            for entry in os.listdir(tmp_dir):
                p = os.path.join(tmp_dir, entry)
                if os.path.isdir(p) and entry.lower() == 'images':
                    images_dir_ci = p
                    break
        except FileNotFoundError:
            images_dir_ci = None

        exts = {'.png', '.jpg', '.jpeg', '.svg', '.webp', '.gif'}
        copied_any = False
        def copy_all_images_from(source_root: str):
            nonlocal copied_any
            for root, _dirs, files in os.walk(source_root):
                # skip macOS metadata
                if os.path.basename(root).startswith('__MACOSX'):
                    continue
                for fn in files:
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in exts:
                        src_f = os.path.join(root, fn)
                        dst_f = os.path.join(dst_images_dir, fn)
                        try:
                            shutil.copy2(src_f, dst_f)
                            copied_any = True
                        except Exception:
                            logging.warning(f"Failed to copy image: {src_f}")

        if images_dir_ci and os.path.exists(images_dir_ci):
            # copy images directory recursively
            copy_all_images_from(images_dir_ci)
        else:
            # fallback: copy any image files under tmp_dir
            copy_all_images_from(tmp_dir)

        # 6) save product yaml
        product_yaml_path = os.path.join(PRODUCT_YAML_DIR, f"{slug}.yml")
        _save_yaml(product_yaml_path, yaml_data)

        # 7) update products catalog yaml
        first_image = (
            yaml_data['en'].get('catalog_image')
            or (yaml_data['en'].get('images') or [None])[0]
            or f"assets/images/product/{asset_slug}/product-1.svg"
        )
        _append_to_catalog(asset_slug, en_name, de_name, category, first_image)

        # 8) return URL for EN
        return f"/en/products/{asset_slug}/"

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


