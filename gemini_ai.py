import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

API_KEY = os.getenv("GEMINI_API_KEY")

def AI_Summary(detail, link):
    if not HAS_GEMINI:
        print("Gemini AI dependency missing. Returning generic summary.")
        return f"New Job: {detail[:100]}... Check it out here: {link} #Jobotron"
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Summarize the following job description for a tweet along with the full link to the job provided: " + detail + ". Job link:" + link + ". Add a Jobotron hashtag along with two other relating to the job and/or jobs in Ghana.")
        return response.text
    except Exception as e:
        print(f"Gemini AI error: {e}")
        return f"Job: {link} #Jobotron"

def extractClosingDate(text):
    if not HAS_GEMINI:
        # Simple regex or fallback for closing date
        import re
        # Look for something like DD/MM/YYYY
        match = re.search(r'\d{2}/\d{2}/\d{4}', text)
        return match.group(0) if match else "False"
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Text to analyze: '"+ text +"'. Extract the Closing Date from the text to analyze and only reply with the corressponding date in a DD/MM/YYY format. If theres not Closing Date to extract or the text to analyze says 'No details found', reply with only 'False'.")
        return response.text.strip()
    except Exception as e:
        print(f"Gemini AI error in extractClosingDate: {e}")
        return "False"

def jobTips():
    if not HAS_GEMINI:
        return "Tip: Keep your LinkedIn profile updated! #Jobotron #GhanaJobs"
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Write a tweet that provides practical tips for job seekers in Ghana on how to stay competitive in the current job market. Please include relevant hashtags and #Jobotron. This tweet should be under 280 characters long")
        return response.text
    except Exception:
        return "Success in your job search! #Jobotron"

def adviceAndMotivation():
    if not HAS_GEMINI:
        return "Stay positive and keep applied! Your dream job is out there. #Jobotron #Motivation"
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Write a motivational on various topics of your choosing for a tweet for job seekers in Ghana . Add relevant hashtags and #Jobotron. This tweet should be under 280 characters long")
        return response.text
    except Exception:
        return "Keep pushing forward! #Jobotron"

