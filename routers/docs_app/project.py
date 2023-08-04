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



@router.get('/add')
async def post_account(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    all_organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()
    return templates.TemplateResponse('docs_app/projects/projects_add.html',
                                      {'request': request, 'all_organizations': all_organizations, 'user': user})

@router.post('/add', response_class=HTMLResponse)
async def post_account(request: Request,
                       name_project: str = Form(...), code_project: str = Form(...),
                       description_project: str = Form(...), org_id: str = Form(...),
                       db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    project_model = models.Project()
    project_model.name_project = name_project
    project_model.code_project = code_project
    project_model.description_project = description_project
    project_model.org_id = org_id
    project_model.user_id = user.get('user_id')

    db.add(project_model)
    db.commit()

    return RedirectResponse(url='/projects', status_code=status.HTTP_302_FOUND)

@router.get('/')
async def get_select_organization(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    all_organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()

    return templates.TemplateResponse('docs_app/projects/projects.html',
                                      {'request': request, 'all_organizations': all_organizations, 'user': user})


@router.get('/{org_id}', response_class=HTMLResponse)
async def get_all_projects_for_organization(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    projects = db.query(models.Project).filter(models.Project.org_id == org_id).all()
    current_organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/projects/projects_for_organization.html',
                                      {'request': request, 'projects': projects,
                                       'current_organization': current_organization, 'user': user})


@router.get('/edit/{project_id}', response_class=HTMLResponse)
async def project_edit(request: Request, project_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    all_organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()
    return templates.TemplateResponse('docs_app/projects/projects_edit.html',
                                      {'request': request, 'project': project, 'all_organizations': all_organizations,
                                       'user': user})


@router.post('/edit/{project_id}', response_class=HTMLResponse)
async def post_project(request: Request, project_id: int,
                       name_project: str = Form(...), code_project: str = Form(...),
                       description_project: str = Form(...),
                       org_id: str = Form(...),
                       db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    project.name_project = name_project
    project.code_project = code_project
    project.description_project = description_project
    project.org_id = org_id

    db.add(project)
    db.commit()

    id = project.org_id

    return RedirectResponse(url=f'/projects/{id}', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{project_id}')
async def project_delete(request: Request, project_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    org_id = project.org_id
    if project is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    db.query(models.Project).filter(models.Project.id == project_id).delete()
    db.commit()

    return RedirectResponse(url=f'/projects/{org_id}', status_code=status.HTTP_302_FOUND)


