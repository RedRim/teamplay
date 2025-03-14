from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/users")
async def get_users():
    return [
        {
            "id": 1,
            "name": "goida"
        }
    ]
