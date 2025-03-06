# Todo App

React + TypeScript + Vite + Tailwind CSS + Shadcn UI + FastAPI + PostgreSQL + Docker Compose

## 必要条件

- Docker
- Docker Compose
- Node.js v22.14.0（推奨）
- Python 3.12以上
- React v19
- TypeScript v5
- Tailwind CSS v4

## プロジェクト構成

```
todo-app/
├── backend/
├── frontend/
├── compose.yml
└── README.md
```

## セットアップと起動方法

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. 環境変数の設定

バックエンドの`.env`ファイルを作成:

```bash
cd backend
cp .env.example .env
```

必要な環境変数:
```
DATABASE_TYPE=postgresql
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=todo_db
DATABASE_USER=postgres
DATABASE_PASSWORD=password
SECRET_KEY=your-secret-key
```

### 3. SSL証明書の設定（仕方なく。。。）

DocBaseを確認したところ、システムの方にプロキシ部分で依頼すると解消するとのことでした。

`.ssl`ディレクトリを作成し、必要な証明書を配置:

```bash
mkdir .ssl
# 証明書をコピー
cp path/to/your/cert_IRET-SSL-TrsutCA.crt .ssl/
```

### 4. アプリケーションの起動

Docker Composeを使用してアプリケーションを起動:

```bash
docker compose up -d
```

これにより以下のサービスが起動します：
- バックエンド: http://localhost:8000
- フロントエンド: http://localhost:3000
- Storybook: http://localhost:6006
- PostgreSQL: localhost:5432

### 5. データベースのマイグレーション

```bash
docker compose exec backend alembic upgrade head
```

## 開発用コマンド

### フロントエンド

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev

# Storybookの起動
npm run storybook

# テストの実行
npm run test

# リントの実行
npm run lint

# フォーマットの実行
npm run prettier
```

### バックエンド

```bash
# 依存関係のインストール
uv pip install -e .

# 開発サーバーの起動
uvicorn app.main:app --reload

# マイグレーションの作成
alembic revision --autogenerate -m "description"

# マイグレーションの実行
alembic upgrade head
```

## API ドキュメント

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 使用している主要なパッケージ

### バックエンド
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Python-Jose
- Passlib
- Psycopg2-binary

### フロントエンド
- React
- TypeScript
- Vite
- Storybook
- Vitest
- Testing Library
- ESLint
- Prettier
- Tailwind CSS（Shadcn UI）
