import requests
from bs4 import BeautifulSoup

# Make a request to the webpage
url = 'https://njdg.ecourts.gov.in/njdg_v3/'
response = requests.get(url)

# Parse the page content
soup = BeautifulSoup(response.text, 'html.parser')

# Scrape all 'span' elements with the class 'h4'
element_a = soup.find_all('span', class_='h4')
print(f"Total elements found: {len(element_a)}")

# Loop through all elements to check if they contain an 'a' tag with an 'onclick' attribute
instituted_in_last_month = set()
disposal_in_last_month = set()
listed_today = set()
undated = set()
excessive_dated = set()
cases_filled_by_women = set()
cases_filled_by_senior_citizens = set()
contested_cases = set()
uncontested_cases = set()
for element in element_a:
    # Check if the 'span' contains an 'a' tag
    link = element.find('a')
    if link and link.has_attr('onclick'):
        # Print the 'onclick' attribute and the text inside the 'a' tag
        if link['onclick'] == "fetchStateData('ins',2);":
            instituted_in_last_month.add(('Civil' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('ins',1);":
            instituted_in_last_month.add(('Criminal' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('ins',3);":
            instituted_in_last_month.add(('Civil & Criminal' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('disp',2);":
            disposal_in_last_month.add(('Civil' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('disp',3);":
            disposal_in_last_month.add(('Criminal' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('disp',1);":
            disposal_in_last_month.add(('Civil & Criminal' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('listed','2')":
            listed_today.add(('Civil' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('listed','3')":
            listed_today.add(('Criminal' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('listed','1')":
            listed_today.add(('Civil & Criminal' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('undated','2')":
            undated.add(('Civil' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('undated','3')":
            undated.add(('Criminal' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('undated','1')":
            undated.add(('Civil & Criminal' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('excessive','2')":
            excessive_dated.add(('Civil' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('excessive','3')":
            excessive_dated.add(('Criminal' , link.text.strip()))
        elif link['onclick'] == "javascript:getAlertData('excessive','1')":
            excessive_dated.add(('Civil & Criminal' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('women',2);":
            cases_filled_by_women.add(('Civil' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('women',3);":
            cases_filled_by_women.add(('Criminal' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('women',1);":
            cases_filled_by_women.add(('Civil & Criminal' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('citizen',2);":
            cases_filled_by_senior_citizens.add(('Civil' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('citizen',3);":
            cases_filled_by_senior_citizens.add(('Criminal' , link.text.strip()))
        elif link['onclick'] == "fetchStateData('citizen',1);":
            cases_filled_by_senior_citizens.add(('Civil & Criminal' , link.text.strip()))  
            
tables = soup.find_all('table')

# Loop through each table to find the span elements with class 'h4'
k=0

for table in tables:
    spans = table.find_all('span', class_='h4')
    
    for span in spans:
        if k==21:
            contested_cases.add(('Civil' , span.text.strip()))
        elif k==22:
            contested_cases.add(('Criminal' , span.text.strip()))
        elif k==23:
            contested_cases.add(('Civil & Criminal' , span.text.strip()))
        elif k==24:
            uncontested_cases.add(('Civil' , span.text.strip()))
        elif k==25:
            uncontested_cases.add(('Criminal' , span.text.strip()))
        elif k==26:
            uncontested_cases.add(('Civil & Criminal' , span.text.strip()))
        k+=1
         
print(instituted_in_last_month)
print(disposal_in_last_month)
print(listed_today)
print(undated)
print(excessive_dated)
print(cases_filled_by_women)
print(cases_filled_by_senior_citizens)
print(contested_cases)
print(uncontested_cases)