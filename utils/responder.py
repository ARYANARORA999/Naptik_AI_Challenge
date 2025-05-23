import os
import google.generativeai as genai

def get_gemini_response(prompt):
    genai.configure(api_key=os.getenv("211322218465a402c5eda377136c91c42201f74e"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text
