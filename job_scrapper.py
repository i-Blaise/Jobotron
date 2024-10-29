import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint
import dataLib
from logs import logProcesses

def jobScrapper():
    # url = "https://www.ghanajob.com/job-vacancies-search-ghana/?utm_source=site&utm_medium=link&utm_campaign=search_split&utm_term=all_jobs&f%5B0%5D=im_field_offre_metiers%3A31"
    # url = "https://www.jobsinghana.com/jobs/indexnew.php?device=d"
    # url = "https://www.jobberman.com.gh/jobs"
    url = "https://jobwebghana.com/jobs/"

    # try:
    response = requests.get(url)
    
    # except ChunkedEncodingError(e):
    #     return "HTTP error"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = soup.find_all(id="titlo")


    # print(type(jobs))
    
    job_dict = { }

    for job in jobs:
        result = job.find('a')
        jobLink = result['href']
        jobName = job.text
        job_dict[jobName] = jobLink
        # print("https://jobgether.com/"+tag.get('href') + " Name of Job: " + tag.get('title'))

    return dataLib.saveJobs(job_dict)
    # return pprint.pprint(job_dict)



# def scrapJobDetails(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # jobDetail = soup.find(_class="how-to-apply")
#     jobDetail = soup.font.text

#     result = {
#         "jobDetail": jobDetail,
#         "link": url
#     }

#     return result





def scrapJobDetails(url):
    try:
        # Attempt to get the page content
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the request was unsuccessful

        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        jobDetail = soup.font.text if soup.font else "Job details not found"

        # Prepare result dictionary
        result = {
            "status": True,
            "jobDetail": jobDetail,
            "link": url,
            "response": "Job Details scrapped successfully"
        }
        logProcesses(result["response"])
        return result

    except requests.exceptions.RequestException as e:
        # print(f"Request error: {e}")
        result = {
            "status": False,
            "response": f"Request error: {e}"
        }
        logProcesses(result["response"])
        return result
    except AttributeError as e:
        # print(f"Parsing error: {e}")
        result = {
            "status": False,
            "response": f"Parsing error: : {e}"
        }
        logProcesses(result["response"])
        return result
    except Exception as e:
        # print(f"An unexpected error occurred: {e}")
        result = {
            "status": False,
            "response": f"An unexpected error occurred: {e}"
        }
        logProcesses(result["response"])
        return result

    return None  # Return None if an error occurs
