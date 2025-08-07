import os
import logging
import zipfile
import shutil
import json
import yaml
import openai
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get absolute paths from the script's location
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

WATCH_PATH = os.path.join(SCRIPT_DIR, 'inbox')
FAILED_PATH = os.path.join(SCRIPT_DIR, 'failed')
DETAILS_PATH = os.path.join(PROJECT_ROOT, 'src', '_data', 'content', 'products', 'details')
CATALOG_PATH = os.path.join(PROJECT_ROOT, 'src', '_data', 'content', 'products', 'catalog')
IMAGE_PATH = os.path.join(PROJECT_ROOT, 'static', 'assets', 'images', 'product')
PAGES_PATH = os.path.join(PROJECT_ROOT, 'src')

class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True

def get_llm_prompt(markdown_content, product_slug):
    # This function remains the same as in watcher.py
    json_schema = """
    {
      "product": {"name":"string", "badge":"string", "model_name":"string", "sku":"string", "ean":"string"},
      "category": "string",
      "hero": {"title":"string", "subtitle":"string", "image":"string", "gallery":["string"]},
      "features": {
        "section_title": "string", "section_intro": "string",
        "items": [{"title":"string", "description":"string", "bullets":["string"], "image":"string"}]
      },
      "specifications": {
        "section_title": "string", "technical": [{"label":"string", "value":"string"}],
        "performance": {"section_title":"string", "capacities": [{"capacity":"string", "read_speed":"string", "write_speed":"string"}]},
        "features": ["string"], "capacity_note": "string"
      },
      "compatibility": {"section_title": "string", "items": [{"label":"string", "note":"string"}]},
      "package": {"section_title": "string", "items": [{"name":"string", "description":"string"}]},
      "product_info": {"model_name":"string", "sku":"string", "ean":"string"}
    }
    """
    prompt = f"""
You are an expert data extraction system. Your task is to parse the provided Markdown and convert it into a structured JSON object.

**CRITICAL RULES:**
1.  **Strictly Adhere to Schema**: The output MUST be a valid JSON object.
2.  **Omit Missing Fields**: If a section, field, or table is NOT present in the Markdown, you MUST omit its key completely from the JSON output. DO NOT use `null`, empty strings, or invented data. This is the most important rule.
3.  **Parse Accurately**: Use the `[Tag]` prefixes and section headers (`##`, `###`) to identify data.

**Parsing Steps:**
- **`product`**:
    - `name`: From `# [Product Name] ...`
    - `model_name`, `sku`, `ean`, `badge`: From the top `<!-- ... -->` block.
- **`category`**: From `product_category` in the top `<!-- ... -->` block. This is mandatory.
- **`hero`**:
    - `title`, `subtitle`: From `[Hero Title]` and `[Hero Subtitle]` tags.
    - `image`: From `<!-- IMAGES: main.jpg -->`. Construct the full path: `/assets/images/product/{product_slug}/main.jpg`.
    - `gallery`: From `<!-- GALLERY: ... -->`. Create a list of full paths for each image.
- **`features`**:
    - `section_title`: From the `## Features` header.
    - `section_intro`: From the `<!-- section_intro: ... -->` comment under `## Features`.
    - `items`: Each `### [Feature Title]` starts a new item. Parse `[Feature Description]` and `[Bullet]` points. The feature image path comes from `<!-- feature_image: ... -->` and should be a full path.
- **`specifications`**:
    - `technical`: Parse from `[Spec]` tags under `### Technical`.
    - **`performance`**: If a Markdown table exists under `### Performance`, parse it. The table headers are the keys for each object in the `capacities` list.
    - `features`: Parse from `[Spec Feature]` tags under `### Features`.
- **`compatibility` and `package`**: Parse from `[Compatibility]` and `[Package]` tags respectively.
- **`product_info`**: Reuse `model_name`, `sku`, and `ean` from the top `product` section.

**JSON Schema Example (Your output must conform to this structure, but only include keys for data found in the text):**
```json
{json_schema}
```

**Markdown Text to Parse:**
---
{markdown_content}
---

**Final Instructions:**
Return ONLY the valid JSON object for the English content. Ensure it's a single, complete JSON object with no extra text.
"""
    return prompt


def get_translation_prompt(json_data):
    # This function remains the same as in watcher.py
    return f"""
You are a professional translator for a German tech accessory brand. Your tone is professional, clear, and modern.

Translate the values in the following JSON object from English to German.
Return a valid JSON object with the exact same structure and keys, but with all string values translated.
Preserve technical specifications and model numbers as they are. Do not translate `product.model_name`, `sku`, `ean`. Image paths must remain identical.

**JSON object to translate:**
```json
{json.dumps(json_data, indent=2)}
```

**Instructions:**
Return ONLY the valid translated JSON object. Do not include any other text or explanations.
"""

def call_openai_api(prompt, model="gpt-4-turbo"):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logging.error(f"OpenAI API call failed: {e}")
        raise

def process_zip(zip_path):
    product_slug = os.path.splitext(os.path.basename(zip_path))[0]
    temp_extract_path = os.path.join(WATCH_PATH, product_slug)
    
    try:
        # 1. Unzip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_path)
        logging.info(f"Unzipped to {temp_extract_path}")

        # 2. Read product.md
        md_path = os.path.join(temp_extract_path, 'product.md')
        if not os.path.exists(md_path):
            raise FileNotFoundError("product.md not found in the zip file.")
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 3. Call LLM to parse (EN)
        logging.info("Calling LLM to parse English content...")
        en_prompt = get_llm_prompt(md_content, product_slug)
        en_data = call_openai_api(en_prompt)
        logging.info("Successfully parsed English data.")

        # 4. Call LLM to translate (DE)
        logging.info("Calling LLM to translate to German...")
        de_prompt = get_translation_prompt(en_data)
        de_data = call_openai_api(de_prompt)
        logging.info("Successfully translated to German.")
        
        category = en_data.get("category")
        if not category:
            raise ValueError("'category' not found in parsed data. It is mandatory.")

        # 5. Create YML data files
        product_details_dir = os.path.join(DETAILS_PATH, product_slug)
        os.makedirs(product_details_dir, exist_ok=True)
        with open(os.path.join(product_details_dir, 'en.yml'), 'w', encoding='utf-8') as f:
            yaml.dump(en_data, f, Dumper=NoAliasDumper, allow_unicode=True, sort_keys=False)
        with open(os.path.join(product_details_dir, 'de.yml'), 'w', encoding='utf-8') as f:
            yaml.dump(de_data, f, Dumper=NoAliasDumper, allow_unicode=True, sort_keys=False)
        logging.info(f"Created YML files in {product_details_dir}")

        # 6. Copy images
        source_image_dir = os.path.join(temp_extract_path, 'images')
        dest_image_dir = os.path.join(IMAGE_PATH, product_slug)
        if os.path.exists(dest_image_dir):
            shutil.rmtree(dest_image_dir) # Overwrite if exists
        if os.path.exists(source_image_dir):
            shutil.copytree(source_image_dir, dest_image_dir)
            logging.info(f"Copied images to {dest_image_dir}")

        # 7. Update catalog files
        for lang, data in [('en', en_data), ('de', de_data)]:
            catalog_file = os.path.join(CATALOG_PATH, f'{lang}.yml')
            with open(catalog_file, 'r', encoding='utf-8') as f:
                catalog_data = yaml.safe_load(f)
            
            # Remove existing entry if it exists to prevent duplicates
            if category in catalog_data['products']:
                catalog_data['products'][category] = [p for p in catalog_data['products'][category] if p.get('link') != f"/{lang}/products/{category}/{product_slug}/"]

            new_entry = {
                'name': data['product']['name'],
                'description': data['hero']['subtitle'],
                'details': "",
                'image': data['hero']['image'],
                'alt': data['product']['name'],
                'link': f"/{lang}/products/{category}/{product_slug}/"
            }
            if category not in catalog_data['products']:
                 catalog_data['products'][category] = []
            catalog_data['products'][category].append(new_entry)
            
            with open(catalog_file, 'w', encoding='utf-8') as f:
                yaml.dump(catalog_data, f, Dumper=NoAliasDumper, allow_unicode=True, sort_keys=False)
            logging.info(f"Updated catalog file: {catalog_file}")

        # 8. Create NJK page files
        for lang, data in [('en', en_data), ('de', de_data)]:
            page_dir = os.path.join(PAGES_PATH, lang, 'products', category, product_slug)
            os.makedirs(page_dir, exist_ok=True)
            njk_content = f"""---
title: "{data['product']['name']}"
lang: {lang}
permalink: /{lang}/products/{category}/{product_slug}/
---
{{% set product = content.products.details.{product_slug.replace('-', '_')}.{lang} %}}
{{% include "product-detail.njk" %}}
"""
            with open(os.path.join(page_dir, 'index.njk'), 'w', encoding='utf-8') as f:
                f.write(njk_content)
            logging.info(f"Created NJK file in {page_dir}")

        logging.info(f"Successfully processed product: {product_slug}")
        # Return the URL of the new product page
        product_url = f"/en/products/{category}/{product_slug}/"
        return product_url

    except Exception as e:
        logging.error(f"Failed to process {os.path.basename(zip_path)}: {e}", exc_info=True)
        # Move to a 'failed' folder
        if not os.path.exists(FAILED_PATH):
            os.makedirs(FAILED_PATH)
        # Ensure the source file exists before moving
        if os.path.exists(zip_path):
            shutil.move(zip_path, os.path.join(FAILED_PATH, os.path.basename(zip_path)))
            logging.info(f"Moved failed zip to {FAILED_PATH}")
        # Re-raise the exception to be caught by the server
        raise
        
    finally:
        # Clean up temp folder
        if os.path.exists(temp_extract_path):
            shutil.rmtree(temp_extract_path)
        # Remove the original zip from inbox if processing was successful
        if os.path.exists(zip_path) and not os.path.exists(os.path.join(FAILED_PATH, os.path.basename(zip_path))):
             os.remove(zip_path)


