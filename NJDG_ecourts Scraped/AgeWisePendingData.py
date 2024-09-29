import requests
from bs4 import BeautifulSoup
import re

resp = requests.get("https://njdg.ecourts.gov.in/")

soup = BeautifulSoup(resp.content, "html.parser")
script_tags = soup.find_all('script', {'type': 'text/javascript'})
for script in script_tags:
    if script.string and 'Less than one year' in script.string:
        html_content =  script.string
        break
soup = BeautifulSoup(html_content, 'html.parser')
script_content = soup.get_text()
pending_agewise_values = re.findall(r'pendingAgewiseBarChart\(\s*\'[^\']+\',\s*\'([^\']+)\',\s*\'([^\']+)\',', script_content)
if pending_agewise_values:
    first_set = pending_agewise_values[0][0].split('~')
    second_set = pending_agewise_values[0][1].split('~')
    print("Pending Agewise Numbers (Civil): ", first_set)  # First set of values
    print("Pending Agewise Numbers (Criminal): ", second_set)  # Second set of values

# Output:
Civil = []
Criminal = []
i=0
j=0
index = ['Less than 1 year','1-3 years','3-5 years','5-10 years','10-20 years']
for cases in first_set:
    Civil.append((index[i],cases))
    i+=1
for cases in second_set:
    Criminal.append((index[j],cases))
    j+=1
print(Civil)
print(Criminal)
    
