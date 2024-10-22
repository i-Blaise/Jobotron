from job_scrapper import jobScrapper
from dataLib import retrieveData, countData, deleteAllData



def startPoint():
    if countData() >= 4:
        return retrieveData()

    
# print(startPoint())
print(countData())
# print(deleteAllData())









print(jobScrapper())

# print(retrieveData())