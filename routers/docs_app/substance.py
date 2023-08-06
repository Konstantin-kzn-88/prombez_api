import sys

sys.path.append('../..')

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Form, Request, Depends, APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from routers.auth import get_current_user
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/subs',
    tags=['subs'],
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


@router.get('/')
async def get_substances(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    all_substances = db.query(models.Substance).all()

    return templates.TemplateResponse('docs_app/subs/subs.html',
                                      {'request': request, 'all_substances': all_substances, 'user': user})


@router.get('/edit/{sub_id}', response_class=HTMLResponse)
async def sub_edit(request: Request, sub_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    sub = db.query(models.Substance).filter(models.Substance.id == sub_id).first()
    return templates.TemplateResponse('docs_app/subs/subs_edit.html',
                                      {'request': request, 'sub': sub, 'user': user})


@router.post('/edit/{sub_id}', response_class=HTMLResponse)
async def post_organization(request: Request, sub_id: int,
                            sub_name: str = Form(...), sub_density_liguid: str = Form(...),
                            sub_density_gas: str = Form(...), sub_mol_weight: str = Form(...),
                            sub_steam_pressure: str = Form(...), sub_flash_temp: str = Form(...),
                            sub_boiling_temp: str = Form(...), sub_evaporation_heat: str = Form(...),
                            sub_heat_capacity: str = Form(...), sub_class: str = Form(...),
                            sub_heat_combustion_temp: str = Form(...), sub_sigma: str = Form(...),
                            sub_energy_level: str = Form(...), sub_lower_conc: str = Form(...),
                            db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    sub = db.query(models.Substance).filter(models.Substance.id == sub_id).first()

    sub.sub_name = sub_name
    sub.sub_density_liguid = sub_density_liguid
    sub.sub_density_gas = sub_density_gas
    sub.sub_mol_weight = sub_mol_weight
    sub.sub_steam_pressure = sub_steam_pressure
    sub.sub_flash_temp = sub_flash_temp
    sub.sub_boiling_temp = sub_boiling_temp
    sub.sub_evaporation_heat = sub_evaporation_heat
    sub.sub_heat_capacity = sub_heat_capacity
    sub.sub_class = sub_class
    sub.sub_heat_combustion_temp = sub_heat_combustion_temp
    sub.sub_sigma = sub_sigma
    sub.sub_energy_level = sub_energy_level
    sub.sub_lower_conc = sub_lower_conc

    db.add(sub)
    db.commit()

    return RedirectResponse(url='/subs', status_code=status.HTTP_302_FOUND)
