from passlib.context import CryptContext
import os
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Users
from dotenv import load_dotenv

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class HashVerifyPassword:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(secret=password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(secret=password, hash=hashed_password)


class JWT:
    def __init__(self):
        self.SECRET = os.getenv("SECRET")
        self.ALGORITHM = os.getenv("ALGORITHM")

    def jwt_encode(self, payload: dict) -> str:
        encoded_str = jwt.encode(
            payload=payload, key=self.SECRET, algorithm=self.ALGORITHM
        )
        return encoded_str

    def jwt_decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.SECRET, [self.ALGORITHM]
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": str(error)},
            )
        else:
            return payload


def verify_user(email: str, password: str, db: Session) -> Users:
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid credentials, check the username and password."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = user.password
    if not HashVerifyPassword().verify_password(
        password=password, hashed_password=hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid credentials, check the username and password."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_user(token: str = Depends(oauth_scheme)) -> dict:
    payload = JWT().jwt_decode(token=token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid credentials, check the username and password."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
