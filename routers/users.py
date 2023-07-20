import sys

sys.path.append('..')

from fastapi import Depends, APIRouter
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
# from .auth import get_current_user, get_user_exception, verify_password, get_password_hash

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'descrition': 'Not found'}}

)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    user_name: str
    password: str
    new_password: str


@router.get('/')
async def read_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()