"""Ops blueprint: environment setup wizard, health checks, build/preview/deploy.

Mounted by server.py. Product upload/list/delete logic lives in server.py and
is intentionally untouched.
"""
import os
import shutil
import signal
import subprocess
import threading

from flask import Blueprint, jsonify, request

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # repo root
ENV_PATH = os.path.join(BASE_DIR, '.env')

# Keys managed by the setup wizard. Secrets are never echoed back to the UI.
ENV_KEYS = ['OPENAI_API_KEY', 'FTP_HOST', 'FTP_USER', 'FTP_PASS', 'FTP_REMOTE_DIR', 'UPLOAD_PARALLEL']
SECRET_KEYS = {'OPENAI_API_KEY', 'FTP_PASS'}
REQUIRED_KEYS = ['OPENAI_API_KEY', 'FTP_HOST', 'FTP_USER', 'FTP_PASS']

ops = Blueprint('ops', __name__)


# ---------------------------------------------------------------- job runner
# Single job at a time; log kept in memory and polled by the UI.
_job_lock = threading.Lock()
_job = {'id': 0, 'name': None, 'status': 'idle', 'log': [], 'rc': None}


def _start_job(name, cmd, cwd=BASE_DIR):
    with _job_lock:
        if _job['status'] == 'running':
            return None
        _job['id'] += 1
        _job.update({'name': name, 'status': 'running', 'log': [], 'rc': None})
        jid = _job['id']

    def worker():
        try:
            p = subprocess.Popen(
                cmd, cwd=cwd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1,
            )
            for line in p.stdout:
                _job['log'].append(line.rstrip('\n'))
                if len(_job['log']) > 4000:
                    del _job['log'][:2000]
            p.wait()
            _job['rc'] = p.returncode
            _job['status'] = 'done' if p.returncode == 0 else 'failed'
        except Exception as e:  # noqa: BLE001
            _job['log'].append(f'[admin] job error: {e}')
            _job['rc'] = -1
            _job['status'] = 'failed'

    threading.Thread(target=worker, daemon=True).start()
    return jid


@ops.get('/api/job')
def api_job():
    return jsonify({
        'ok': True,
        'id': _job['id'], 'name': _job['name'],
        'status': _job['status'], 'rc': _job['rc'],
        'log': '\n'.join(_job['log'][-1500:]),
    })


def _busy_response():
    return jsonify({'ok': False, 'error': f"另一個工作({_job['name']})執行中,請稍候"}), 409


# ------------------------------------------------------------------- actions
@ops.post('/api/run/install')
def api_run_install():
    jid = _start_job('npm install', ['npm', 'install'])
    return _busy_response() if jid is None else jsonify({'ok': True, 'id': jid})


@ops.post('/api/run/build')
def api_run_build():
    jid = _start_job('build', ['npm', 'run', 'build'])
    return _busy_response() if jid is None else jsonify({'ok': True, 'id': jid})


@ops.post('/api/run/deploy_dry')
def api_run_deploy_dry():
    jid = _start_job('deploy (dry-run)', ['bash', 'upload_checksum_manifest.sh', '--dry-run'])
    return _busy_response() if jid is None else jsonify({'ok': True, 'id': jid})


@ops.post('/api/run/deploy')
def api_run_deploy():
    jid = _start_job('deploy', ['bash', 'upload_checksum_manifest.sh'])
    return _busy_response() if jid is None else jsonify({'ok': True, 'id': jid})


@ops.post('/api/run/deploy_full')
def api_run_deploy_full():
    jid = _start_job('deploy (full mirror)', ['bash', 'upload_to_ftp.sh'])
    return _busy_response() if jid is None else jsonify({'ok': True, 'id': jid})


# ------------------------------------------------------------------- preview
_preview = {'proc': None}
PREVIEW_PORT = int(os.environ.get('PREVIEW_PORT', '8080'))


def _preview_running():
    p = _preview['proc']
    return p is not None and p.poll() is None


@ops.post('/api/preview/start')
def api_preview_start():
    if _preview_running():
        return jsonify({'ok': True, 'running': True, 'url': f'http://localhost:{PREVIEW_PORT}/'})
    try:
        _preview['proc'] = subprocess.Popen(
            ['npx', '@11ty/eleventy', '--serve', f'--port={PREVIEW_PORT}'],
            cwd=BASE_DIR,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        return jsonify({'ok': True, 'running': True, 'url': f'http://localhost:{PREVIEW_PORT}/'})
    except Exception as e:  # noqa: BLE001
        return jsonify({'ok': False, 'error': str(e)}), 500


@ops.post('/api/preview/stop')
def api_preview_stop():
    p = _preview['proc']
    if p is not None and p.poll() is None:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except Exception:  # noqa: BLE001
            try:
                p.terminate()
            except Exception:  # noqa: BLE001
                pass
    _preview['proc'] = None
    return jsonify({'ok': True, 'running': False})


# ----------------------------------------------------------------------- env
def _env_map():
    m = {}
    if not os.path.exists(ENV_PATH):
        return m
    with open(ENV_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#') or '=' not in s:
                continue
            k, v = s.split('=', 1)
            m[k.strip()] = v.strip().strip('"').strip("'")
    return m


@ops.get('/api/env')
def api_env_get():
    m = _env_map()
    out = {}
    for k in ENV_KEYS:
        v = m.get(k, '')
        entry = {'set': bool(v)}
        if k not in SECRET_KEYS:
            entry['value'] = v
        out[k] = entry
    return jsonify({'ok': True, 'exists': os.path.exists(ENV_PATH), 'keys': out})


@ops.post('/api/env')
def api_env_post():
    data = request.get_json(silent=True) or {}
    updates = {}
    for k in ENV_KEYS:
        v = data.get(k)
        if isinstance(v, str) and v.strip():
            updates[k] = v.strip()
    if not updates:
        return jsonify({'ok': False, 'error': '沒有可更新的欄位'}), 400

    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()

    seen = set()
    new_lines = []
    for line in lines:
        s = line.strip()
        if s and not s.startswith('#') and '=' in s:
            k = s.split('=', 1)[0].strip()
            if k in updates:
                new_lines.append(f'{k}={updates[k]}')
                seen.add(k)
                continue
        new_lines.append(line)
    for k, v in updates.items():
        if k not in seen:
            new_lines.append(f'{k}={v}')

    tmp = ENV_PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines).rstrip('\n') + '\n')
    os.replace(tmp, ENV_PATH)
    try:
        os.chmod(ENV_PATH, 0o600)
    except Exception:  # noqa: BLE001
        pass
    return jsonify({'ok': True, 'updated': sorted(updates.keys())})


# -------------------------------------------------------------------- health
def _cmd_out(cmd, timeout=6):
    try:
        r = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0:
            return r.stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return None


@ops.get('/api/health')
def api_health():
    tools = {}
    for t in ['node', 'npm', 'python3', 'git', 'lftp', 'curl']:
        ok = shutil.which(t) is not None
        ver = None
        if ok:
            out = _cmd_out([t, '--version'])
            if out:
                ver = out.splitlines()[0]
        tools[t] = {'ok': ok, 'version': ver}

    m = _env_map()
    env = {k: bool(m.get(k)) for k in REQUIRED_KEYS}

    git = {}
    branch = _cmd_out(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    if branch:
        git['branch'] = branch
        git['last_commit'] = _cmd_out(['git', 'log', '-1', '--format=%h %s'])
        porcelain = _cmd_out(['git', 'status', '--porcelain'])
        git['dirty'] = len([l for l in (porcelain or '').splitlines() if l.strip()])
        ab = _cmd_out(['git', 'rev-list', '--left-right', '--count', 'HEAD...origin/main'])
        if ab and '\t' in ab:
            ahead, behind = ab.split('\t')
            git['ahead'] = int(ahead)
            git['behind'] = int(behind)

    return jsonify({
        'ok': True,
        'tools': tools,
        'env': {'exists': os.path.exists(ENV_PATH), 'keys': env},
        'node_modules': os.path.isdir(os.path.join(BASE_DIR, 'node_modules')),
        'site_built': os.path.isdir(os.path.join(BASE_DIR, '_site')),
        'git': git,
        'preview': {'running': _preview_running(), 'url': f'http://localhost:{PREVIEW_PORT}/'},
        'job': {'status': _job['status'], 'name': _job['name']},
    })
