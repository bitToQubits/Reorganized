import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    def __init__(self):
        self.API_V1_STR: str = "/api/v1"
        self.POSTGRES_URL: str = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_SERVER"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB")
        )
        self.MIGRATION_POSTGRES_URL: str = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_SERVER"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB")
        )
        self.CHALLENGES_API_URL: str = "https://challenges.bettergroup.io/bp_backend/v1"
        self.CANDIDATE_ID = os.getenv("CANDIDATE_ID")
        self.CHALLENGES_API_KEY = os.getenv("CHALLENGES_API_KEY")
        self.API_KEY_AUTHENTICATION = "y2p3B1Mb1T7dbZAOV5F1W2Eh5"

settings = Settings()