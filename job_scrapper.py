import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint
import dataLib

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

# print(jobScrapper())