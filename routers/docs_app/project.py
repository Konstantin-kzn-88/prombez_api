import sys

import database

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
    prefix='/projects',
    tags=['projects'],
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
    organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()

    return templates.TemplateResponse('docs_app/projects.html',
                                      {'request': request, 'organizations': organizations, 'user': user})

@router.get('/{org_id}', response_class=HTMLResponse)
async def get_all_projects_for_organization(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    projects = db.query(models.Project).filter(models.Project.org_id == org_id).all()
    organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/projects_for_organization.html',
                                      {'request': request, 'projects': projects, 'organization': organization, 'user': user})


@router.get('/edit/{project_id}', response_class=HTMLResponse)
async def project_edit(request: Request, project_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    return templates.TemplateResponse('docs_app/projects_edit.html',
                                      {'request': request, 'project': project, 'user': user})


@router.post('/edit/{project_id}', response_class=HTMLResponse)
async def post_project(request: Request, project_id: int,
                       name_project: str = Form(...), code_project: str = Form(...),
                       description_project: str = Form(...),
                       db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    project.name_project = name_project
    project.code_project = code_project
    project.description_project = description_project

    db.add(project)
    db.commit()

    return RedirectResponse(url='/projects', status_code=status.HTTP_302_FOUND)