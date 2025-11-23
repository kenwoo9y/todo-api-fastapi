# python3.11のイメージをダウンロード
FROM python:3.11-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# アプリケーションコードをコピー
COPY api ./api

# uvicornのサーバーを立ち上げる
# Herokuでは$PORT環境変数を使用する必要があるため、CMDで動的に設定
CMD poetry run uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}