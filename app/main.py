from fastapi import FastAPI, HTTPException
import requests
import xml.etree.ElementTree as ET
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#'static'폴더를 '/static'경로에 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

#의약 openAPI
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
    page_no: int = 1
    num_of_rows: int = 3
    type: str = 'json'

#질병 openAPI
class Disease(BaseModel):
    znCd: str


#약국 openAPI
class PharmacyInfo(BaseModel):
    Q0: str
    Q1: str
class Detail(BaseModel):
    vcnCd: str


#병원 정보 openAPI
class HospitalInfo(BaseModel):
    emdongNm: str
class Nursing(BaseModel):
    emdongNm: str
class ChildNight(BaseModel):
    emdongNm: str
class MedicalCode(BaseModel):
    dgsbjtCd: str
class Holiday(BaseModel):
    Q0: str
    Q1: str


#응급 의료 기관 openAPI
class EmergencyInfo(BaseModel):
    Q0: str
    Q1: str
class TraumaCenter(BaseModel):
    Q0: str
    Q1: str





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
async def fetch_rare_drug(query: RareDrug):
    url = "http://apis.data.go.kr/1471000/RareDrugCpntService01/getRareDrugCpntInq01"
    params = {
        'ServiceKey': 'ccGlKVP4vK6%2FVd8U3ePooH6zq6w%2BEFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA%3D%3D',
        'PRDT_NM': query.PRDT_NM,
        'type' : query.type
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    drug_list = []
    
    for item in root.findall('.//item'):
        drug_info = {
            "RARE_DRUG_NO": item.find('RARE_DRUG_NO').text if item.find('RARE_DRUG_NO') is not None else "",
            "MFTR_NM": item.find('MFTR_NM').text if item.find('MFTR_NM') is not None else "",
            "MDCT_NM": item.find('MDCT_NM').text if item.find('MDCT_NM') is not None else "",
            "TRGT_DISS_NM": item.find('TRGT_DISS_NM').text if item.find('TRGT_DISS_NM') is not None else "",
            "PRDT_NM": item.find('PRDT_NM').text if item.find('PRDT_NM') is not None else "",
            }
        drug_list.append(drug_info)
    
    return JSONResponse(content=drug_list)

@app.post("/essential")
def fetch_essential_info(query: Essential):
    url = 'http://apis.data.go.kr/1471000/SafeStadDrugService/getSafeStadDrugInq'
    params ={
        'serviceKey' : 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'page_no' : query.page_no,
        'num_of_rows' : query.num_of_rows,
        'type' : query.type
    }
    response = requests.get(url, params=params)
    data = response.json()
    return JSONResponse(content=data)


#질병 예측 정보
@app.post("/diseaseinfo")
async def fetch_disease_info(query: Disease):
    url = "http://apis.data.go.kr/B550928/dissForecastInfoSvc/getDissForecastInfo"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'znCd': query.znCd,
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    disease_list = []
    
    for item in root.findall('.//item'):
        disease_info = {
            "dissCd": item.find('dissCd').text if item.find('dissCd') is not None else "",
            "cnt": item.find('cnt').text if item.find('cnt') is not None else "",
            "risk": item.find('risk').text if item.find('risk') is not None else "",
            "dissRiskXpln": item.find('dissRiskXpln').text if item.find('dissRiskXpln') is not None else "",
            "dt": item.find('dt').text if item.find('dt') is not None else "",
            }
        disease_list.append(disease_info)
    
    return JSONResponse(content=disease_list)

#예방접종 감염병 정보
@app.post("/vaccination")
async def fetch_vaccination():
    url = "http://apis.data.go.kr/1790387/vcninfo/getCondVcnCd"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    disease_list = []
    
    for item in root.findall('.//item'):
        disease_info = {
            "cd": item.find('cd').text if item.find('cd') is not None else "",
            "cdNm": item.find('cdNm').text if item.find('cdNm') is not None else "",
            }
        disease_list.append(disease_info)
    
    return JSONResponse(content=disease_list)

@app.post("/detail")
async def fetch_detail(query: Detail):
    url = "http://apis.data.go.kr/1790387/vcninfo/getVcnInfo"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'vcnCd': query.vcnCd 
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    disease_list = []
    
    for item in root.findall('.//item'):
        disease_info = {
            "title": item.find('title').text if item.find('title') is not None else "",
            "message": item.find('message').text if item.find('message') is not None else ""
            }
        disease_list.append(disease_info)
    
    return JSONResponse(content=disease_list)


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

@app.post("/getHospitalInfo")
async def get_hospital_info(query: HospitalInfo):
    url = "http://apis.data.go.kr/B551182/hospInfoService1/getHospBasisList1"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'emdongNm': query.emdongNm
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    hospital_list = []
    
    for item in root.findall('.//item'):
        hospital_info = {            
            "yadmNm": item.find('yadmNm').text if item.find('yadmNm') is not None else "",
            "clCd": item.find('clCd').text if item.find('clCd') is not None else "",
            "clCdNm": item.find('clCdNm').text if item.find('clCdNm') is not None else "",
            "addr": item.find('addr').text if item.find('addr') is not None else "",
            "telno": item.find('telno').text if item.find('telno') is not None else "",
            "hospUrl": item.find('hospUrl').text if item.find('hospUrl') is not None else "",
            "drTotCnt": item.find('drTotCnt').text if item.find('drTotCnt') is not None else "",
            "mdeptGdrCnt": item.find('mdeptGdrCnt').text if item.find('mdeptGdrCnt') is not None else "",           
            "mdeptIntnCnt": item.find('mdeptIntnCnt').text if item.find('mdeptIntnCnt') is not None else "",
            "mdeptResdntCnt": item.find('mdeptResdntCnt').text if item.find('mdeptResdntCnt') is not None else "",                    
            "mdeptSdrCnt": item.find('mdeptSdrCnt').text if item.find('mdeptSdrCnt') is not None else "",         
            "detyGdrCnt": item.find('detyGdrCnt').text if item.find('detyGdrCnt') is not None else "",          
            "detyIntnCnt": item.find('detyIntnCnt').text if item.find('detyIntnCnt') is not None else "",           
            "detyResdntCnt": item.find('detyResdntCnt').text if item.find('detyResdntCnt') is not None else "",          
            "detySdrCnt": item.find('detySdrCnt').text if item.find('detySdrCnt') is not None else "",       
            "cmdcGdrCnt": item.find('cmdcGdrCnt').text if item.find('cmdcGdrCnt') is not None else "",
            "cmdcIntnCnt": item.find('cmdcIntnCnt').text if item.find('cmdcIntnCnt') is not None else "",
            "cmdcResdntCnt": item.find('cmdcResdntCnt').text if item.find('cmdcResdntCnt') is not None else "",
            "cmdcSdrCnt": item.find('cmdcSdrCnt').text if item.find('cmdcSdrCnt') is not None else "",
            }
        hospital_list.append(hospital_info)
    
    return JSONResponse(content=hospital_list)

#요양 병원 찾기
@app.post("/getNursing")
async def get_nursing(query: Nursing):
    url = "http://apis.data.go.kr/B551182/spclMdlrtHospInfoService1/getRcperHospList1"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'emdongNm': query.emdongNm
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    hospital_list = []
    
    for item in root.findall('.//item'):
        hospital_info = {
            "yadmNm": item.find('yadmNm').text if item.find('yadmNm') is not None else "",
            "clCdNm": item.find('clCdNm').text if item.find('clCdNm') is not None else "",
            "addr": item.find('addr').text if item.find('addr') is not None else "",
            "telno": item.find('telno').text if item.find('telno') is not None else "",
            "estbDd": item.find('estbDd').text if item.find('estbDd') is not None else "",
            }
        hospital_list.append(hospital_info)
    
    return JSONResponse(content=hospital_list)

#소아 야간 진료 병원
@app.post("/getChildNight")
async def get_childnight(query: ChildNight):
    url = "http://apis.data.go.kr/B551182/spclMdlrtHospInfoService1/getChildNightMdlrtList1"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'emdongNm': query.emdongNm
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    hospital_list = []
    
    for item in root.findall('.//item'):
        hospital_info = {
            "yadmNm": item.find('yadmNm').text if item.find('yadmNm') is not None else "",
            "clCdNm": item.find('clCdNm').text if item.find('clCdNm') is not None else "",
            "addr": item.find('addr').text if item.find('addr') is not None else "",
            "telno": item.find('telno').text if item.find('telno') is not None else "",
            "hospUrl": item.find('hospUrl').text if item.find('hospUrl') is not None else "",
            "estbDd": item.find('estbDd').text if item.find('estbDd') is not None else "",
            }
        hospital_list.append(hospital_info)
    
    return JSONResponse(content=hospital_list)

#진료과목별 병원 조회
@app.post("/getMedicalCode")
async def get_medicalcode(query: MedicalCode):
    url = "http://apis.data.go.kr/B551182/spclMdlrtHospInfoService1/getMdlrtSbjectList1"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'dgsbjtCd': query.dgsbjtCd
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    hospital_list = []
    
    for item in root.findall('.//item'):
        hospital_info = {
            "yadmNm": item.find('yadmNm').text if item.find('yadmNm') is not None else "",
            "clCdNm": item.find('clCdNm').text if item.find('clCdNm') is not None else "",
            "addr": item.find('addr').text if item.find('addr') is not None else "",
            "telno": item.find('telno').text if item.find('telno') is not None else "",
            "hospUrl": item.find('hospUrl').text if item.find('hospUrl') is not None else "",
            "estbDd": item.find('estbDd').text if item.find('estbDd') is not None else "",
            }
        hospital_list.append(hospital_info)
    
    return JSONResponse(content=hospital_list)

#명절 비상 진료 기관 조회
@app.post("/holiday")
async def get_holiday(query: Holiday):
    url = "http://apis.data.go.kr/B552657/HolidyEmgncClnicInsttInfoInqireService/getHolidyClnicPosblEgytInfoInqire"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'Q0': query.Q0,
        'Q1': query.Q1

    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    hospital_list = []
    
    for item in root.findall('.//item'):
        hospital_info = {
            "dutyName": item.find('dutyName').text if item.find('dutyName') is not None else "",
            "dutyAddr": item.find('dutyAddr').text if item.find('dutyAddr') is not None else "",
            "dutyDivName": item.find('dutyDivName').text if item.find('dutyDivName') is not None else "",
            "dutyTel1": item.find('dutyTel1').text if item.find('dutyTel1') is not None else "",
            "hpid": item.find('hpid').text if item.find('hpid') is not None else "",
            }
        hospital_list.append(hospital_info)
    
    return JSONResponse(content=hospital_list)

#응급 의료 정보 openAPI
@app.post("/getEmergencyInfo")
async def get_emergency_info(query: EmergencyInfo):
    url = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'Q0': query.Q0,
        'Q1': query.Q1,
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    emergency_list = []
    
    for item in root.findall('.//item'):
                emergency_info = {
                    "dutyName": item.find('dutyName').text if item.find('dutyName') is not None else "",
                    "hpid": item.find('hpid').text if item.find('hpid') is not None else "",
                    "dutyAddr": item.find('dutyAddr').text if item.find('dutyAddr') is not None else "",
                    "dutyEmcls": item.find('dutyEmcls').text if item.find('dutyEmcls') is not None else "",
                    "dutyEmclsName": item.find('dutyEmclsName').text if item.find('dutyEmclsName') is not None else "",
                    "dutyTel1": item.find('dutyTel1').text if item.find('dutyTel1') is not None else "",
                    "dutyTel3": item.find('dutyTel3').text if item.find('dutyTel3') is not None else "",
                }
                emergency_list.append(emergency_info)
    
    return JSONResponse(content=emergency_list)

@app.post("/getTraumaCenter")
async def get_trauma_center(query: TraumaCenter):
    url = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getStrmListInfoInqire"
    params = {
        'ServiceKey': 'ccGlKVP4vK6/Vd8U3ePooH6zq6w+EFSEHPTyq19WmAuLlAXB5krJemrGyDxvFw4GgejS2hZNV8r6qfMUMtpQgA==',
        'Q0': query.Q0,
        'Q1': query.Q1,
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="API request failed")
    
    root = ET.fromstring(response.content)
    emergency_list = []
    
    for item in root.findall('.//item'):
                emergency_info = {
                    "dutyName": item.find('dutyName').text if item.find('dutyName') is not None else "",
                    "hpid": item.find('hpid').text if item.find('hpid') is not None else "",
                    "dutyAddr": item.find('dutyAddr').text if item.find('dutyAddr') is not None else "",
                    "dutyEmcls": item.find('dutyEmcls').text if item.find('dutyEmcls') is not None else "",
                    "dutyEmclsName": item.find('dutyEmclsName').text if item.find('dutyEmclsName') is not None else "",
                    "dutyTel1": item.find('dutyTel1').text if item.find('dutyTel1') is not None else "",
                    "dutyTel3": item.find('dutyTel3').text if item.find('dutyTel3') is not None else "",
                }
                emergency_list.append(emergency_info)
    
    return JSONResponse(content=emergency_list)