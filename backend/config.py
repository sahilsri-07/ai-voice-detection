import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VOICE_API_KEY", "CHANGE_ME_IN_PROD")

ALLOWED_LANGUAGES = {"ta": "Tamil", "en": "English", "hi": "Hindi",
                     "ml": "Malayalam", "te": "Telugu"}