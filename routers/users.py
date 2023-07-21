import sys

sys.path.append('..')

from fastapi import Depends, APIRouter, HTTPException
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, EmailStr

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


class User(BaseModel):
    user_name: str
    email: EmailStr
    company_name: str
    first_name: str
    last_name: str
    phone_number: str
    hashed_password: str


@router.get('/')
async def read_all_users(db: Session = Depends(get_db)):
    '''Получение всех пользователей из таблицы USER базы данных '''
    return db.query(models.User).all()


@router.get('/{user_id}')
async def read_user_with_id(user_id: int, db: Session = Depends(get_db)):
    '''
    Получение пользователя по id
    :param user_id: - id пользователя из таблицы USER базы данных
    :param db: - параметр привязки к базе данных через функцию get_db
    :return: user_model - dict с полями из базы данных для конкретного пользователя
    '''
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is not None:
        return user_model
    raise http_exception()


@router.post('/')
async def create_user(user: User, db: Session = Depends(get_db)):
    '''

    :param user: class User с аттрибутами для полей базы данных
    :param db: - параметр привязки к базе данных через функцию get_db
    :return: - ответ о добавлении пользователя
    '''
    user_model = models.User()
    user_model.user_name = user.user_name
    user_model.email = user.email
    user_model.company_name = user.company_name
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.phone_number = user.phone_number
    user_model.hashed_password = user.hashed_password

    db.add(user_model)
    db.commit()

    return successful_response(201)


def http_exception():
    return HTTPException(status_code=404, detail="User not found")


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'successful'
    }
