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
    prefix='/user_organizations',
    tags=['user_organizations'],
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
async def get_all_organizsations(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()
    return templates.TemplateResponse('docs_app/organizations.html',
                                      {'request': request, 'organizations': organizations, 'user': user})


@router.get('/edit/{org_id}', response_class=HTMLResponse)
async def organization_edit(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/organizations_edit.html',
                                      {'request': request, 'organization': organization, 'user': user})


@router.post('/edit/{org_id}', response_class=HTMLResponse)
async def post_organization(request: Request, org_id: int,
                       name_organization: str = Form(...), legal_address: str = Form(...),
                       name_position_director: str = Form(...), name_director: str = Form(...),
                       name_position_tech_director: str = Form(...), name_tech_director: str = Form(...),
                       telephone: str = Form(...), email: str = Form(...),
                       db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()

    organization.name_organization = name_organization
    organization.legal_address = legal_address
    organization.name_position_director = name_position_director
    organization.name_director = name_director
    organization.name_position_tech_director = name_position_tech_director
    organization.name_tech_director = name_tech_director
    organization.telephone = telephone
    organization.email = email

    db.add(organization)
    db.commit()

    return RedirectResponse(url='/user_organizations', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{org_id}')
async def organization_delete(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    if organization is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    db.query(models.Organization).filter(models.Organization.id == org_id).delete()
    db.commit()

    return RedirectResponse(url='/user_organizations', status_code=status.HTTP_302_FOUND)


@router.get('/add', response_class=HTMLResponse)
async def organization_add(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('docs_app/organizations_add.html', {'request': request, 'user': user})


@router.post('/add', response_class=HTMLResponse)
async def post_account(request: Request,
                       name_organization: str = Form(...), legal_address: str = Form(...),
                       name_position_director: str = Form(...), name_director: str = Form(...),
                       name_position_tech_director: str = Form(...), name_tech_director: str = Form(...),
                       telephone: str = Form(...), email: str = Form(...),
                       db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    organization_model = models.Organization()
    organization_model.name_organization = name_organization
    organization_model.legal_address = legal_address
    organization_model.name_position_director = name_position_director
    organization_model.name_director = name_director
    organization_model.name_position_tech_director = name_position_tech_director
    organization_model.name_tech_director = name_tech_director
    organization_model.telephone = telephone
    organization_model.email = email
    organization_model.user_id = user.get('user_id')

    db.add(organization_model)
    db.commit()

    return RedirectResponse(url='/user_organizations', status_code=status.HTTP_302_FOUND)
