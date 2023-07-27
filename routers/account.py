import sys

sys.path.append('..')

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, Depends, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/account',
    tags=['account'],
    responses={404: {'descrition': 'Not found'}}

)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates/')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/')
async def get_account(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    return templates.TemplateResponse('account.html', {'request': request, 'user': user})


@router.post('/', response_class=HTMLResponse)
async def post_account(request: Request,
                            email: str = Form(...), user_name: str = Form(...),
                            company_name: str = Form(...), first_name: str = Form(...),
                            last_name: str = Form(...), phone_number: str = Form(...),
                            db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    user.email = email
    user.user_name = user_name
    user.company_name = company_name
    user.first_name = first_name
    user.last_name = last_name
    user.phone_number = phone_number

    db.add(user)
    db.commit()

    msg = 'Данные изменены'
    return templates.TemplateResponse('account.html', {'request': request, 'user': user, 'msg': msg})

@router.get('/delete/{user_id}')
async def delete_account(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    if user is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()

    msg = 'Пользователь успешно удален'
    response = templates.TemplateResponse('login.html', {'request': request, 'msg': msg})
    response.delete_cookie(key='access_token')
    return response

