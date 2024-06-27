from fastapi import FastAPI
from typing import List
from fastapi import WebSocket,WebSocketException,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)





class websockets_manager:
    def __inti__(self):
        self.active_connections: List[WebSocket] = []
    async def connect(self,socket:WebSocket):
        await socket.accept()
        self.active_connections.append(socket)
    
    def disconnect(self,socket:WebSocket):
        self.active_connections.remove(socket)
    
    async def send_personal_message(self,message:str,socket:WebSocket):
        await socket.send_text(message)
    
    async def broadcast(self,mess:str):
        for conn in self.active_connections:
            await conn.send_text(mess)

manager = websockets_manager()


@app.get("/")
def home():
    return "welcome home"


@app.websocket('/ws/{client_id}')
async def connect_endpoints(socket:WebSocket,client_id:int):
    await manager.connect(socket)
    now = datetime.now()
    curr = now.strftime("%H:%M")
    try:
        while True:
            data = await socket.receive_text
            mess = {
                'time':curr,
                'client_id':client_id,
                'message': data
            }
            await manager.broadcast(json.dumps(mess)) 

    except WebSocketDisconnect :
        manager.disconnect(socket)
        mess = {
            'time':curr,
            'client_id':client_id,
            'message':"offline connect latter",
        }
        await manager.broadcast(json.dumps(mess))