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



def scrapJobDetails(url):
    # url = "https://jobwebghana.com/jobs/field-sales-agents-jiji-ghana/"
    # url = "https://jobwebghana.com/jobs/promoters-rmg-ghana-limited/"
    key_titles = ['job summary', 'purpose statement', 'about the role', 'job description', 'join our team']
    qualification_titles = ['qualifications', '']

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # jobDetail = soup.find(_class="how-to-apply")
    jobDetail = soup.font.text

    result = {
        "jobDetail": jobDetail,
        "link": url
    }

    return result

    # for i in range(len(jobDetail)):
    #     title = jobDetail[i].text.lower()
    #     if title == 'job summary':
    #         print(jobDetail[i+2].text)




    # for key, value in jobDetail.items():
    #     title = value.text.lower()
    #     if title == 'key responsibilities':
    #         print(key)

    # return jobDetail





# print(scrapJobDetails())