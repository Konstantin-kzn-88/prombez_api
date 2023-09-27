import sys

sys.path.append('../..')

from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, APIRouter
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user
from fastapi.responses import HTMLResponse

from calculation_methods import calc_fireball

router = APIRouter(
    prefix='/fireball',
    tags=['fireball'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/mchs_404_fireball', response_class=HTMLResponse)
async def get_fireball(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/mchs_404_fireball_form.html', {'request': request, 'user': user})


@router.post('/mchs_404_fireball', response_class=HTMLResponse)
async def post_fireball(request: Request,
                        mass: str = Form(...), ef: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    # 1. Получим класс для расчета шара
    fireball_unit = calc_fireball.Fireball()
    # 2. Получим зоны для большой таблицы (не классифицированные)
    zone_array = fireball_unit.fireball_array(float(mass), float(ef))
    # Преобразование к виду [(r, q, Q, pr, q_vp),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2], zone_array[3], zone_array[4])
    zipped_list = list(zipped_values)
    # 3. Получим зоны классифицированные
    zone_cls_array = fireball_unit.termal_class_zone(float(mass), float(ef))

    plot_div_fireball_q = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[1], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="Расстояние, м"),
                         yaxis=dict(title="Интенсивность теплового излучения, кВт/м2"))
    },
        output_type='div', show_link=False, link_text="")

    plot_div_fireball_Q = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[2], line=dict(color='#6072fb', width=3))],
        "layout": Layout(xaxis=dict(title="Расстояние, м"), yaxis=dict(title="Доза теплового излучения, кДж/м2"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/mchs_404_fireball_result.html', {'request': request,
                                                                                 'user': user,
                                                                                 'zone_array': zipped_list,
                                                                                 'zone_cls_array': zone_cls_array,
                                                                                 'plot_div_fireball_q': plot_div_fireball_q,
                                                                                 'plot_div_fireball_Q': plot_div_fireball_Q,
                                                                                 'calc_data': (mass, ef)
                                                                                 })
