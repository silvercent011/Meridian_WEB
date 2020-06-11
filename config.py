from os import getenv
from dotenv import load_dotenv
load_dotenv()


class Settings:
    API_LINK = getenv('API_LINK')
    MD5_KEY = getenv('MD5_KEY')
    SCR_KEY = getenv('SCR_KEY')
    LOGO_LINK = getenv('LOGO_LINK')
    PORT = getenv('PORT')


app_config = Settings()
