import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# this class creates a generator that calls google gemini
class Generator:

    # constructor
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")