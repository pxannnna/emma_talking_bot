"""
Step 2:
Text Generation using Gemini API
generate API key from: https://ai.google.dev/gemini-api/docs/api-key
"""

import google.generativeai as genai
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import *

# Configure the Gemini API with your API key.
genai.configure(api_key=GEMINI_API_KEY)


def gemini_api(text):
    # Initialize a genAI model
    model = genai.GenerativeModel(model_name=GEMINI_MODEL)
    # generate a response based on the input text.
    response = model.generate_content(text)

    print(response.text)


# -------------MAIN----------------

text = "Hi, be my personal AI robot. explain to me what an api is briefly?"
gemini_api(text)
