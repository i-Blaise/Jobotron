import google.generativeai as genai
import os
from env_config import APIKey

def AI_Summary(text, link):
    genai.configure(api_key = APIKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Summarize the following job description for a tweet along with the full link to the job provided: " + text + ". Job link:" + link + ". Add a Jobotron hashtag along with two other relating to the job and jobs in Ghana.")
    return response.text