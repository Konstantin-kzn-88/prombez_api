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
    prefix='/pipelines',
    tags=['pipelines'],
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
    return templates.TemplateResponse('docs_app/pipelines/pipelines.html',
                                      {'request': request, 'all_organizations': all_organizations, 'user': user})


@router.get('/objects-for-org={org_id}', response_class=HTMLResponse)
async def get_all_objects_for_organization(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    objects = db.query(models.Object).filter(models.Object.org_id == org_id).all()
    current_organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/pipelines/objects_for_organization.html',
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
    return templates.TemplateResponse('docs_app/pipelines/projects_for_object.html',
                                      {'request': request, 'projects': projects, 'object': object_id,
                                       'current_organization': current_organization, 'user': user})


@router.get('/objects-for-org={org_id}/projects-for-obj={object_id}/pipes-for-project={project_id}',
            response_class=HTMLResponse)
async def get_all_pipes_for_project(request: Request, object_id: int, org_id: int, project_id: int,
                                    db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    pipes = db.query(models.Pipeline).filter(models.Pipeline.project_id == project_id).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    return templates.TemplateResponse('docs_app/pipelines/pipelines_for_project.html',
                                      {'request': request, 'pipes': pipes, 'object_id': object_id,
                                       'project_id': project_id,
                                       'current_organization': current_organization, 'user': user})


@router.get(
    '/objects-for-org={org_id}/projects-for-obj={object_id}/pipes-for-project={project_id}/edit-pipe_id={pipe_id}',
    response_class=HTMLResponse)
async def dev_edit(request: Request, object_id: int, org_id: int, project_id: int, pipe_id: int,
                   db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    pipe = db.query(models.Pipeline).filter(models.Pipeline.id == pipe_id).first()
    projects = db.query(models.Project).filter(models.Project.object_id == object_id).all()
    subs = db.query(models.Substance).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    return templates.TemplateResponse('docs_app/pipelines/pipelines_edit.html',
                                      {'request': request, 'projects': projects, 'subs': subs, 'pipe': pipe,
                                       'current_organization': current_organization, 'project_id': project_id,
                                       'user': user})


@router.post(
    '/objects-for-org={org_id}/projects-for-obj={object_id}/pipes-for-project={prj_id}/edit-pipe_id={pipe_id}',
    response_class=HTMLResponse)
async def post_dev(request: Request, object_id: int, org_id: int, prj_id: int, pipe_id: int,
                   pipe_name: str = Form(...), pipe_lenght: str = Form(...),
                   pipe_diameter: str = Form(...), pipe_pressure: str = Form(...),
                   pipe_temp: str = Form(...), pipe_flow: str = Form(...),
                   pipe_shutdown: str = Form(...), pipe_view_space: str = Form(...),
                   pipe_death_man: str = Form(...), pipe_injured_man: str = Form(...),
                   project_id: str = Form(...),
                   db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    pipe = db.query(models.Pipeline).filter(models.Pipeline.id == pipe_id).first()

    pipe.pipe_name = pipe_name
    pipe.pipe_lenght = pipe_lenght
    pipe.pipe_diameter = pipe_diameter
    pipe.pipe_pressure = pipe_pressure
    pipe.pipe_temp = pipe_temp
    pipe.pipe_flow = pipe_flow
    pipe.pipe_shutdown = pipe_shutdown
    pipe.pipe_view_space = pipe_view_space
    pipe.pipe_death_man = pipe_death_man
    pipe.pipe_injured_man = pipe_injured_man
    pipe.project_id = project_id

    db.add(pipe)
    db.commit()

    return RedirectResponse(
        url=f'/pipelines/objects-for-org={org_id}/projects-for-obj={object_id}/pipes-for-project={prj_id}',
        status_code=status.HTTP_302_FOUND)


@router.get('/delete/{pipe_id}')
async def pipe_delete(request: Request, pipe_id: int,
                      db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    pipe = db.query(models.Pipeline).filter(models.Pipeline.id == pipe_id).first()
    if pipe is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    db.query(models.Pipeline).filter(models.Pipeline.id == pipe_id).delete()
    db.commit()

    return RedirectResponse(url=f'/pipelines/', status_code=status.HTTP_302_FOUND)


@router.get('/objects-for-org={org_id}/projects-for-obj={object_id}/pipes-for-project={project_id}/pipe-add')
async def get_add_post_pipe(request: Request, object_id: int, org_id: int, project_id: int,
                            db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    projects = db.query(models.Project).filter(models.Project.object_id == object_id).all()
    subs = db.query(models.Substance).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()

    return templates.TemplateResponse('docs_app/pipelines/pipelines_add.html',
                                      {'request': request, 'projects': projects, 'subs': subs, 'object_id': object_id,
                                       'current_organization': current_organization, 'project_id': project_id,
                                       'user': user})


@router.post('/objects-for-org={org_id}/projects-for-obj={object_id}/pipes-for-project={prj_id}/pipe-add',
             response_class=HTMLResponse)
async def post_add_pipe(request: Request, object_id: int, org_id: int, prj_id: int,
                        pipe_name: str = Form(...), pipe_lenght: str = Form(...),
                        pipe_diameter: str = Form(...), pipe_pressure: str = Form(...),
                        pipe_temp: str = Form(...), pipe_flow: str = Form(...),
                        pipe_shutdown: str = Form(...), pipe_view_space: str = Form(...),
                        pipe_death_man: str = Form(...), pipe_injured_man: str = Form(...),
                        project_id: str = Form(...),
                        db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    pipe_model = models.Pipeline()

    pipe_model.pipe_name = pipe_name
    pipe_model.pipe_lenght = pipe_lenght
    pipe_model.pipe_diameter = pipe_diameter
    pipe_model.pipe_pressure = pipe_pressure
    pipe_model.pipe_temp = pipe_temp
    pipe_model.pipe_flow = pipe_flow
    pipe_model.pipe_shutdown = pipe_shutdown
    pipe_model.pipe_view_space = pipe_view_space
    pipe_model.pipe_death_man = pipe_death_man
    pipe_model.pipe_injured_man = pipe_injured_man
    pipe_model.project_id = project_id

    db.add(pipe_model)
    db.commit()

    return RedirectResponse(
        url=f'/pipelines/objects-for-org={org_id}/projects-for-obj={object_id}/pipes-for-project={prj_id}',
        status_code=status.HTTP_302_FOUND)
