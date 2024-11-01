from dotenv import load_dotenv
import os
import openai
from pydantic import BaseModel
from FunctionList import *
FunctionList = {
    "my_case_status": my_case_status,
    "Age_Wise_Pending_Data": Age_Wise_Pending_Data,
    "Get_Live_Stream": Get_Live_Stream,
    "Traffic_Violation_and_E_Challan": Traffic_Violation_and_E_Challan,
    "Ecourt_mobile_services_app": Ecourt_mobile_services_app,
    "Fast_Track_Court_services": Fast_Track_Court_services,
    "Queries_about_judge_appointment": Queries_about_judge_appointment,
    "Tele_Law_Services": Tele_Law_Services,
}# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
apikey = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=apikey
)
  # You can use other models as well
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

links = '''
[('https://www.youtube.com/watch?v=zYxUaNyiHH8', ''), ('https://www.youtube.com/watch?v=zYxUaNyiHH8', ''), ('https://www.youtube.com/watch?v=g8d5v_NCio4', ''), ('https://www.youtube.com/watch?v=g8d5v_NCio4', ''), ('https://www.youtube.com/watch?v=9bb6AMp2__0', ''), ('https://www.youtube.com/watch?v=9bb6AMp2__0', ''), ('https://www.youtube.com/watch?v=OGq4sFSGoNM', ''), ('https://www.youtube.com/watch?v=OGq4sFSGoNM', ''), ('https://www.youtube.com/watch?v=X_yoX3PkbHE', ''), ('https://www.youtube.com/watch?v=X_yoX3PkbHE', ''), ('https://www.youtube.com/watch?v=BKmv-n0yUYc', ''), ('https://www.youtube.com/watch?v=BKmv-n0yUYc', ''), ('https://www.youtube.com/watch?v=udjcKQMAyd0', ''), ('https://www.youtube.com/watch?v=udjcKQMAyd0', ''), ('https://www.youtube.com/watch?v=mniX7-rKvHk', ''), ('https://www.youtube.com/watch?v=mniX7-rKvHk', ''), ('https://www.youtube.com/watch?v=uOto7frzrCc', ''), ('https://www.youtube.com/watch?v=uOto7frzrCc', ''), ('https://www.youtube.com/watch?v=Nq2wYlWFucg', ''), ('https://www.youtube.com/watch?v=Nq2wYlWFucg', '')]
'''    


# Improved System Prompt
system_prompt = """You are an AI assistant specialized in providing legal and judicial information in India. 
I have a set of predefined functions to help users quickly access specific information:

1. Case Status Lookup (`my_case_status`):
   - Helps users find the status of a specific court case
   - Requires diary number and year
   - Provides a summary of the case details

2. Age-Wise Pending Data (`Age_Wise_Pending_Data`):
   - Provides a summary of pending cases categorized by age groups
   - Covers both civil and criminal cases

3. Traffic Violation Information (`Traffic_Violation_and_E_Challan`):
   - Explains current traffic rules and penalties
   - Provides information about e-challan portal
   - Helps users understand traffic violation consequences

4. eCourts Mobile Services (`Ecourt_mobile_services_app`):
   - Offers details about the eCourts Services mobile app
   - Provides download links for Android and iOS

5. Fast Track Court Services (`Fast_Track_Court_services`):
   - Explains the purpose and functioning of Fast Track Special Courts
   - Focuses on cases involving crimes against women and children

6. Judge Appointment Queries (`Queries_about_judge_appointment`):
   - Provides information about judicial appointments
   - Explains different divisions of the Department of Justice

7. Tele-Law Services (`Tele_Law_Services`):
   - Describes the Tele-Law project
   - Explains how legal advice is provided through video conferencing

8. Court Live Stream Lookup (`Get_Live_Stream`):
   - Attempts to find live streams for high courts or the Supreme Court

Return me the specifiacally saying only the function name which matches with the objective of message the most.
If a user's query does not match any of these specific functions return None"""


def query_answer(msg):
    """
    General query handling function.
    Uses the LLM to generate a response if no specific function matches.
    """
    # Call LLM to get the function name based on the user's message
    a = llm_invok(system_prompt, msg)

    if a == "None":
        return llm_invok("Answer the user question", msg)
    else:
        function_name = a.strip()  # Get the function name from LLM response

        # Remove any single quotes around the function name if present
        function_name = function_name.strip("'")

        try:
            # Ensure that the function name is valid and exists in FunctionList
            function_to_call = FunctionList.get(function_name)

            if function_to_call is not None:
                # If the function requires parameters, pass them accordingly
                return function_to_call(msg)  # Pass the necessary parameters
            else:
                return llm_invok("Answer to the user query",msg)
        except Exception as e:
            return f"An error occurred while calling the function: {str(e)}"

