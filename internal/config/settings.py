import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()
        self.API_PREFIX = os.getenv('API_PREFIX', '/api')
        self.HEALTH_PREFIX = os.getenv('HEALTH_PREFIX', '/health')

        self.DATABASE_URL = os.getenv('DATABASE_URL')
        assert self.DATABASE_URL is not None

        self.AUTHORIZATION_URL = os.getenv('AUTHORIZATION_URL')
        self.TOKEN_URL = os.getenv('TOKEN_URL')
        self.REFRESH_URL = os.getenv('REFRESH_URL')
        self.AUTH_SCHEME_NAME = os.getenv('AUTH_SCHEME_NAME')

        self.ST_DWITHIN_KM = int(os.getenv('ST_DWITHIN_KM', '15'))


settings = Settings()
