import random
import shelve
from typing import Optional

from fastapi import FastAPI, Header
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from enums import ACCOUNT_TYPES

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = shelve.open("db")


@app.get("/")
async def root():
    return {"message": "Welcome to InsuranceHive"}


class RegistrationDetails(BaseModel):
    username: str
    betaUser: Optional[bool] = False
    accountType: Optional[str] = None


@app.post("/register")
async def register(registration_details: RegistrationDetails):
    if registration_details.username in db:
        return {"message": "Account already exists"}
    registration_details.accountType = random.choice(ACCOUNT_TYPES)
    db[registration_details.username] = registration_details
    return registration_details


class LoginDetails(BaseModel):
    username: str


@app.post("/login")
async def login(login_details: LoginDetails):
    if login_details.username not in db:
        return {"error": "User does not exist."}
    return db[login_details.username]


@app.get("/me")
async def me(authorization: Optional[str] = Header(None)):
    if authorization:
        return db[authorization]
    return {"username": None, "betaUser": None, "accountType": None}
