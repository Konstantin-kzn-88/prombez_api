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

from calculation_methods import calc_sp_explosion
from calculation_methods import calc_tvs_explosion

router = APIRouter(
    prefix='/explosion',
    tags=['explosion'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/sp1213130-2009', response_class=HTMLResponse)
async def get_explosion_sp(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/explosion_sp_form.html', {'request': request, 'user': user})


@router.post('/sp1213130-2009', response_class=HTMLResponse)
async def post_dev_edit(request: Request,
                        mass: str = Form(...), heat_of_combustion: str = Form(...),
                        z: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    # 1. Получим класс для расчета взрыва
    explosion_unit = calc_sp_explosion.Explosion()
    # 2. Получим зоны для большой таблицы (не классифицированные)
    zone_array = explosion_unit.explosion_array(float(mass), float(heat_of_combustion), float(z))
    # Преобразование к виду [(r, dP, i, pr, q_vp),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2], zone_array[3], zone_array[4])
    zipped_list = list(zipped_values)
    # 3. Получим зоны классифицированные
    zone_cls_array = explosion_unit.explosion_class_zone(float(mass), float(heat_of_combustion), float(z))

    plot_div_explosion = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[1], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="Расстояние, м"), yaxis=dict(title="Избыточное давление, кПа"))
    },
        output_type='div', show_link=False, link_text="")

    plot_div_impuls = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[2], line=dict(color='#6072fb', width=3))],
        "layout": Layout(xaxis=dict(title="Расстояние, м"), yaxis=dict(title="Импульс, Па*с"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/explosion_sp_result.html', {'request': request,
                                                                            'user': user,
                                                                            'zone_array': zipped_list,
                                                                            'zone_cls_array': zone_cls_array,
                                                                            'plot_div_explosion': plot_div_explosion,
                                                                            'plot_div_impuls': plot_div_impuls,
                                                                            'calc_data': (mass, heat_of_combustion, z)
                                                                            })


@router.get('/tvs', response_class=HTMLResponse)
async def get_explosion_tvs(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/explosion_tvs_form.html', {'request': request, 'user': user})


@router.post('/tvs', response_class=HTMLResponse)
async def post_dev_edit(request: Request,
                        mass: str = Form(...), heat_of_combustion: str = Form(...),
                        view_space: str = Form(...), class_substance: str = Form(...),
                        sigma: str = Form(...), energy_level: str = Form(...), ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    # 1. Получим класс для расчета взрыва
    explosion_unit = calc_tvs_explosion.Explosion()
    # 2. Получим зоны для большой таблицы (не классифицированные)
    zone_array = explosion_unit.explosion_array(int(class_substance), int(view_space), float(mass),
                                                float(heat_of_combustion), int(sigma), int(energy_level))
    # Преобразование к виду [(r, dP, i, pr, q_vp),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2], zone_array[3], zone_array[4])
    zipped_list = list(zipped_values)
    # 3. Получим зоны классифицированные
    zone_cls_array = explosion_unit.explosion_class_zone(int(class_substance), int(view_space), float(mass),
                                                float(heat_of_combustion), int(sigma), int(energy_level))


    plot_div_explosion = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[1], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="Расстояние, м"), yaxis=dict(title="Избыточное давление, кПа"))
    },
        output_type='div', show_link=False, link_text="")

    plot_div_impuls = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[2], line=dict(color='#6072fb', width=3))],
        "layout": Layout(xaxis=dict(title="Расстояние, м"), yaxis=dict(title="Импульс, Па*с"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/explosion_tvs_result.html', {'request': request,
                                                                             'user': user,
                                                                             'zone_array': zipped_list,
                                                                             'zone_cls_array': zone_cls_array,
                                                                             'plot_div_explosion': plot_div_explosion,
                                                                             'plot_div_impuls': plot_div_impuls,
                                                                             'calc_data': (
                                                                             class_substance, view_space, mass,
                                                                             heat_of_combustion, sigma, energy_level)
                                                                             })
