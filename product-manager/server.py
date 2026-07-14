import os
import re
import json
import shutil
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

# Allow importing the existing V2 processor
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GEN_V2_DIR = os.path.join(BASE_DIR, 'product-generator-v2')
if GEN_V2_DIR not in sys.path:
    sys.path.insert(0, GEN_V2_DIR)

# NOTE: processor_v2 builds an OpenAI client at import time and dies without
# OPENAI_API_KEY, so it is imported lazily inside upload() — this lets the
# admin (and its Setup wizard) boot before any key exists.


PROJECT_ROOT = BASE_DIR
PRODUCT_YAML_DIR = os.path.join(PROJECT_ROOT, 'src', '_data', 'products')
PRODUCTS_CATALOG_FILE = os.path.join(PROJECT_ROOT, 'src', '_data', 'products.yml')
ASSETS_PRODUCT_DIR = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images', 'product')

INBOX_DIR = os.path.join(os.path.dirname(__file__), 'inbox')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

from ops import ops as ops_blueprint  # noqa: E402
app.register_blueprint(ops_blueprint)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def ensure_dirs():
    os.makedirs(PRODUCT_YAML_DIR, exist_ok=True)
    os.makedirs(ASSETS_PRODUCT_DIR, exist_ok=True)
    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


def slugify_name(text: str) -> str:
    if not text:
        return ''
    text = text.strip().lower()
    # remove dots between alphanumerics (e.g., m.2 -> m2)
    text = re.sub(r'(?<=[a-z0-9])\.(?=[a-z0-9])', '', text)
    text = re.sub(r"[^a-z0-9]+", '-', text)
    text = re.sub(r"-+", '-', text)
    return text.strip('-')


def read_yaml(path: str) -> Optional[Dict[str, Any]]:
    import yaml
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def write_yaml(path: str, data: Any):
    import yaml
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def list_products() -> List[Dict[str, Any]]:
    """Scan YAML files and return a list of products grouped by category."""
    results: List[Dict[str, Any]] = []
    for fname in sorted(os.listdir(PRODUCT_YAML_DIR)):
        if not fname.endswith('.yml'):
            continue
        path = os.path.join(PRODUCT_YAML_DIR, fname)
        data = read_yaml(path)
        if not data or 'en' not in data:
            continue
        en = data.get('en', {}) or {}
        de = data.get('de', {}) or {}
        en_name = en.get('name') or fname[:-4]
        de_name = de.get('name') or en_name
        category = (en.get('category') or '').strip().lower() or 'gan_charger'
        # derive asset slug from first image if possible
        images = en.get('images') or de.get('images') or []
        asset_slug = None
        if images:
            m = re.search(r"assets/images/product/([^/]+)/", images[0])
            if m:
                asset_slug = m.group(1)
        friendly_en_slug = slugify_name(en_name)
        friendly_de_slug = slugify_name(de_name)
        results.append({
            'yaml_file': fname,
            'en_name': en_name,
            'de_name': de_name,
            'category': category,
            'asset_slug': asset_slug,
            'url_en': f"/en/products/{friendly_en_slug}/",
            'url_de': f"/de/products/{friendly_de_slug}/",
            'images_count': len(images),
        })
    return results


def delete_products(yaml_files: List[str]) -> Dict[str, Any]:
    report = {'deleted': [], 'errors': []}
    # load catalog once
    import yaml
    catalog = read_yaml(PRODUCTS_CATALOG_FILE) or {}
    for fname in yaml_files:
        try:
            path = os.path.join(PRODUCT_YAML_DIR, fname)
            data = read_yaml(path) or {}
            en = data.get('en', {}) or {}
            de = data.get('de', {}) or {}
            en_name = en.get('name') or ''
            de_name = de.get('name') or en_name
            friendly_en = slugify_name(en_name)
            friendly_de = slugify_name(de_name)
            # remove assets
            images = en.get('images') or de.get('images') or []
            asset_slug = None
            if images:
                m = re.search(r"assets/images/product/([^/]+)/", images[0])
                if m:
                    asset_slug = m.group(1)
            if asset_slug:
                assets_dir = os.path.join(ASSETS_PRODUCT_DIR, asset_slug)
                if os.path.exists(assets_dir):
                    shutil.rmtree(assets_dir, ignore_errors=True)

            # remove from catalog (both langs)
            for lang in ['en', 'de']:
                if lang in catalog and 'categories' in catalog[lang]:
                    cats = catalog[lang]['categories']
                    # Skip 'tabs' as it's a list, not a product category
                    for group_key, group in list(cats.items()):
                        if group_key == 'tabs':
                            continue
                        if isinstance(group, dict) and 'products' in group:
                            prods = group.get('products', []) or []
                            target_slug = friendly_en if lang == 'en' else friendly_de
                            url = f"/{lang}/products/{target_slug}/"
                            new_list = [p for p in prods if p.get('url') != url]
                            group['products'] = new_list

            # remove YAML file
            if os.path.exists(path):
                os.remove(path)

            report['deleted'].append(fname)
        except Exception as e:
            logging.exception("Delete failed for %s", fname)
            report['errors'].append({'file': fname, 'error': str(e)})

    # save catalog back
    write_yaml(PRODUCTS_CATALOG_FILE, catalog)
    return report


@app.route('/')
def index():
    return render_template('dashboard.html', active='dashboard')


@app.route('/setup')
def setup_page():
    return render_template('setup.html', active='setup')


@app.route('/products')
def products_page():
    return render_template('products.html', active='products')


@app.route('/ops')
def ops_page():
    return render_template('ops.html', active='ops')


@app.route('/api/list')
def api_list():
    try:
        items = list_products()
        # group by category
        groups: Dict[str, List[Dict[str, Any]]] = {}
        for it in items:
            groups.setdefault(it['category'], []).append(it)
        return jsonify({ 'ok': True, 'groups': groups, 'count': len(items) })
    except Exception as e:
        logging.exception("List failed")
        return jsonify({ 'ok': False, 'error': str(e) }), 500


@app.route('/api/delete', methods=['POST'])
def api_delete():
    data = request.get_json(silent=True) or {}
    files = data.get('yaml_files') or []
    if not isinstance(files, list) or not files:
        return jsonify({ 'ok': False, 'error': 'No yaml_files provided' }), 400
    res = delete_products(files)
    return jsonify({ 'ok': True, **res })


@app.route('/upload', methods=['POST'])
def upload():
    ensure_dirs()
    if 'file' not in request.files:
        return jsonify({ 'ok': False, 'error': 'No file part' }), 400
    file = request.files['file']
    if not file or not file.filename:
        return jsonify({ 'ok': False, 'error': 'No file selected' }), 400
    if not file.filename.lower().endswith('.zip'):
        return jsonify({ 'ok': False, 'error': 'Only .zip accepted' }), 400

    filename = secure_filename(file.filename)
    zip_path = os.path.join(INBOX_DIR, filename)
    file.save(zip_path)

    # backup policy: keep latest by filename (overwrite)
    backup_path = os.path.join(BACKUP_DIR, filename)
    shutil.copy2(zip_path, backup_path)

    # process via existing V2 (lazy import: needs OPENAI_API_KEY, may be set
    # via the Setup wizard after this server started — load_dotenv() inside
    # processor_v2 picks up the fresh .env)
    try:
        from processor_v2 import process_zip_v2  # type: ignore
        url = process_zip_v2(zip_path)
        return jsonify({ 'ok': True, 'product_url': url })
    except Exception as e:
        logging.exception("Process failed")
        return jsonify({ 'ok': False, 'error': str(e) }), 500


if __name__ == '__main__':
    ensure_dirs()
    host = os.environ.get('ADMIN_HOST', '127.0.0.1')
    port = int(os.environ.get('ADMIN_PORT', '5012'))
    app.run(host=host, port=port, debug=False)


