import sys

sys.path.append('..')


from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, Depends, APIRouter
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


@router.get('/account_info')
async def get_account_info(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    current_user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    return templates.TemplateResponse('account_info.html', {'request': request, 'current_user': current_user, 'user': user})


@router.post('/account_info', response_class=HTMLResponse)
async def post_account_info(request: Request, email: str = Form(...), db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    user_model = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    user_model.email = email
    db.add(user_model)
    db.commit()

    msg = 'Данные изменены'
    return templates.TemplateResponse('account_info.html', {'request': request, 'current_user': user_model, 'msg': msg})