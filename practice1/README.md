# Docker と Anaconda3 実習教材リポジトリ

このフォルダは Docker と Anaconda3 を使った実習用の教材・設定をまとめたものです。

**目的**:
- Docker コンテナで Anaconda3 環境を再現し、Jupyter や実習用スクリプトで学習を行う。

**リポジトリ概要**:
- `docker-compose.yml`, `docker-compose.2nd.yml`, `docker-compose.3rd.yml`, `docker-compose.4th.yml`: 複数バージョンの docker-compose 設定ファイル（用途や構成の違いを段階的に管理）。
- `Dockerfile`, `Dockerfile.2nd`, `Dockerfile.3rd`, `Dockerfile.4th`: 各構成に対応する Dockerfile（Anaconda や必要パッケージのインストールを想定）。
- `start.sh`: 簡易起動スクリプト（実行権限を与えて利用）。
- `commands/`: 実習で利用するコマンドやサンプルスクリプトを格納するディレクトリ。
 - `workspace/`: 実習データを格納するディレクトリ（ボリュームマウント先として使用）。

**簡単な使い方（クイックスタート）**:
1. リポジトリの `practice1` ディレクトリへ移動:

```bash
cd practice1
```

2. 任意の docker-compose ファイルでコンテナをビルド＆起動（例: 4th）:

```bash
# Docker Compose V2 コマンド
docker compose -f docker-compose.4th.yml up --build -d

# もしくは互換の docker-compose
docker-compose -f docker-compose.4th.yml up --build -d
```

3. コンテナ内に入る（コンテナ名は `docker ps` で確認）:

```bash
docker exec -it <コンテナ名> /bin/bash
```

4. Anaconda3 環境で Jupyter を起動する例（コンテナ内またはローカルで）:

```bash
# 必要に応じて環境を作成
conda create -n practice python=3.10 -y
conda activate practice
pip install jupyterlab
# Jupyter を外部からアクセス可能に起動
jupyter lab --ip=0.0.0.0 --no-browser --allow-root
```

5. `start.sh` を使う場合:

```bash
chmod +x start.sh
./start.sh
```

**Anaconda3 実習のポイント**:
- コンテナ内で環境を固定すると受講者間で環境差が出にくくなります。
- `workspace/` をボリュームマウントしておくとデータの持ち回りが容易です。
- Jupyter 起動時のトークンやポート（通常 8888）が開放されていることを確認してください。

**注意事項**:
- 使う `docker-compose.*.yml` を切り替えることで環境の差分を試せます。
- 各 `Dockerfile*` の中身に Anaconda をインストールする手順がある想定ですが、実際の設定はファイルを確認してください。
- コンテナ内のユーザーやパーミッションによっては `--allow-root` 等の起動オプションが必要になります。

**次のステップ（提案）**:
- `Dockerfile.*` の内容を確認して README に環境作成手順を具体化する。
- 実習用ノートブック（`notebooks/`）やサンプルデータを `workspace/` に追加する。

**実行方法（ローカル / コンテナ）**:
- **ローカル（Anaconda / conda 推奨）:**
	- Conda 環境を作る（任意の名前 `practice` を使用する例）:

		```bash
		conda create -n practice python=3.10 -y
		conda activate practice
		pip install -r requirements.txt
		```

	- スクリプトを実行:

		```bash
		cd practice1
		python plot_gaussian.py
		# ヒストグラムも表示する場合
		python plot_gaussian.py --hist
		```

- **Jupyter でインタラクティブ実行:**
	- `plot_gaussian.ipynb` を開いて上から順にセルを実行します。`ipywidgets` を使うとスライダーで `mu`/`sigma` を操作できます。

- **Docker（コンテナ）上で Jupyter を使う場合）:**
	- `docker-compose.4th.yml` を使う例:

		```bash
		cd practice1
		docker compose -f docker-compose.4th.yml up -d --build
		```

	- ブラウザで JupyterLab にアクセス:

		- http://localhost:8888/lab?token=visible_token (`docker-compose.4th.yml` に設定した `JUPYTER_TOKEN` を使う)

	- コンテナに入って直接スクリプトを実行する場合:

		```bash
		docker exec -it linux_study_server /bin/bash
		python /workspace/plot_gaussian.py
		```

- **最大素数を求めるスクリプト**:
	- スクリプト `max_prime.py` を実行すると 1000 以下の最大の素数を表示します:

		```bash
		cd practice1
		python max_prime.py
		# 出力: 997
		```

**注意**:
- `requirements.txt` を更新した場合は Docker イメージを再ビルドしてください（`--build` オプションを付ける）。
- 公開環境でのトークン固定や root の SSH 設定はセキュリティ上のリスクがあります。教材用途に限定して利用してください。

----

README を `practice1` 配下に作成しました。
