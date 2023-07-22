import sys

sys.path.append('..')

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/start_page',
    tags=['start_page'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates/')


@router.get('/')
async def start_page(request: Request):
    msg = 'Привет, вы успешно вошли!'
    return templates.TemplateResponse('start_page.html', {'request': request, 'msg': msg})
