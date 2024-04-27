from sqlalchemy import create_engine

from api.models.task_model import Base
from api.models.user_model import Base

DB_URL = "mysql+pymysql://root@mysql-db:3306/todo?charset=utf8"
#DB_URL = "postgresql+psycopg2://todo:todo@postgresql-db:5432/todo"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()