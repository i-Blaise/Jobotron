from pymongo import MongoClient
import urllib.parse

PASSWORD = urllib.parse.quote_plus('bl@!!se-3296')
USERNAME = urllib.parse.quote_plus('Jobotron-admin')

uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@jobotron.1uucl.mongodb.net/?retryWrites=true&w=majority&appName=Jobotron"
client = MongoClient(uri)

try:
    database = client["jobs"]
    collection = database["jobsToPost"]
    # result = collection.insert_one({ "name" : "value" })
    # print(result.acknowledged)
    client.close()
except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

