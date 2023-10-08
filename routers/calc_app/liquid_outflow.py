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

from calculation_methods import calc_liguid_outflow_tank

router = APIRouter(
    prefix='/liquid_outflow',
    tags=['liquid_outflow'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/tank', response_class=HTMLResponse)
async def get_outflow_tank(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/liquid_outflow_tank_form.html', {'request': request, 'user': user})


@router.post('/tank', response_class=HTMLResponse)
async def post_outflow_tank(request: Request,
                            volume: str = Form(...), height: str = Form(...),
                            pressure: str = Form(...), fill_factor: str = Form(...),
                            hole_diametr: str = Form(...), density: str = Form(...), ):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    # 1. Получим класс для расчета взрыва
    outflow_unit = calc_liguid_outflow_tank.Outflow(volume=float(volume), height=float(height),
                                                    pressure=float(pressure),
                                                    fill_factor=float(fill_factor), hole_diametr=float(hole_diametr),
                                                    density=float(density))
    # 2. Получим зоны для большой таблицы (не классифицированные)
    zone_array = outflow_unit.result()
    # Преобразование к виду [(mass_liquid,time,fill_tank,height,pressure,flow_rate,delta_mass,mass_leaking),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2], zone_array[3], zone_array[4], zone_array[5], zone_array[6], zone_array[7])
    zipped_list = list(zipped_values)

    plot_div_mass_in_spill = plot({
        "data": [Scatter(x=zone_array[1], y=zone_array[0], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="Время, с"), yaxis=dict(title="Масса жидкости в оборудовании, кг"))
    },
        output_type='div', show_link=False, link_text="")

    plot_div_flow_rate = plot({
        "data": [Scatter(x=zone_array[1], y=zone_array[5], line=dict(color='#6072fb', width=3))],
        "layout": Layout(xaxis=dict(title="Время, с"), yaxis=dict(title="Расход, кг/с"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/liquid_outflow_tank_result.html', {'request': request,
                                                                                   'user': user,
                                                                                   'zone_array': zipped_list,
                                                                                   'plot_div_mass_in_spill': plot_div_mass_in_spill,
                                                                                   'plot_div_flow_rate': plot_div_flow_rate,
                                                                                   'calc_data': (
                                                                                   volume, height, pressure,
                                                                                   fill_factor, hole_diametr, density)
                                                                                   })
