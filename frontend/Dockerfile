# ベースイメージとしてNode.jsを使用
FROM node:22-slim

# 作業ディレクトリを設定
WORKDIR /app

COPY .ssl/cert_IRET-SSL-TrsutCA.crt /etc/ssl/certs/IRET-SSL-TrsutCA.crt

# パッケージファイルをコピー
COPY package.json package-lock.json ./

ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/IRET-SSL-TrsutCA.crt

# 依存関係をインストール
RUN npm install

# 開発用サーバの起動
CMD ["npm", "run", "dev"]