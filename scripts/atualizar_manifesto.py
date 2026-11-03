#!/usr/bin/env python3
"""Validacao de release e publicacao do manifesto Calisxtreme. Execute pelo GitHub Actions."""
import json, os, re, subprocess, urllib.request
from pathlib import Path

REPO = 'SrDanvers/calisxtreme-atualizacoes'
PKG = 'com.calisxtreme.app'
TOKEN = os.environ['GITHUB_TOKEN']
EVENT = Path(os.environ['GITHUB_EVENT_PATH'])
if os.environ['GITHUB_REPOSITORY'] != REPO:
    raise SystemExit('Repositorio inesperado; atualizacao bloqueada.')

def github_json(url):
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {TOKEN}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'calisxtreme-updates'})
    with urllib.request.urlopen(req,timeout=45) as r:
        return json.load(r)

event = json.loads(EVENT.read_text())
release = event.get('release')
if release is None:
    release = github_json(f'https://api.github.com/repos/{REPO}/releases/latest')
if release.get('draft') or release.get('prerelease'):
    print('Release de testes ignorada: update.json permanece inalterado.')
    raise SystemExit(0)
tag = release.get('tag_name', '')
if not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
    raise SystemExit('Use a tag v2.0.1, v2.0.2, etc.')
body = re.sub(r'[*_`]', '', release.get('body') or '')
match = re.search(r'(?im)^\s*(?:c[oó]digo|versioncode)\s*:\s*(\d+)\s*$', body)
if match is None:
    raise SystemExit('A descricao precisa ter linha: Codigo: 14 (exemplo).')
version_code = int(match.group(1))
assets = [x for x in release.get('assets', []) if x.get('name','').lower().endswith('.apk')]
if len(assets) != 1 or assets[0].get('state') != 'uploaded':
    raise SystemExit('Anexe exatamente um APK, com upload concluido.')
asset = assets[0]
digest = asset.get('digest') or ''
if not re.fullmatch(r'sha256:[0-9a-fA-F]{64}', digest):
    raise SystemExit('GitHub nao forneceu SHA-256 valido ao APK.')

# Baixa o binario para conferir pacote, versao e assinatura ANTES de anunciar.
req = urllib.request.Request(asset['browser_download_url'], headers={
    'User-Agent': 'calisxtreme-updates'})
import hashlib
h = hashlib.sha256()
size = 0
with urllib.request.urlopen(req, timeout=90) as response, open('release_apk_tmp.apk', 'wb') as f:
    while True:
        part = response.read(65536)
        if not part: break
        size += len(part)
        if size > 150 * 1024 * 1024: raise SystemExit('APK ultrapassa 150 MB.')
        h.update(part); f.write(part)
if h.hexdigest() != digest.split(':',1)[1].lower():
    raise SystemExit('SHA-256 do asset nao corresponde ao arquivo baixado.')
import shutil
if not shutil.which('aapt') or not shutil.which('apksigner'):
    raise SystemExit('Ferramentas aapt/apksigner nao encontradas. Configure PATH do Android SDK no workflow.')
check = subprocess.run(['aapt','dump','badging','release_apk_tmp.apk'], capture_output=True, text=True, check=True)
line = next((x for x in check.stdout.splitlines() if x.startswith('package: ')), '')
pkg = re.search(r"name='([^']+)'", line)
code = re.search(r"versionCode='(\d+)'", line)
version_name = re.search(r"versionName='([^']+)'", line)
if not pkg or pkg.group(1) != PKG or not code or int(code.group(1)) != version_code:
    raise SystemExit(f'Pacote ou versionCode errado: {line}')
if not version_name or version_name.group(1) != tag.removeprefix('v'):
    raise SystemExit(f'Versao do APK difere da tag {tag}: {line}')
signed = subprocess.run(['apksigner','verify','--print-certs','release_apk_tmp.apk'],
                        check=True, capture_output=True, text=True)
certificates = []
for cert_line in signed.stdout.splitlines():
    marker = 'certificate SHA-256 digest:'
    if marker in cert_line:
        certificates.append(cert_line.split(marker, 1)[1].strip().lower())
expected_cert = 'cab25fb0ab0a691371281cf9dc00b0e258a9336794f4ac797b08a33de7510000'
if not certificates or any(cert != expected_cert for cert in certificates):
    print('Certificados apresentados pelo apksigner:', certificates)
    raise SystemExit('APK nao usa o certificado ORIGINAL do Calisxtreme; release bloqueada.')
print('Certificado original confirmado pelo apksigner.')
Path('release_apk_tmp.apk').unlink(missing_ok=True)

p = Path('update.json')
manifest = json.loads(p.read_text(encoding='utf-8'))
if manifest.get('applicationId') != PKG: raise SystemExit('Manifesto com pacote errado.')
old_code = int(manifest.get('latestVersionCode', 0))
if version_code <= old_code:
    print('Versao antiga ou ja publicada: nenhuma alteracao.'); raise SystemExit(0)
notes = [x[2:].strip() for x in body.splitlines() if x.lstrip().startswith('- ')]
manifest.update({
    'schemaVersion':1,
    'applicationId':PKG,
    'enabled':True,
    'latestVersionCode':version_code,
    'latestVersionName':tag.removeprefix('v'),
    'apkUrl':asset['browser_download_url'],
    'apkSha256':h.hexdigest(),
    'releaseNotes':'; '.join(notes)[:800] or release.get('name') or tag,
    'publishedAt':release.get('published_at') or ''})
p.write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
print(f'Publicado {tag}; versionCode {version_code}; sha256 {h.hexdigest()}')
