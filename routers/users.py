import sys

sys.path.append('..')

from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .auth import get_current_user, verify_password, get_password_hash


templates = Jinja2Templates(directory='templates/')

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


@router.get('/user/{user_id}')
async def user_by_path(user_id: int, db: Session = Depends(get_db)):
    print('Here')
    user_model = db.query(models.User).filter(models.User.id == user_id).all()

    if user_model is not None:
        return user_model
    return 'Invalid user_id'


@router.get('/user/')
async def user_by_path(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is not None:
        return user_model
    return 'Invalid user_id'


@router.put('/user/password')
async def user_pass_word_change(user_verification: UserVerification,
                                user: dict = Depends(get_current_user),
                                                     db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail='Not Found')
    user_model = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    if user_model is not None:
        if user_verification.user_name == user_model.username and verify_password(user_verification.password, user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return 'Successful change password'

    return 'Invalid user or request'


@router.delete('/user')
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail='Not Found')
    user_model = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    if user_model is None:
        return 'Invalid user or request'
    db.query(models.User).filter(models.User.id == user.get('user_id')).delete()
    db.commit()
    return 'Delete succssesful'
