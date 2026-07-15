"""Compose blueprint: write product.md in the browser, manage draft images,
export a spec-compliant ZIP (product.md + images/) or submit it straight to
the existing V2 processor.

Drafts live in product-manager/drafts/<name>/ (gitignored).
"""
import io
import os
import re
import shutil
import zipfile

from flask import Blueprint, jsonify, request, send_file

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # repo root
DRAFTS_DIR = os.path.join(os.path.dirname(__file__), 'drafts')
INBOX_DIR = os.path.join(os.path.dirname(__file__), 'inbox')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')

TEMPLATE_DEFAULT = os.path.join(BASE_DIR, 'Sample-data', 'ALL_FIELDS_SAMPLE', 'product.md')
REF_DIR = os.path.join(BASE_DIR, 'ref_only')
ICONS_DIR = os.path.join(BASE_DIR, 'src', 'assets', 'images', 'icons')

IMG_EXTS = {'.png', '.jpg', '.jpeg', '.svg', '.webp', '.gif'}

compose = Blueprint('compose', __name__)


def _safe_name(name):
    name = re.sub(r'[^A-Za-z0-9._ -]', '', (name or '')).strip()
    name = re.sub(r'\s+', '-', name).strip('.-')
    return name[:80]


def _draft_dir(name, create=False):
    safe = _safe_name(name)
    if not safe:
        return None
    d = os.path.join(DRAFTS_DIR, safe)
    if create:
        os.makedirs(os.path.join(d, 'images'), exist_ok=True)
    return d if os.path.isdir(d) or create else None


def _draft_images(d):
    img_dir = os.path.join(d, 'images')
    if not os.path.isdir(img_dir):
        return []
    return sorted(f for f in os.listdir(img_dir)
                  if os.path.splitext(f)[1].lower() in IMG_EXTS)


def _templates():
    items = [{'id': 'all-fields', 'name': 'ALL FIELDS(全欄位標準樣板)', 'default': True}]
    if os.path.isdir(REF_DIR):
        for f in sorted(os.listdir(REF_DIR)):
            if f.endswith('.md'):
                items.append({'id': 'ref:' + f[:-3], 'name': 'ref_only / ' + f[:-3], 'default': False})
    return items


def _template_path(tid):
    if tid == 'all-fields':
        return TEMPLATE_DEFAULT
    if tid.startswith('ref:'):
        fname = _safe_name(tid[4:]) + '.md'
        p = os.path.join(REF_DIR, fname)
        if os.path.isfile(p):
            return p
    return None


# ------------------------------------------------------------------ metadata
@compose.get('/api/compose/meta')
def api_meta():
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    drafts = []
    for n in sorted(os.listdir(DRAFTS_DIR)):
        d = os.path.join(DRAFTS_DIR, n)
        if os.path.isdir(d):
            mp = os.path.join(d, 'product.md')
            drafts.append({'name': n, 'mtime': int(os.path.getmtime(mp)) if os.path.exists(mp) else 0})
    icons = []
    if os.path.isdir(ICONS_DIR):
        icons = sorted(f for f in os.listdir(ICONS_DIR) if f.endswith('.svg'))
    return jsonify({'ok': True, 'templates': _templates(), 'icons': icons, 'drafts': drafts})


@compose.get('/api/compose/template/<tid>')
def api_template(tid):
    p = _template_path(tid)
    if not p:
        return jsonify({'ok': False, 'error': '樣板不存在'}), 404
    with open(p, 'r', encoding='utf-8') as f:
        return jsonify({'ok': True, 'content': f.read()})


# -------------------------------------------------------------------- drafts
@compose.get('/api/compose/draft/<name>')
def api_draft_get(name):
    d = _draft_dir(name)
    if not d:
        return jsonify({'ok': False, 'error': '草稿不存在'}), 404
    mp = os.path.join(d, 'product.md')
    md = ''
    if os.path.exists(mp):
        with open(mp, 'r', encoding='utf-8') as f:
            md = f.read()
    return jsonify({'ok': True, 'name': os.path.basename(d), 'md': md, 'images': _draft_images(d)})


@compose.post('/api/compose/draft/<name>')
def api_draft_save(name):
    data = request.get_json(silent=True) or {}
    md = data.get('md')
    if md is None:
        return jsonify({'ok': False, 'error': '缺少 md 內容'}), 400
    d = _draft_dir(name, create=True)
    if not d:
        return jsonify({'ok': False, 'error': '草稿名稱無效'}), 400
    tmp = os.path.join(d, 'product.md.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(md)
    os.replace(tmp, os.path.join(d, 'product.md'))
    return jsonify({'ok': True, 'name': os.path.basename(d)})


@compose.delete('/api/compose/draft/<name>')
def api_draft_delete(name):
    d = _draft_dir(name)
    if not d:
        return jsonify({'ok': False, 'error': '草稿不存在'}), 404
    shutil.rmtree(d, ignore_errors=True)
    return jsonify({'ok': True})


# -------------------------------------------------------------------- images
@compose.post('/api/compose/draft/<name>/images')
def api_image_upload(name):
    d = _draft_dir(name, create=True)
    if not d:
        return jsonify({'ok': False, 'error': '草稿名稱無效'}), 400
    files = request.files.getlist('files') or []
    saved, skipped = [], []
    for fs in files:
        fname = _safe_name(fs.filename or '')
        ext = os.path.splitext(fname)[1].lower()
        if not fname or ext not in IMG_EXTS:
            skipped.append(fs.filename)
            continue
        fs.save(os.path.join(d, 'images', fname))
        saved.append(fname)
    return jsonify({'ok': True, 'saved': saved, 'skipped': skipped, 'images': _draft_images(d)})


@compose.delete('/api/compose/draft/<name>/images/<fname>')
def api_image_delete(name, fname):
    d = _draft_dir(name)
    if not d:
        return jsonify({'ok': False, 'error': '草稿不存在'}), 404
    safe = _safe_name(fname)
    p = os.path.join(d, 'images', safe)
    if os.path.exists(p):
        os.remove(p)
    return jsonify({'ok': True, 'images': _draft_images(d)})


@compose.get('/api/compose/draft/<name>/images/<fname>')
def api_image_get(name, fname):
    d = _draft_dir(name)
    if not d:
        return jsonify({'ok': False, 'error': '草稿不存在'}), 404
    p = os.path.join(d, 'images', _safe_name(fname))
    if not os.path.exists(p):
        return jsonify({'ok': False, 'error': '圖片不存在'}), 404
    return send_file(p)


# ----------------------------------------------------------------------- zip
def _build_zip_bytes(d):
    mp = os.path.join(d, 'product.md')
    if not os.path.exists(mp):
        return None
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(mp, 'product.md')
        for img in _draft_images(d):
            zf.write(os.path.join(d, 'images', img), 'images/' + img)
    buf.seek(0)
    return buf


@compose.get('/api/compose/draft/<name>/zip')
def api_zip_download(name):
    d = _draft_dir(name)
    if not d:
        return jsonify({'ok': False, 'error': '草稿不存在'}), 404
    buf = _build_zip_bytes(d)
    if buf is None:
        return jsonify({'ok': False, 'error': '草稿沒有 product.md'}), 400
    zip_name = os.path.basename(d) + '.zip'
    return send_file(buf, mimetype='application/zip', as_attachment=True, download_name=zip_name)


@compose.post('/api/compose/draft/<name>/submit')
def api_submit(name):
    d = _draft_dir(name)
    if not d:
        return jsonify({'ok': False, 'error': '草稿不存在'}), 404
    buf = _build_zip_bytes(d)
    if buf is None:
        return jsonify({'ok': False, 'error': '草稿沒有 product.md'}), 400

    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    zip_name = os.path.basename(d) + '.zip'
    zip_path = os.path.join(INBOX_DIR, zip_name)
    with open(zip_path, 'wb') as f:
        f.write(buf.getvalue())
    shutil.copy2(zip_path, os.path.join(BACKUP_DIR, zip_name))

    # same lazy-import path as the Products upload flow
    try:
        from processor_v2 import process_zip_v2  # type: ignore
        url = process_zip_v2(zip_path)
        return jsonify({'ok': True, 'product_url': url})
    except Exception as e:  # noqa: BLE001
        return jsonify({'ok': False, 'error': str(e)}), 500
