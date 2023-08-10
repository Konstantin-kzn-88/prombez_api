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


@router.get('/objects-for-org={org_id}', response_class=HTMLResponse)
async def get_all_objects_for_organization(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    objects = db.query(models.Object).filter(models.Object.org_id == org_id).all()
    current_organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/devs/objects_for_organization.html',
                                      {'request': request, 'objects': objects,
                                       'current_organization': current_organization, 'user': user})


@router.get('/objects-for-org={org_id}/projects-for-obj={object_id}', response_class=HTMLResponse)
async def get_all_projects_for_object(request: Request, object_id: int, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    projects = db.query(models.Project).filter(models.Project.object_id == object_id).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    return templates.TemplateResponse('docs_app/devs/projects_for_object.html',
                                      {'request': request, 'projects': projects, 'object': object_id,
                                       'current_organization': current_organization, 'user': user})


@router.get('/objects-for-org={org_id}/projects-for-obj={object_id}/devs-for-project={project_id}',
            response_class=HTMLResponse)
async def get_all_devs_for_project(request: Request, object_id: int, org_id: int, project_id: int,
                                   db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    devs = db.query(models.Device).filter(models.Device.project_id == project_id).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    return templates.TemplateResponse('docs_app/devs/devs_for_project.html',
                                      {'request': request, 'devs': devs, 'object_id': object_id,
                                       'project_id': project_id,
                                       'current_organization': current_organization, 'user': user})


@router.get('/objects-for-org={org_id}/projects-for-obj={object_id}/devs-for-project={project_id}/edit-dev_id={dev_id}',
            response_class=HTMLResponse)
async def dev_edit(request: Request, object_id: int, org_id: int, project_id: int, dev_id: int,
                   db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    dev = db.query(models.Device).filter(models.Device.id == dev_id).first()
    projects = db.query(models.Project).filter(models.Project.object_id == object_id).all()
    subs = db.query(models.Substance).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    return templates.TemplateResponse('docs_app/devs/devs_edit.html',
                                      {'request': request, 'projects': projects, 'subs': subs, 'dev': dev,
                                       'current_organization': current_organization, 'project_id': project_id, 'user': user})
