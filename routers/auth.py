import sys

sys.path.append('..')

from fastapi import Form, Depends, status, HTTPException, APIRouter, Request, Response
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

from starlette.responses import RedirectResponse

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

SECRET_KEY = 'A~#PLmx$TPkBE*hc1ckryg#sAngY@m'
ALGORITHM = 'HS256'

templates = Jinja2Templates(directory='templates/')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'user': 'Not autorized'}}

)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.user_name: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.user_name = form.get('email')
        self.password = form.get('password')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(user_name: str, password: str, db):
    user = db.query(models.User).filter(models.User.user_name == user_name).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(user_name: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {'sub': user_name, 'id': user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get('sub')
        user_id: str = payload.get('id')
        if user_name is None or user_id is None:
            logout(request)
        return {'user_name': user_name, 'user_id': user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail='User not found')


@router.post('/token')
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.user_name, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.user_name, user.id, expires_delta=token_expires)
    response.set_cookie(key='access_token', value=token, httponly=True)
    return True


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'successful'
    }


@router.get('/', response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/', response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response,
                                                            form_data=form,
                                                            db=db)

        if not validate_user_cookie:
            msg = 'Incorrect user_name or Login'
            return templates.TemplateResponse('login.html', {'request': request, 'msg': msg})
        return response
    except HTTPException:
        msg = 'Uncnow Error'
        return templates.TemplateResponse('login.html', {'request': request, 'msg': msg})


@router.get('/logout')
async def logout(request: Request):
    msg = 'Logout Successful'
    response = templates.TemplateResponse('login.html', {'request': request, 'msg': msg})
    response.delete_cookie(key='access_token')
    return response


@router.get('/register', response_class=HTMLResponse)
async def registration_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register', response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(...),
                        user_name: str = Form(...), first_name: str = Form(...),
                        last_name: str = Form(...), password: str = Form(...),
                        password2: str = Form(...), company_name: str = Form(...),
                        phone_number: str = Form(...),
                        db: Session = Depends(get_db)):
    validation1 = db.query(models.User).filter(models.User.user_name == user_name).first()
    validation2 = db.query(models.User).filter(models.User.email == email).first()

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = 'Invalid registration request'
        return templates.TemplateResponse('register.html', {'request': request, 'msg': msg})

    user_model = models.User()
    user_model.user_name = user_name
    user_model.email = email
    user_model.first_name = first_name
    user_model.last_name = last_name
    user_model.company_name = company_name
    user_model.phone_number = phone_number

    hash_password = get_password_hash(password)
    user_model.hashed_password = hash_password

    db.add(user_model)
    db.commit()

    msg = 'User successfully created'
    return templates.TemplateResponse('login.html', {'request': request, 'msg': msg})
