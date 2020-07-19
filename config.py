from os import getenv
from dotenv import load_dotenv
load_dotenv()


class Settings:
    API_LINK = getenv('API_LINK')
    MD5_KEY = getenv('MD5_KEY')
    SCR_KEY = getenv('SCR_KEY')
    LOGO_LINK = getenv('LOGO_LINK')
    BOLETIM_API = getenv('BOLETIM_API')
    SCH_NAME = getenv('SCH_NAME')
    PORT = getenv('PORT')
    VERSION = getenv('VERSION')
    BOLETIM_LINK = getenv('LINK_BOLETIM')
    LINK_IMG_ALUNO = getenv('LINK_IMG_ALUNO')


app_config = Settings()
