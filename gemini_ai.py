import google.generativeai as genai
import os
from env_config import APIKey

def AI_Summary(detail, link):
    genai.configure(api_key = APIKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Summarize the following job description for a tweet along with the full link to the job provided: " + detail + ". Job link:" + link + ". Add a Jobotron hashtag along with two other relating to the job and/or jobs in Ghana.")
    return response.text



def extractClosingDate(text):
    genai.configure(api_key = APIKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Text to analyze: '"+ text +"'. Extract the Closing Date from the text to analyze and only reply with the corressponding date in a DD/MM/YYY format. If theres not Closing Date to extract or the text to analyze says 'No details found', reply with only 'False'.")
    return response.text


def jobTips():
    genai.configure(api_key = APIKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a tweet that provides practical tips for job seekers in Ghana on how to stay competitive in the current job market. Please include relevant hashtags and #Jobotron. This tweet should be under 280 characters long")
    return response.text


# def adviceAndMotivation():
#     genai.configure(api_key = APIKey)
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content("Write a motivational tweet for job seekers in Ghana that encourages persistence in the job hunt and highlights the importance of staying positive or general motivation. Add relevant hashtags and #Jobotron. This tweet should be under 280 characters long")
#     return response.text


def adviceAndMotivation():
    genai.configure(api_key = APIKey)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a motivational on various topics of your choosing for a tweet for job seekers in Ghana . Add relevant hashtags and #Jobotron. This tweet should be under 280 characters long")
    return response.text

