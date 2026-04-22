from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from pydantic import BaseModel
from api.data_router import router as data_router
from fastapi.middleware.cors import CORSMiddleware
import asyncio                                                                                                                                                                        
from fastapi import FastAPI, Request                                                                                                                                                  
from fastapi.responses import JSONResponse  
from business_logic.data_logic import Data_Logic            

app = FastAPI()

data_logic=Data_Logic()
app.include_router(data_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, use specific domains
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"status": "success", "message": "FastAPI is running!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"greeting": f"Hello, {name}!"}

async def call_llm(user_message: str) -> str:
      await asyncio.sleep(0)
      return data_logic.search_results(user_message)         

                                                                                                                            
   
                                                                                                                                                                                        
@app.post("/webhook")
async def webhook(request: Request):
      payload = await request.json()                                                                                                                                                    
   
                                                                                                                                                                    
      if "chat" in payload and "messagePayload" in payload.get("chat", {}):
          msg_payload = payload["chat"]["messagePayload"]
          message = msg_payload.get("message", {})                                                                                                                                      
      else:
                                                                                                                                                              
          if payload.get("type") != "MESSAGE":
              return JSONResponse(content={"status": "ignored"})
          message = payload.get("message", {})
                                                                                                                                                                                        
      user_message = (message.get("argumentText") or message.get("text", "")).strip()
                                                                                                                                                                                        
      if not user_message:
          return JSONResponse(content={"text": ""})

      response_text = await call_llm(user_message)                                                                                                                                      
      return JSONResponse(content={
          "hostAppDataAction": {                                                                                                                                                        
              "chatDataAction": {
                  "createMessageAction": {
                      "message": {"text": response_text}
                  }
              }
          }                                                                                                                                                                             
      })
