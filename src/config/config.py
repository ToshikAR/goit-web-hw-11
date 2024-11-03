from decouple import config


class Config:
    __base = config("POSTQ_DB")
    __user = config("POSTQ_USER")
    __password = config("POSTQ_PASSWORD")
    __host = config("POSTQ_HOST")
    __port = config("POSTQ_PORT")

    DB_URL = f"postgresql+asyncpg://{__user}:{__password}@{__host}:{__port}/{__base}"


config = Config
