import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def AI_Summary(detail, link):
    """
    Summarizes job details for a tweet using OpenAI.
    """
    prompt = (
        f"Summarize the following job description for a tweet along with the full link "
        f"to the job provided: {detail}. Job link: {link}. Add a #Jobotron hashtag "
        f"along with two other relating to the job and/or jobs in Ghana."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes job postings for social media."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error in AI_Summary: {e}")
        # Fallback to a basic summary if API fails
        return f"New Job: {detail[:100]}... Check it out here: {link} #Jobotron"

def extractClosingDate(text):
    """
    Extracts the closing date from job application details using OpenAI.
    """
    if text == "No details found":
        return "False"
        
    prompt = (
        f"Text to analyze: '{text}'. Extract the Closing Date from the text to "
        f"analyze and only reply with the corresponding date in a DD/MM/YYYY format. "
        f"If there is no Closing Date to extract, reply with only 'False'."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise data extractor. Only return the date or 'False'."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20
        )
        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        print(f"OpenAI error in extractClosingDate: {e}")
        # Simple fallback: look for a date pattern if OpenAI fails
        import re
        match = re.search(r'\d{2}/\d{2}/\d{4}', text)
        return match.group(0) if match else "False"

def jobTips():
    """
    Generates a job-seeking tip for Ghana using OpenAI.
    """
    prompt = (
        "Write a tweet that provides practical tips for job seekers in Ghana on "
        "how to stay competitive in the current job market. Please include relevant "
        "hashtags and #Jobotron. This tweet should be under 280 characters long."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career consultant specialized in the Ghanaian job market."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error in jobTips: {e}")
        return "Tip: Keep your LinkedIn profile updated and network within your industry! #Jobotron #GhanaJobs"

def adviceAndMotivation():
    """
    Generates motivational content for job seekers using OpenAI.
    """
    prompt = (
        "Write a motivational tweet for job seekers in Ghana that encourages persistence "
        "in the job hunt and highlights the importance of staying positive. "
        "Add relevant hashtags and #Jobotron. This tweet should be under 280 characters long."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a motivational coach for job seekers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error in adviceAndMotivation: {e}")
        return "Stay positive and keep pushing! Your opportunity is coming. #Jobotron #Ghana"
