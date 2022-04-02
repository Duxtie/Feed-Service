from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8001",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # SQLALCHEMY_DATABASE_URI: str = "postgres://"
    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg2://"

    class Config:
        case_sensitive = True


settings = Settings()


# import os
# from pathlib import Path
#
# from dotenv import load_dotenv
#
#
# # dotenv_path = Path(__file__).resolve().parent / '..' / '..' / '..' / '.env'
# # load_dotenv(dotenv_path)
#
# load_dotenv("../../../.env")
#
# settings = os.environ