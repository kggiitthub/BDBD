#!/usr/bin/env bash
set -euo pipefail

# conda 初期化
. /opt/conda/etc/profile.d/conda.sh || true

# SSH をバックグラウンドで起動
/usr/sbin/sshd

# Jupyter 設定
CONFIG_DIR=/root/.jupyter
CONFIG_FILE=${CONFIG_DIR}/jupyter_server_config.py
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_FILE" <<'PY'
import os
c = get_config()
port = int(os.environ.get('JUPYTER_PORT', 8888))
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = port
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True
PY

# パスワードが指定されていればハッシュ化して設定
if [ -n "${JUPYTER_PASSWORD:-}" ]; then
    HASH=$(/opt/conda/bin/python - <<'PY'
from notebook.auth import passwd
import os
print(passwd(os.environ['JUPYTER_PASSWORD']))
PY
)
    cat >> "$CONFIG_FILE" <<PYCFG
c.ServerApp.password = u'${HASH}'
PYCFG
fi

# トークンが指定されていれば設定、なければ自動生成してログに出力
if [ -n "${JUPYTER_TOKEN:-}" ]; then
    cat >> "$CONFIG_FILE" <<PYCFG
c.ServerApp.token = u'${JUPYTER_TOKEN}'
PYCFG
else
    TOKEN=$(/opt/conda/bin/python - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)
    cat >> "$CONFIG_FILE" <<PYCFG
c.ServerApp.token = u'${TOKEN}'
PYCFG
    echo "Jupyter token: ${TOKEN}" >&2
fi

# 起動
exec /opt/conda/bin/jupyter lab --config="$CONFIG_FILE"
