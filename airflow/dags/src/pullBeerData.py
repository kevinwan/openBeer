import requests
import json
from datetime import datetime
import os

start_url = "https://sampledata.petdesk.com/data/"

def generate_urls():
    """
	use the subtotal endpoint to generate a complete list of urls
	"""
    total = requests.get(start_url + "subtotals")
    urls = []
    if total.status_code == 200:
        for item in total.json():
            for page in range(item['numPages']):
                url = start_url + 'year/' + str(item['year']) + '/' + str(page+1)
                print(url)
                urls.append(url)
        return urls
    else:
        print("error code {0} in request subTotals".format(total.status_code))


def pull_beer_data():
    """
	use the rest api to pull beer data, then dump to local json files
	"""
    for url in generate_urls() :
        res = requests.get(url)
        
        # if the API request was sucessful, dump data to local json files
        # file names will be generated as "$year_$month_$page.json"
        if res.status_code == 200 :
            json_data = res.json()
            file_name = '_'.join(url.split('/')[-3:])+ '.json'
            full_name = os.path.join(os.path.dirname(__file__), 'data', file_name)

            with open(full_name, 'w') as outputfile:
                json.dump(json_data, outputfile)
        else :
            print("error code {0} in request subTotals".format(res.status_code))

if __name__ == "__main__": 
    pull_beer_data()