import requests
from urllib.parse import quote_plus
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

def jobbermanScrapper():
    """Scrapes job listings from Jobberman Ghana and saves them to the DB."""
    config = get_config()
    query = " ".join(config["keywords"]) or config["jobberman_fallback_query"]
    url = f"https://www.jobberman.com.gh/jobs?q={quote_plus(query)}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error_msg = f"Jobberman Scraper: Error fetching job list: {e}"
        logProcesses(error_msg)
        print(error_msg)
        return {"status": False, "response": error_msg}

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Jobberman listings are in links containing "/listings/"
    job_links = soup.find_all('a')
    
    job_dict = {}
    for elem in job_links:
        href = elem.get('href')
        if href and '/listings/' in href:
            jobName = elem.get_text().strip()
            if jobName:
                job_dict[jobName] = href

    if not job_dict:
        msg = "Jobberman Scraper: No jobs found on the page."
        logProcesses(msg)
        print(msg)
        return "No New Job"

    return dataLib.saveJobs(job_dict)

def jobbermanScrapJobDetails(url):
    """Scrapes individual job details from Jobberman, including the closing date."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        article = soup.find('article')
        if article:
            # Clean up excessive whitespace
            jobDetail = ' '.join(article.get_text(separator=' ').split())
        else:
            jobDetail = "Job details not found in article tag"
            
        # Jobberman doesn't always have a distinct how-to-apply block, the URL itself is the apply link.
        applyDetails = f"Apply directly at the following link: {url}"
        
        closingDate = extractClosingDate(jobDetail)

        result = {
            "status": True,
            "jobDetail": jobDetail[:5000], # Limit length to prevent token overflow
            "howToApply": applyDetails,
            "link": url,
            "closingDate": closingDate,
            "response": "Jobberman Job Details scrapped successfully"
        }
        logProcesses(result["response"])
        return result

    except requests.exceptions.RequestException as e:
        result = {"status": False, "response": f"Jobberman Request error: {e}"}
        logProcesses(result["response"])
        return result
    except Exception as e:
        result = {"status": False, "response": f"Jobberman An unexpected error occurred: {e}"}
        logProcesses(result["response"])
        return result
