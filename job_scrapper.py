import requests
from bs4 import BeautifulSoup
import dataLib
from config_manager import get_config
from logs import logProcesses
from ai_manager import extractClosingDate


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    # Let requests set Accept-Encoding itself: advertising "br" without the
    # brotli package installed makes response.text undecodable garbage.
    "Connection": "keep-alive",
}

def jobScrapper():
    """Scrapes job listings from the main page and saves them to the DB."""
    url = "https://jobwebghana.com/jobs/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error_msg = f"Error fetching job list: {e}"
        logProcesses(error_msg)
        print(error_msg)
        return {"status": False, "response": error_msg}

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all(id="titlo")
    
    if not jobs:
        msg = "No jobs found on the page."
        logProcesses(msg)
        print(msg)
        return {"status": False, "response": msg}

    keywords = get_config()["keywords"]

    job_dict = {}
    for job in jobs:
        result = job.find('a')
        if result and result.get('href'):
            jobLink = result['href']
            jobName = job.text.strip()
            if keywords and not any(k.lower() in jobName.lower() for k in keywords):
                continue
            job_dict[jobName] = jobLink

    if not job_dict:
        return "No New Job"

    return dataLib.saveJobs(job_dict)

def scrapJobDetails(url):
    """Scrapes individual job details, including the closing date."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding job details - simplified and made more robust
        jobDetail = soup.font.text.strip() if soup.font else "Job details not found"
        
        # Searching for application details
        apply_section = soup.find(size="3")
        applyDetails = apply_section.text.strip() if apply_section else "No details found"
        
        closingDate = extractClosingDate(applyDetails)

        result = {
            "status": True,
            "jobDetail": jobDetail,
            "howToApply": applyDetails,
            "link": url,
            "closingDate": closingDate,
            "response": "Job Details scrapped successfully"
        }
        logProcesses(result["response"])
        return result

    except requests.exceptions.RequestException as e:
        result = {"status": False, "response": f"Request error: {e}"}
        logProcesses(result["response"])
        return result
    except Exception as e:
        result = {"status": False, "response": f"An unexpected error occurred: {e}"}
        logProcesses(result["response"])
        return result

