import requests
from bs4 import BeautifulSoup

# Make a request to the webpage
url = 'https://njdg.ecourts.gov.in/njdg_v3/'
response = requests.get(url)

# Parse the page content
soup = BeautifulSoup(response.text, 'html.parser')

# Scrape all 'span' elements with the class 'h4'
element_a = soup.find_all('span', class_='float-end h6 m-0 fw-bold')
print(len(element_a))
print(element_a)
civil_cases = element_a[0].text
criminal_cases = element_a[1].text
total_cases = element_a[2].text
pre_ligitation_trial = element_a[3].text
print(civil_cases)
print(criminal_cases)
print(total_cases)
print(pre_ligitation_trial)
