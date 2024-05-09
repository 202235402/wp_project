from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#'static'폴더를 '/static'경로에 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

class Vaccine(BaseModel):
    service_key: str
    prd_lst_sn: str
    page_no: int = 1
    num_of_rows: int = 10
    type: str

@app.post("/vaccine/")
def fetch_vaccine_info(query: Vaccine):
    url = "http://apis.data.go.kr/1471000/IcdVacinDrugPrdtInfoService/getIcdVacinDrugPrdtInfo"
    params = {
        "ServiceKey": query.service_key,
        "PRDLST_SN": query.prd_lst_sn,
        "pageNo": query.page_no,
        "numOfRows": query.num_of_rows,
        "type": query.type
    }
    contents = requests.get(url, params=params)
    if contents.status_code != 200:
        raise HTTPException(status_code=404, detail="API request failed")
    return {"message": contents.json()}