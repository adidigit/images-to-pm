import requests
import json
basic_url = 'https://aqs.epa.gov/data/api/sampleData/byCounty?email=test@aqs.api&key=test&param=88101&bdate={0}0101&edate={0}1231&state=06&county=037'
out_file = '/home/adiraz/adiraz/pm_data/{0}'
years = list(range(2010,2021))
for year in years:
    url = basic_url.format(year)
    out = requests.get(url)
    with open(out_file.format(year) +'.json', 'w') as f:
        json.dump(f,out)
