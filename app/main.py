from fastapi import FastAPI, HTTPException
import requests
import xml.etree.ElementTree as ET
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#'static'폴더를 '/static'경로에 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

class Drug(BaseModel):
    itemName: str
    type: str = 'json'
class Vaccine(BaseModel):
    PRDLST_NM: str
    type: str = 'json'
class Dosage(BaseModel):
    DRUG_CPNT_KOR_NM: str
    type: str = 'json'
class RareDrug(BaseModel):
    PRDT_NM: str
    type: str = 'json'
class Essential(BaseModel):
    type: str = 'json'
class Disease(BaseModel):
    znCd: str
    type: str = 'json'

class PharmacyInfo(BaseModel):
    Q0: str
    Q1: str

class HospitalInfo(BaseModel):
    sidoCd: str
    sgguCd: str
    emdongNm: str

@app.post("/drug")
def fetch_drug_info(query: Drug):
    url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList?serviceKey=ccGlKVP4vK6%2FVd8U3ePooH6zq6w%2BEFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA%3D%3D&type=json'
    params ={
        'itemName': query.itemName,
        'type' : query.type
    }
    response = requests.get(url, params=params)
    data = response.json()
    return JSONResponse(content=data)

@app.post("/vaccine")
def fetch_vaccine_info(query: Vaccine):
    url = 'http://apis.data.go.kr/1471000/IcdVacinDrugPrdtInfoService/getIcdVacinDrugPrdtInfo?serviceKey=ccGlKVP4vK6%2FVd8U3ePooH6zq6w%2BEFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA%3D%3D&type=json'
    params ={
        'PRDLST_NM' : query.PRDLST_NM,
        'type' : query.type
    }
    response = requests.get(url, params=params)
    data = response.json()
    return JSONResponse(content=data)

@app.post("/dosage")
def fetch_dosage_info(query: Dosage):
    url = 'http://apis.data.go.kr/1471000/DayMaxDosgQyByIngdService/getDayMaxDosgQyByIngdInq?serviceKey=ccGlKVP4vK6%2FVd8U3ePooH6zq6w%2BEFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA%3D%3D&type=json'
    params ={
        'DRUG_CPNT_KOR_NM' : query.DRUG_CPNT_KOR_NM,
        'type' : query.type
    }
    response = requests.get(url, params=params)
    data = response.json()
    return JSONResponse(content=data)

@app.post("/raredrug")
def fetch_rare_drug_info(query: RareDrug):
    url = 'http://apis.data.go.kr/1471000/RareDrugCpntService01/getRareDrugCpntInq01'
    params ={
        'serviceKey' : 'ccGlKVP4vK6%2FVd8U3ePooH6zq6w%2BEFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA%3D%3D',
        'PRDT_NM' : query.PRDT_NM,
        'type' : query.type
    }
    response = requests.get(url, params=params)
    data = response.json()
    return JSONResponse(content=data)

@app.get("/essential")
def get_essential_info(query: Essential):
    url = 'http://apis.data.go.kr/1471000/SafeStadDrugService/getSafeStadDrugInq'
    params ={
        'serviceKey' : 'ccGlKVP4vK6%2FVd8U3ePooH6zq6w%2BEFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA%3D%3D',
        'type' : query.type
    }
    response = requests.get(url, params=params)
    data = response.json()
    return JSONResponse(content=data)

@app.post("/diseaseinfo")
def fetch_disease_info(query: Disease):
    url = 'http://apis.data.go.kr/B550928/dissForecastInfoSvc/getDissForecastInfo?serviceKey=ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==&type=json'
    params ={
        'znCd' : query.znCd,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return JSONResponse(content=data)

@app.post("/getPharmacyInfo")
async def get_pharmacy_info(query: PharmacyInfo):
    url = "http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'Q0': query.Q0,
        'Q1': query.Q1
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return {"error": "API 요청 실패"}, response.status_code
    
    root = ET.fromstring(response.content)
    pharmacy_list = []
    
    for item in root.findall('.//item'):
        pharmacy_info = {
            "institution_name": item.find('dutyName').text if item.find('dutyName') is not None else "",
            "address": item.find('dutyAddr').text if item.find('dutyAddr') is not None else "",
            "remarks": item.find('dutyEtc').text if item.find('dutyEtc') is not None else "",
            "phone_number": item.find('dutyTel1').text if item.find('dutyTel1') is not None else "",
            "hours_1": item.find('dutyTime1s').text if item.find('dutyTime1s') is not None else "",
            "hours_2": item.find('dutyTime1c').text if item.find('dutyTime1c') is not None else "",
            "hours_3": item.find('dutyTime2s').text if item.find('dutyTime2s') is not None else "",
            "hours_4": item.find('dutyTime2c').text if item.find('dutyTime2c') is not None else "",           
            "hours_5": item.find('dutyTime3s').text if item.find('dutyTime3s') is not None else "",
            "hours_6": item.find('dutyTime3c').text if item.find('dutyTime3c') is not None else "",                    
            "hours_7": item.find('dutyTime4s').text if item.find('dutyTime4s') is not None else "",         
            "hours_8": item.find('dutyTime4c').text if item.find('dutyTime4c') is not None else "",          
            "hours_9": item.find('dutyTime5s').text if item.find('dutyTime5s') is not None else "",           
            "hours_10": item.find('dutyTime5c').text if item.find('dutyTime5c') is not None else "",          
            "hours_11": item.find('dutyTime6s').text if item.find('dutyTime6s') is not None else "",       
            "hours_12": item.find('dutyTime6c').text if item.find('dutyTime6c') is not None else "",
            "hours_13": item.find('dutyTime7s').text if item.find('dutyTime7c') is not None else "",
            "hours_14": item.find('dutyTime7c').text if item.find('dutyTime7c') is not None else "",
            "hours_15": item.find('dutyTime8s').text if item.find('dutyTime8s') is not None else "",
            "hours_16": item.find('dutyTime8c').text if item.find('dutyTime8c') is not None else "",            
            "institution_id": item.find('hpid').text if item.find('hpid') is not None else ""
        }
        pharmacy_list.append(pharmacy_info)
    
    return JSONResponse(content=pharmacy_list)

@app.post("/hospitalinfo")
async def get_hospital_info(query: HospitalInfo):
    url = "https://opendata.hira.or.kr/op/opc/selectColumnCodeList.do"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'sidoCd': query.sidoCd,
        'sgguCd': query.sgguCd,
        'emdongNm' : query.emdongNm
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return {"error": "API 요청 실패"}, response.status_code
    
    root = ET.fromstring(response.content)
    hospital_list = []
    
    for item in root.findall('.//item'):
        hospital_info = {
            "yadmNm": item.find('yadmNm').text if item.find('yadmNm') is not None else "",
            "addr": item.find('addr').text if item.find('addr') is not None else "",
            "hospUrl": item.find('hospUrl').text if item.find('hospUrl') is not None else "",
            "telno": item.find('telno').text if item.find('telno') is not None else "",       
            "clCdNm": item.find('clCdNm').text if item.find('clCdNm') is not None else "",            
            "cmdcResdntCnt": item.find('cmdcResdntCnt').text if item.find('cmdcResdntCnt') is not None else "",
            "cmdcSdrCnt": item.find('cmdcSdrCnt').text if item.find('cmdcSdrCnt') is not None else "",
            "pnursCnt": item.find('pnursCnt').text if item.find('pnursCnt') is not None else "",
            "distance": item.find('distance').text if item.find('distance') is not None else "",
            "detyGdrCnt": item.find('detyGdrCnt').text if item.find('detyGdrCnt') is not None else "",
            "detyIntnCnt": item.find('detyIntnCnt').text if item.find('detyIntnCnt') is not None else "",
            "detyResdntCnt": item.find('detyResdntCnt').text if item.find('detyResdntCnt') is not None else "",
            "detySdrCnt": item.find('detySdrCnt').text if item.find('detySdrCnt') is not None else "",           
            "cmdcGdrCnt": item.find('cmdcGdrCnt').text if item.find('cmdcGdrCnt') is not None else "",
            "cmdcIntnCnt": item.find('cmdcIntnCnt').text if item.find('cmdcIntnCnt') is not None else "",                    
            "mdeptResdntCnt": item.find('mdeptResdntCnt').text if item.find('mdeptResdntCnt') is not None else "",         
            "drTotCnt": item.find('drTotCnt').text if item.find('drTotCnt') is not None else "",          
            "mdeptGdrCnt": item.find('mdeptGdrCnt').text if item.find('mdeptGdrCnt') is not None else "",           
            "mdeptIntnCnt": item.find('mdeptIntnCnt').text if item.find('mdeptIntnCnt') is not None else "",          
            "mdeptSdrCnt": item.find('mdeptSdrCnt').text if item.find('mdeptSdrCnt') is not None else "",            
        }
        hospital_list.append(hospital_info)
    
    return JSONResponse(content=hospital_list)