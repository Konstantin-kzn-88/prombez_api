import sys

sys.path.append('../..')

from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, Depends, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from fastapi.responses import HTMLResponse

from calculation_methods import calc_sp_explosion

router = APIRouter(
    prefix='/explosion',
    tags=['explosion'],
    responses={404: {'descrition': 'Not found'}}

)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/sp1213130-2009', response_class=HTMLResponse)
async def get_explosion_sp(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    return templates.TemplateResponse('calc_app/sp12_13130_2009.html', {'request': request, 'user': user})


@router.post('/sp1213130-2009', response_class=HTMLResponse)
async def post_dev_edit(request: Request,
                        mass: str = Form(...), heat_of_combustion: str = Form(...),
                        z: str = Form(...)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    explosion_unit = calc_sp_explosion.Explosion()
    zone_array = explosion_unit.explosion_array(float(mass), float(heat_of_combustion), float(z))
    # Преобразование к виду [(r, dP, i, pr, q_vp),...]
    zipped_values = zip(zone_array[0], zone_array[1], zone_array[2], zone_array[3], zone_array[4])
    zipped_list = list(zipped_values)

    x_data = zone_array[0]
    y_data = zone_array[1]

    plot_div = plot({
        "data": [Scatter(x=x_data, y=y_data)],
        "layout": Layout(title="Взрыв (СП 12.13130-2009)", xaxis=dict(title="X Label"), yaxis=dict(title="У Label"))
    },
        output_type='div', show_link=False, link_text="")

    return templates.TemplateResponse('calc_app/sp12_13130_2009_result.html', {'request': request,
                                                                               'user': user,
                                                                               'zone_array': zipped_list,
                                                                               'plot_div': plot_div
                                                                               })
