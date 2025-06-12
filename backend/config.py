import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
    TEXTRAZOR_API_KEY = os.getenv("TEXTRAZOR_API_KEY")