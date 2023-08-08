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
    prefix='/devs',
    tags=['devs'],
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
async def get_select_organization(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    all_organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()
    return templates.TemplateResponse('docs_app/devs/devs.html',
                                      {'request': request, 'all_organizations': all_organizations, 'user': user})


@router.get('/{org_id}', response_class=HTMLResponse)
async def get_all_projects_for_organization(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    projects = db.query(models.Project).filter(models.Project.org_id == org_id).all()
    current_organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/devs/objects_for_organization.html',
                                      {'request': request, 'projects': projects,
                                       'current_organization': current_organization, 'user': user})


@router.get('/project/{project_id}', response_class=HTMLResponse)
async def project_edit(request: Request, project_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    current_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    all_devs = db.query(models.Device).filter(models.Device.project_id == project_id).all()
    return templates.TemplateResponse('docs_app/devs/dev_for_project.html',
                                      {'request': request, 'current_project': current_project, 'all_devs': all_devs,
                                       'user': user})
