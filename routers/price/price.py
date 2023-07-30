import sys

sys.path.append('../..')

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user

router = APIRouter(
    prefix='/price',
    tags=['price'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/')
async def start_page(request: Request):
    user = await get_current_user(request)
    if user is None:
        return templates.TemplateResponse('price/price.html', {'request': request})
    return templates.TemplateResponse('price/price.html', {'request': request, 'user': user})
