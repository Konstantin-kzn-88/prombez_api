import sys

sys.path.append('../..')

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, APIRouter
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user
from fastapi.responses import HTMLResponse

from calculation_methods import calc_jet_fire

router = APIRouter(
    prefix='/jet_fire',
    tags=['jet_fire'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/mchs_404_jet_fire', response_class=HTMLResponse)
async def get_jet_fire(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/mchs_404_jet_fire_form.html', {'request': request, 'user': user})

@router.post('/mchs_404_jet_fire', response_class=HTMLResponse)
async def post_fireball(request: Request,
                        consumption: str = Form(...), type_sub: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    # 1. Получим класс для расчета
    jetfire_unit = calc_jet_fire.Torch()
    # 2. Получим зоны
    lenght, width = jetfire_unit.jetfire_size(float(consumption), int(type_sub))

    return templates.TemplateResponse('calc_app/mchs_404_jet_fire_result.html', {'request': request,
                                                                                 'user': user,
                                                                                 'consumption': float(consumption),
                                                                                 'calc_data': (lenght, width)
                                                                                 })