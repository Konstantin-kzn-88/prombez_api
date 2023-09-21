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

from calculation_methods import calc_strait_fire

router = APIRouter(
    prefix='/strait_fire',
    tags=['strait_fire'],
    responses={404: {'descrition': 'Not found'}}

)

templates = Jinja2Templates(directory='templates')


@router.get('/mchs_404_strait_fire', response_class=HTMLResponse)
async def get_explosion_sp(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('calc_app/mchs_404_strait_fire_form.html', {'request': request, 'user': user})


@router.post('/mchs_404_strait_fire', response_class=HTMLResponse)
async def post_dev_edit(request: Request,
                        s_spill: str = Form(...), m_sg: str = Form(...),
                        mol_mass: str = Form(...), t_boiling: str = Form(...),
                        wind_velocity: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    fire_unit = calc_strait_fire.Strait_fire()
    zone_array = fire_unit.termal_radiation_array(float(s_spill), float(m_sg), float(mol_mass), float(t_boiling),
                                                  float(wind_velocity))
    # Преобразование к виду [(r, q, pr, q_vp),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2], zone_array[3])
    zipped_list = list(zipped_values)

    plot_div_q_termal = plot({
        "data": [Scatter(x=zone_array[0], y=zone_array[1], line=dict(color='#62fb60', width=3))],
        "layout": Layout(xaxis=dict(title="Расстояние, м"), yaxis=dict(title="Интенсивность теплизлучения, кВт/м2"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/mchs_404_strait_fire_result.html', {'request': request,
                                                                                    'user': user,
                                                                                    'zone_array': zipped_list,
                                                                                    'plot_div_q_termal': plot_div_q_termal,
                                                                                    'calc_data': (
                                                                                        s_spill, m_sg, mol_mass,
                                                                                        t_boiling,
                                                                                        wind_velocity)
                                                                                    })
