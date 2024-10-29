from datetime import datetime

def logProcesses(response):
    currentDate = datetime.now()
    stringDate = currentDate.strftime('%m/%d/%Y  %X')
    f = open("logfile.txt", "a")
    f.write("\nLog issue date: "+ stringDate + ". ========= Log issue response: "+ response )
    f.close()