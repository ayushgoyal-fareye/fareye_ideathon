from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,HttpUrl
from typing import List
from business_logic.data_logic import Data_Logic

router = APIRouter(
    prefix="/data",
    tags=["data"]
)

class Data(BaseModel):
    problem:str
    Screenshots:List[str]
    RCA:str
    solution:str

class Query(BaseModel):
    problem:str
    Screenshots:List[str]

@router.post("/add")
async def add_data(data:Data):
    datalogic:Data_Logic=Data_Logic()
    return datalogic.add_data(data)

@router.post("/response")
async def ans(query:Query):
    datalogic:Data_Logic=Data_Logic()
    return datalogic.search_results(query)
    


