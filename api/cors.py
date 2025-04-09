from decouple import config
from fastapi.middleware.cors import CORSMiddleware

# 環境変数からORIGINSを取得し、カンマで区切られた文字列をリストに変換
origins = config("CORS_ORIGINS").split(",")


def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
