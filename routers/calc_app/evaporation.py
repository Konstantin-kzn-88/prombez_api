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

from calculation_methods import calc_evaporation_LPG

router = APIRouter(
    prefix='/evaporation',
    tags=['evaporation'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/lpg', response_class=HTMLResponse)
async def get_evaporation(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/evaporation_lpg_form.html', {'request': request, 'user': user})


@router.post('/lpg', response_class=HTMLResponse)
async def post_evaporation(request: Request,
                           molar_mass: str = Form(...), strait_area: str = Form(...),
                           wind_velosity: str = Form(...), lpg_temperature: str = Form(...),
                           surface_temperature: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    # 1. Получим класс для расчета взрыва
    evaporation_unit = calc_evaporation_LPG.LPG_evaporation(float(molar_mass), float(strait_area), float(wind_velosity),
                                                            float(lpg_temperature), float(surface_temperature))
    # 2. Получим зоны для большой таблицы (не классифицированные)
    zone_array = evaporation_unit.evaporation_array()
    # Преобразование к виду [(t, mass),...]
    zipped_values = zip(zone_array[0], zone_array[1])
    zipped_list = list(zipped_values)

    plot_div_evaporation = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[1], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="Время, с"), yaxis=dict(title="Масса вещества, кг"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/evaporation_lpg_result.html', {'request': request,
                                                                               'user': user,
                                                                               'zone_array': zipped_list,
                                                                               'plot_div_evaporation': plot_div_evaporation,
                                                                               'calc_data': (
                                                                               molar_mass, strait_area, wind_velosity,
                                                                               lpg_temperature, surface_temperature)
                                                                               })
