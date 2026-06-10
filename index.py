from job_scrapper import jobScrapper, scrapJobDetails as jobwebScrapJobDetails
from jobberman_scrapper import jobbermanScrapper, jobbermanScrapJobDetails
from dataLib import retrieveData, countData, updatePostedJob, deleteOneData
from ai_manager import AI_Summary, jobTips, adviceAndMotivation

from createxpost import postJob
from logs import logProcesses
from datetime import datetime
from mongodbConnect import MongoDBManager

def check_db_connection():
    """Check MongoDB connection at startup and return True if available."""
    client = MongoDBManager.get_client()
    if client is None:
        print("ERROR: MongoDB connection failed. Check your MONGODB_URI in .env.")
        print("  - Ensure the MongoDB Atlas cluster is running.")
        print("  - Ensure your server's IP is whitelisted in MongoDB Atlas Network Access.")
        print("  - Verify dnspython is installed: pip install dnspython")
        logProcesses("STARTUP ERROR: MongoDB connection unavailable.")
        return False
    print("MongoDB connection: OK")
    return True


def has_date_elapsed(date_str):
    if not date_str or date_str == 'False':
        return False
    try:
        # Parse the date string (DD/MM/YYYY) into a datetime object
        input_date = datetime.strptime(date_str, "%d/%m/%Y")
        # Get the current date without the time part
        current_date = datetime.now().date()
        # Compare input date with the current date
        return input_date.date() < current_date
    except ValueError:
        return False

def startPoint():
    """Main orchestration function to process and post job listings."""
    # Health check: fail fast if DB is unavailable
    if not check_db_connection():
        return

    max_scrape_attempts = 3

    scrape_attempts = 0

    while True:
        count = countData()
        print(f"Current stored jobs: {count}")
        
        # Run scraper if we have fewer than 4 jobs to maintain a buffer
        if count < 4 and scrape_attempts < max_scrape_attempts:
            scrape_attempts += 1
            print(f"DB has fewer than 4 jobs. Running scrapers (attempt {scrape_attempts}/{max_scrape_attempts})...")
            
            # Run Jobwebghana scraper
            scrap_result = jobScrapper()
            logProcesses(f"Jobweb Scraper run result: {scrap_result}")
            
            # If no new jobs, try Jobberman
            if isinstance(scrap_result, str) and scrap_result in ("No New Job", "Database Unavailable"):
                print(f"Jobwebghana found no new jobs. Trying Jobberman...")
                scrap_result_jb = jobbermanScrapper()
                logProcesses(f"Jobberman Scraper run result: {scrap_result_jb}")
                if isinstance(scrap_result_jb, str) and scrap_result_jb in ("No New Job", "Database Unavailable"):
                    print(f"Jobberman returned: '{scrap_result_jb}'. Continuing to post remaining jobs if any.")
                    scrape_attempts = max_scrape_attempts
                elif isinstance(scrap_result_jb, dict) and not scrap_result_jb.get("status", True):
                    print(f"Jobberman Scraper failed: {scrap_result_jb.get('response')}. Continuing to post remaining jobs if any.")
                    scrape_attempts = max_scrape_attempts
            elif isinstance(scrap_result, dict) and not scrap_result.get("status", True):
                print(f"Jobweb Scraper failed: {scrap_result.get('response')}. Continuing to post remaining jobs if any.")
                scrape_attempts = max_scrape_attempts
                
            # Recalculate count after scraping
            count = countData()
            print(f"Current stored jobs after scrape attempt: {count}")

        if count > 0:
            job = retrieveData()
            if not job:
                print("No job retrieved from DB.")
                break
                
            jobLink = job['link']
            if 'jobberman.com' in jobLink:
                jobDetails = jobbermanScrapJobDetails(jobLink)
            else:
                jobDetails = jobwebScrapJobDetails(jobLink)
            
            if not jobDetails or not jobDetails.get("status"):
                print(f"Failed to scrap details for {jobLink}. Skipping this job.")
                updatePostedJob(job) # Mark as attempted so we move on
                continue

            expirationDate = jobDetails["closingDate"].strip()
            if has_date_elapsed(expirationDate):
                deleteOneData(job["_id"])
                print(f"Job '{job['name']}' deleted because it's expired.")
                continue # Try getting the next job
            
            twitterPost = AI_Summary(jobDetails["jobDetail"], jobDetails["link"])
            if twitterPost:
                postResult = postJob(twitterPost)
                if postResult["status"]:
                    updatePostedJob(job)
                    print(f"Job Tweeted: {job['name']}")
                else:
                    print(f"Failed to tweet job: {postResult.get('response')}")
            break # Success or finished attempt for this run
        else:
            print("Not enough jobs to post and scraper couldn't find new ones.")
            break


