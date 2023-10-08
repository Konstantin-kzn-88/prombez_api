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

from calculation_methods import calc_light_gas_disp
from calculation_methods import calc_heavy_gas_disp

router = APIRouter(
    prefix='/dispersion',
    tags=['dispersion'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/light_gas', response_class=HTMLResponse)
async def get_dispersion_light_gas(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/dispersion_light_gas_form.html', {'request': request, 'user': user})


@router.post('/light_gas', response_class=HTMLResponse)
async def post_dispersion_light_gas(request: Request,
                                    ambient_temperature: str = Form(...), cloud: str = Form(...),
                                    wind_speed: str = Form(...), is_night: str = Form(...),
                                    is_urban_area: str = Form(...), ejection_height: str = Form(...),
                                    gas_temperature: str = Form(...), gas_weight: str = Form(...),
                                    gas_flow: str = Form(...), closing_time: str = Form(...),
                                    molecular_weight: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    # 1. Получим класс для расчета взрыва
    if float(gas_temperature) <= float(ambient_temperature):
        gas_temperature = float(ambient_temperature) + 10  # температура газа не может быть меньше температуры воздуха
    dispertion_unit = calc_light_gas_disp.Source(float(ambient_temperature), float(cloud), float(wind_speed),
                                                 float(is_night), float(is_urban_area), float(ejection_height),
                                                 float(gas_temperature), float(gas_weight), float(gas_flow),
                                                 float(closing_time), float(molecular_weight))
    # 2. Получим зоны для большой таблицы (не классифицированные)
    zone_array = dispertion_unit.result()
    # Преобразование к виду [(dist, conc, dose),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2])
    zipped_list = list(zipped_values)

    plot_div_dispertion = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[1], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="расстояние, м"), yaxis=dict(title="Концентарция, кг/м3"))
    },
        output_type='div', show_link=False, link_text="")

    plot_div_dose = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[2], line=dict(color='#ff0000', width=3))],
        "layout": Layout(xaxis=dict(title="расстояние, м"), yaxis=dict(title="Токсодоза, мг/мин*л"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/dispersion_light_gas_result.html', {'request': request,
                                                                                    'user': user,
                                                                                    'zone_array': zipped_list,
                                                                                    'plot_div_dispertion': plot_div_dispertion,
                                                                                    'plot_div_dose': plot_div_dose,
                                                                                    'calc_data': (
                                                                                        ambient_temperature,
                                                                                        cloud, wind_speed,
                                                                                        is_night,
                                                                                        is_urban_area,
                                                                                        ejection_height,
                                                                                        gas_temperature,
                                                                                        gas_weight, gas_flow,
                                                                                        closing_time,
                                                                                        molecular_weight)
                                                                                    })


@router.get('/heavy_gas_inst', response_class=HTMLResponse)
async def get_dispersion_heavy_gas_inst(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/dispersion_heavy_gas_inst_form.html',
                                      {'request': request, 'user': user})


@router.post('/heavy_gas_inst', response_class=HTMLResponse)
async def post_dispersion_heavy_gas_inst(request: Request,
                                         volume_gas: str = Form(...), density_init: str = Form(...),
                                         density_air: str = Form(...), wind_speed: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    # 1. Получим класс для расчета взрыва
    if float(density_init) < float(density_air):
        density_init = float(density_init) + 1
    dispertion_unit = calc_heavy_gas_disp.Instantaneous_source(volume_gas=float(volume_gas),
                                                               density_init=float(density_init),
                                                               wind_speed=float(wind_speed),
                                                               density_air=float(density_air))
    # 2. Получим зоны для большой таблицы (не классифицированные)
    zone_array = dispertion_unit.result()
    # Преобразование к виду [(dose, conc, dist, wight, time),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2], zone_array[3], zone_array[4])
    zipped_list = list(zipped_values)

    plot_div_dispertion = plot({
        "data": [Scatter(x=zone_array[2], y=zone_array[1], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="расстояние, м"), yaxis=dict(title="Концентарция, кг/м3"))
    },
        output_type='div', show_link=False, link_text="")

    plot_div_dose = plot({
        "data": [Scatter(x=zone_array[2], y=zone_array[0], line=dict(color='#ff0000', width=3))],
        "layout": Layout(xaxis=dict(title="расстояние, м"), yaxis=dict(title="Токсодоза, мг/мин*л"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/dispersion_heavy_gas_inst_result.html', {'request': request,
                                                                                         'user': user,
                                                                                         'zone_array': zipped_list,
                                                                                         'plot_div_dispertion': plot_div_dispertion,
                                                                                         'plot_div_dose': plot_div_dose,
                                                                                         'calc_data': (
                                                                                             volume_gas, density_init,
                                                                                             wind_speed, density_air)
                                                                                         })
