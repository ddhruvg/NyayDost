import re
import requests
import os
import openai
from dotenv import load_dotenv
load_dotenv()
from bs4 import BeautifulSoup
import googleapiclient.discovery
import json



apikey = os.getenv('OPENAI_API_KEY')
youtube_api=os.getenv('GOOGLE_YOUTUBE_API')

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=apikey
)

def llm_invok(system_prompt, msg):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": msg,
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    return chat_completion.choices[0].message.content

# Function to get case status using the given diary number and year
def caseStatus(diary_no, diary_year):
    url = f"https://www.sci.gov.in/wp-admin/admin-ajax.php"
    params = {
        'diary_no': diary_no,
        'diary_year': diary_year,
        'tab_name': 'case_details',
        'action': 'get_case_details',
        'es_ajax_request': '1',
        'language': 'en'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # print(response.json()['data'])
        return response.json()['data']  # Assuming the response is in JSON format
    else:
        return f"Error: {response.status_code}"

# Function to detect diary number and year in the user's message
def detect_diary_no_and_year(msg):
    # Regex to find a 4-5 digit diary number and a 4-digit year
    diary_no_match = re.search(r"\b(\d{4,5})\b", msg)
    diary_year_match = re.search(r"\b(20\d{2})\b", msg)
    
    if diary_no_match and diary_year_match:
        diary_no = diary_no_match.group(1)
        diary_year = diary_year_match.group(1)
        return diary_no, diary_year
    else:
        return None, None

# Function to detect if the user is asking for case status
def is_case_status_query(msg):
    case_keywords = ['case status', 'diary number', 'case details', 'case information', 'current case status']
    return any(keyword in msg.lower() for keyword in case_keywords)

# Function to summarize the case status
def summarize_case_status(diary_no, diary_year):
    case_data = caseStatus(diary_no, diary_year)
    system_prompt = "Summarize the case"
    return llm_invok(system_prompt, case_data)

# Function to detect if user is asking for case status in general and respond accordingly
def my_case_status(msg):
    # Check if the user is asking for a case status
    if "can you give" in msg.lower() and "case status" in msg.lower():
        return "Yes, I can provide your case status. Please provide the diary number and the diary year."
    
    # Check if the message contains diary number and year already
    diary_no, diary_year = detect_diary_no_and_year(msg)
    if diary_no and diary_year:
        system_prompt = summarize_case_status(diary_no, diary_year)
        return system_prompt
    else:
        return "I couldn't detect both the diary number and year. Please provide both to continue."
    

def Age_Wise_Pending_Data(msg):
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

    response = llm_invok("Summarize the Age wise pending data according to the message ",f"Age wise pending data is {Civil} of Civil cases and {Criminal} of criminal cases ",msg)
    return response

def Card_Header():
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
    response = llm_invok("Summarize the Age wise pending data ",f"Age wise pending data is {Civil} of Civil cases and {Criminal} of criminal cases ") # need to change the msg and system_prompt
    return response

def Features():
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
    response = llm_invok("Summarize the Age wise pending data ",f"Age wise pending data is {Civil} of Civil cases and {Criminal} of criminal cases ") # need to change the msg and system_prompt
    return response


def Traffic_Violation_and_E_Challan(msg):
    system_prompt = 'answer the following msg according to the given paragraph : The Motor Vehicles (Amendment) Act, 2019, introduced a comprehensive update to traffic laws and penalties in India, aiming to enhance road safety and encourage compliance. Effective from September 1, 2019, in Delhi, this Act enforces strict penalties for various violations. All vehicle owners must have a valid Driving Licence, insurance, and Registration Certificate (RC) when driving. Common violations, such as overspeeding, red light jumping, dangerous driving, using a mobile phone while driving, and driving without a seatbelt, attract fines ranging from Rs. 500 to Rs. 10,000, with more severe punishments, including imprisonment, for offenses like driving under the influence of alcohol. Specific rules apply to four-wheelers and two-wheelers alike: four-wheeler drivers must ensure that all occupants wear seatbelts, follow lane discipline, and park only in permitted zones, while two-wheeler riders are required to wear helmets (including pillion riders), avoid triple riding, and adhere to speed limits. Soft copies of required documents are acceptable via the DigiLocker app, providing ease of access and compliance. For penalties related to juvenile driving offenses, fines can reach Rs. 25,000, with further legal repercussions. Those fined for violations can conveniently pay their challans online through the e-Challan portal: echallan.parivahan.gov.in.'
    return llm_invok(system_prompt,msg)

def Ecourt_mobile_services_app(msg):
    system_prompt = """answer the following msg according to the given paragraph and return the app link for user : The eCourts Services app, developed by the National Informatics Centre under the guidance of the eCommittee of the Supreme Court of India, provides essential judicial information and services to the public. It allows users to easily access case details, check case status, and view judgments across all courts in India. Key features include locating nearby courts, tracking case hearings, obtaining case details like case history, orders, and judgments, as well as receiving automatic case alerts. The app aims to improve transparency, streamline access to judicial information, and reduce the need for physical visits to courts.

You can download the eCourts Services app here: https://play.google.com/store/apps/details?id=com.servicesinfo.ecourtservices&hl=en_US for Android users.

For iOS users, search for "eCourts Services" in the Apple App Store"""

    return llm_invok(system_prompt,msg)

def Fast_Track_Court_services(msg):
    system_prompt = """answer the following msg according to the given paragraph : Fast Track Special Courts (FTSCs) were established in India to provide expedited handling of cases involving crimes against women and children, particularly under the Protection of Children from Sexual Offences (POCSO) Act, and cases of rape. Initiated by the Indian government as part of a centrally-sponsored scheme, these courts aim to reduce the judicial backlog and ensure swift justice for victims. FTSCs were set up in response to a growing demand for quicker legal processes in sensitive cases and are designed to function with dedicated resources, including specialized judges and staff, to handle cases exclusively related to these crimes.

The government allocated significant funding for FTSCs, with state governments encouraged to create more courts based on local requirements. These courts work on strict timelines, with a goal to conclude cases within 60 days from the charge sheet's filing, as mandated under the POCSO Act and Criminal Law (Amendment) Act, 2018. The introduction of FTSCs has contributed to reducing the pendency of cases, but challenges remain, including the need for adequate infrastructure, trained personnel, and sustained financial support to maintain the efficiency and effectiveness of these courts."""
    
    return llm_invok(system_prompt,msg)


def Queries_about_judge_appointment(msg):
    system_prompt =""" answer the following msg according to the given paragraph : For queries on Department of Justice (DoJ) divisions and judge appointments, here’s a detailed overview:

### 1. **Divisions of the Department of Justice (DoJ)**
   - **Judicial Reforms**: This division focuses on implementing reforms to improve judicial processes, including steps to reduce case pendency and enhance access to justice.
   - **National Judicial Infrastructure**: This division oversees the development and maintenance of judicial infrastructure, aiming to modernize court facilities and technology across the judiciary.
   - **Legal Aid and Access to Justice**: Responsible for providing free legal aid services to eligible citizens and improving access to justice, especially for marginalized communities.
   - **E-Governance and Digital Justice**: Supports the digital transformation of courts through initiatives like the eCourts project, which facilitates online services like eFiling, case status tracking, and digital hearings.

### 2. **Judge Appointments**
   - **Higher Judiciary (Supreme Court and High Courts)**: The process is largely managed by the **Collegium System**. For the Supreme Court, a five-member collegium (headed by the Chief Justice of India) makes recommendations, which are reviewed by the President of India. High Court judges are appointed based on recommendations from a three-member collegium.
   - **Lower Judiciary (District and Subordinate Courts)**: Appointments are managed by respective state judicial services, under the supervision of High Courts and state Public Service Commissions.
   - **Key Criteria**: For all levels, the selection emphasizes legal acumen, integrity, and impartiality, with recent initiatives aiming to increase transparency and inclusivity in the appointment process.

Each of these areas is critical in maintaining a robust, fair, and accessible judicial system. Let me know if you need more details on any specific division or procedure!"""

    return llm_invok(system_prompt,msg)


def Tele_Law_Services (msg):
    sys_prompt = """ answer the following msg according to the given paragraph :

TELE LAW Tele Law’, is aimed at facilitating delivery of legal advice through an expert panel of lawyers – stationed at the State Legal Services Authorities (SLSA). The project would connect lawyers with clients through video conferencing facilities.

Para legal volunteers will be available for 10 days a month at 500 Common Service Centres in the first phase.

Number of volunteers to be hired are around 1000 and special platform for women and growing women entrepreneurship will be putforth.

The scheme although has a optimum performance objective to achieve as a part of Access to Justice programme but, number of centres and volunteers are negligible amount to get the work going. The scale of matters pending before the court, matters filed everyday are huge in number. To start with at this level, is nothing but an act to jeopardise it in future years to come. Availability of volunteers for 10 days a month is illadviced at the stages of policy making.

Definitely, a technology driven legal activism policy like this, has to go through a lot of hustle and rustle. It will be interesting to see how successful it will get in guiding the way through in future."""

    return llm_invok(sys_prompt,msg)


def channel_id(channel_id):
    # Define API service name and version
    api_service_name = "youtube"
    api_version = "v3"
    api_key = youtube_api  # Replace with your API key

    # Create a YouTube client
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    # Make a request to the YouTube API
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,  # Use the passed channel ID
        eventType="live",
        maxResults=25,
        q="live",
        type="video"
    )
    
    # Execute the request and get the response
    result = request.execute()
    video_playlist = {}
    for item in result['items']:
        video_title = item['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        video_playlist[video_title] = video_url
    
    # Return the response
    return video_playlist



def Get_Live_Stream(msg):
    """
    Function to check for live streams from Indian courts based on user input.
    Uses llm_invok to determine which court is being asked about.
    """

    # System prompt to extract court name from the user message
    sys_prompt = """You are a helpful assistant that extracts the name of the court mentioned in the user's message. 
    The courts to look for include:
    - Supreme Court of India
    - Gujarat High Court
    - Karnataka High Court
    - Delhi High Court
    - Bombay High Court
    - Patna High Court
    - Gauhati High Court
    - Calcutta High Court
    - Madras High Court
    - Allahabad High Court
    - Andhra Pradesh High Court
    - Chattisgarh High Court
    - Himachal Pradesh High Court
    - Jammu & Kashmir High Court
    - Jharkhand High Court
    - Kerala High Court
    - Madhya Pradesh High Court
    - Meghalaya High Court
    - Orissa High Court
    - Punjab & Haryana High Court
    - Rajasthan High Court
    - Sikkim High Court
    - Telangana High Court
    - Tripura High Court
    - Uttarakhand High Court
    
    Please extract the court name from the following message: "{msg}"
    """

    # Use llm_invok to get the court name from the user's message
    court_name = llm_invok(sys_prompt, msg)

    # Check if a court name was returned
    if court_name:
        # Assuming you have a mapping of court names to their channel IDs
        court_id_map = {
            "Supreme Court of India": "UCNPfqOXB7cg2jrNerfWzlVQ",
            "Gujarat High Court": "UCZoBFtdYPm8tBfGDzf4jsUg",
            "Karnataka High Court": "UCIFBFfssHWEZRAwL0zXGJBw",
            "Delhi High Court": "UCmieM-QYWkp91Av-Y2CakYQ",
            "Bombay High Court": "UCO-ztnBfSTHWlQHD2ZFLyiQ",
            "Patna High Court": "UCvb5s5UdLjpaiDpBeaCxVEw",
            "Gauhati High Court": "UCmGt6PmPpCzPmOgE-MWJLug",
            "Calcutta High Court": "UCZrLnL_M6pfY53a9mKvtmdA",
            "Madras High Court": "UCA6M8dZblz6URMiWdBK6uOg",
            "Allahabad High Court": "UCMFYbZwJkDIYRGqExYHh27A",
            "Andhra Pradesh High Court": "UCn5q10z3Q2VdgfuKQwfSS8w",
            "Chattisgarh High Court": "UCW8643pYsVLZMN4CbcSeTHw",
            "Himachal Pradesh High Court": "UCsnwxgawZ-Jp-_4sWl8UTwA",
            "Jammu & Kashmir High Court": "UCHgTFDLsPQMDt_Y7kHkeKfw",
            "Jharkhand High Court": "UC43OwYFDEuS8OrK_PSIabSg",
            "Kerala High Court": "UCONqfqsw_DX8A4BALysSYlg",
            "Madhya Pradesh High Court": "UCCIVFftzmBqzBKoijOmIl1A",
            "Meghalaya High Court": "UCAlulU0MrUQkOLQzS_Trf8Q",
            "Orissa High Court": "UCtTgN30THhZfQ6sQ_v3KBHQ",
            "Punjab & Haryana High Court": "UCvSsuoGMuTNqz26dxVhYzqQ",
            "Rajasthan High Court": "UCMOPtsAY1BmFJbyX0VP9hVg",
            "Sikkim High Court": "UCM0TYJJWZToW02_sQ85x0Qg",
            "Telangana High Court": "UC2t0yf5X9OEktsdXTrUsK4w",
            "Tripura High Court": "UCsI5L97cCA3oYKmR-d-hR-Q",
            "Uttarakhand High Court": "UCG25XfkyzDDeTVYYJBcqisg"
        }

        channel_id = court_id_map.get(court_name.strip())
        
        if channel_id:
            video_playlist = channel_id(channel_id)  # Call the channel_id function with the detected channel ID
            if video_playlist:
                response = f"Here are the list of videos on {court_name} YouTube channel with live court case hearings:\n"
                response += "\n".join([f"{title}: {url}" for title, url in video_playlist.items()])
                return response
            else:
                return f"No live streams are currently available for {court_name}."
        else:
            return "Court not found in the channel ID mapping."
    else:
        return "No specific court mentioned in your request."
