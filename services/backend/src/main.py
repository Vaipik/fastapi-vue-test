from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.user import user_api

app = FastAPI(
    title="fastapi-vue",
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping_pong():
    return "pong"


app.include_router(user_api)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
