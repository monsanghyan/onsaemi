from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 받은 데이터를 구조화할 모델 정의
class SignalData(BaseModel):
    signal_type: str
    value: int

@app.post("/receive-signal")
async def receive_signal(data: SignalData):
    print(f"📥 신호 수신: {data.signal_type}, 값: {data.value}")
    return {"status": "received", "data": data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)