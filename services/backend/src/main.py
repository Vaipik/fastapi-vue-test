from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from routes.user import user_api
from routes.auth import auth_api
from routes.note import notes_api
from schemas.user import UserAuthentication

app = FastAPI(
    title="fastapi-vue",
    version="0.0.1",
)
app.include_router(user_api)
app.include_router(auth_api)
app.include_router(notes_api)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get(
    "/ping",
    tags=["ping-pong"]
)
def ping_pong():
    return "pong"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return UserAuthentication(
        email=token + "fakedecoded",
    )


