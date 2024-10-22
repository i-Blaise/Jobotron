from job_scrapper import jobScrapper
from dataLib import retrieveData, countData, deleteAllData



def startPoint():
    count = countData()
    if count >= 4:
        job = retrieveData()
        link = job['name']
        return link

    
print(startPoint())
# print(countData())
# print(deleteAllData())









# print(jobScrapper())

# print(retrieveData())