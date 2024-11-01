from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from embedding import query_answer
from FunctionList import *

# Pydantic models for request validation
class QueryRequest(BaseModel):
    query: str

class CaseStatusRequest(BaseModel):
    diary_no: str
    diary_year: str

# Initialize FastAPI app
app = FastAPI(
    title="Legal Services API",
    description="API for accessing various legal and judicial services in India",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000"
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoints
@app.post("/query/", 
    response_model=dict,
    summary="General Query Endpoint",
    description="Process any general query about legal services")
async def process_query(item: QueryRequest):
    try:
        print("Hi")
        response = query_answer(item.query)
        print(type(response))
        print(response)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/case-status/", 
    response_model=dict,
    summary="Case Status Lookup",
    description="Get case status using diary number and year")
async def get_case_status(request: CaseStatusRequest):
    try:
        query = f"What is the case status with diary no {request.diary_no} and diary year {request.diary_year}"
        response = my_case_status(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/age-wise-pending/", 
    response_model=dict,
    summary="Age-wise Pending Cases",
    description="Get statistics about pending cases categorized by age")
async def get_age_wise_pending():
    try:
        response = Age_Wise_Pending_Data()
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/traffic-violations/", 
    response_model=dict,
    summary="Traffic Violations Information",
    description="Get information about traffic violations and e-challan system")
async def get_traffic_violations():
    try:
        response = Traffic_Violation_and_E_Challan("Summarise Traffic Violations possible in India and EChallan")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ecourt-services/", 
    response_model=dict,
    summary="eCourt Mobile Services",
    description="Get information about eCourt mobile services and app")
async def get_ecourt_services():
    try:
        response = Ecourt_mobile_services_app("Summarise Ecourt services in India")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/judge-appointments/", 
    response_model=dict,
    summary="Judge Appointment Information",
    description="Get information about judicial appointments and vacancies")
async def get_judge_appointments():
    try:
        response = Queries_about_judge_appointment("Tell me more about judges appointments and vacancy in supreme court")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tele-law/", 
    response_model=dict,
    summary="Tele-Law Services",
    description="Get information about Tele-Law services in India")
async def get_tele_law_services():
    try:
        response = Tele_Law_Services("Summarise Tele Law services in India")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/live-stream/", 
    response_model=dict,
    summary="Court Live Streams",
    description="Get information about available court live streams")
async def get_live_stream():
    try:
        response = Get_Live_Stream("Can we watch live stream of Court hearings?")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/", 
    response_model=dict,
    summary="Status",
    description="Server Status")
async def get_live_stream():
    try:
        
        return {"response": "NyayDost is ready to satisfy you !!!!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)