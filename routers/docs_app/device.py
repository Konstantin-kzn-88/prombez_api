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


@router.get('/org_id={org_id}', response_class=HTMLResponse)
async def get_all_objects_for_organization(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    objects = db.query(models.Object).filter(models.Object.org_id == org_id).all()
    current_organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/devs/objects_for_organization.html',
                                      {'request': request, 'objects': objects,
                                       'current_organization': current_organization, 'user': user})


@router.get('/org_id={org_id}/obj_id={obj_id}', response_class=HTMLResponse)
async def get_all_projects_for_object(request: Request, obj_id: int, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    projects = db.query(models.Project).filter(models.Project.object_id == obj_id).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    return templates.TemplateResponse('docs_app/devs/projects_for_object.html',
                                      {'request': request, 'projects': projects, 'obj_id': obj_id,
                                       'current_organization': current_organization, 'user': user})


@router.get('/org_id={org_id}/obj_id={obj_id}/project_id={project_id}',
            response_class=HTMLResponse)
async def get_all_devs_for_project(request: Request, obj_id: int, org_id: int, project_id: int,
                                   db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    devs = db.query(models.Device).filter(models.Device.project_id == project_id).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    current_project = db.query(models.Project).filter(
        models.Project.id == project_id).first()
    current_object = db.query(models.Object).filter(
        models.Object.id == obj_id).first()
    return templates.TemplateResponse('docs_app/devs/devs_for_project.html',
                                      {'request': request, 'devs': devs, 'current_object': current_object,
                                       'current_project': current_project,
                                       'current_organization': current_organization, 'user': user})


@router.get('/org_id={org_id}/obj_id={obj_id}/project_id={project_id}/edit/dev_id={dev_id}',
            response_class=HTMLResponse)
async def get_dev_edit(request: Request, obj_id: int, org_id: int, project_id: int, dev_id: int,
                   db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    dev = db.query(models.Device).filter(models.Device.id == dev_id).first()
    projects = db.query(models.Project).filter(models.Project.object_id == obj_id).all()
    subs = db.query(models.Substance).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()
    return templates.TemplateResponse('docs_app/devs/devs_edit.html',
                                      {'request': request, 'projects': projects, 'subs': subs, 'dev': dev,
                                       'current_organization': current_organization, 'project_id': project_id,
                                       'user': user})


@router.post(
    '/org_id={org_id}/obj_id={obj_id}/project_id={project_id}/edit/dev_id={dev_id}',
    response_class=HTMLResponse)
async def post_dev_edit(request: Request, obj_id: int, org_id: int, project_id: int, dev_id: int,
                   dev_name: str = Form(...), dev_volume: str = Form(...),
                   dev_complection: str = Form(...), dev_flow: str = Form(...),
                   dev_shutdown: str = Form(...), dev_pressure: str = Form(...),
                   dev_temp: str = Form(...), dev_spill: str = Form(...),
                   dev_death_man: str = Form(...), dev_injured_man: str = Form(...),
                   dev_view_space: str = Form(...), prj_id: str = Form(...),
                   db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    device = db.query(models.Device).filter(models.Device.id == dev_id).first()

    device.dev_name = dev_name
    device.dev_volume = dev_volume
    device.dev_complection = dev_complection
    device.dev_flow = dev_flow
    device.dev_shutdown = dev_shutdown
    device.dev_pressure = dev_pressure
    device.dev_temp = dev_temp
    device.dev_spill = dev_spill
    device.dev_death_man = dev_death_man
    device.dev_injured_man = dev_injured_man
    device.dev_view_space = dev_view_space
    device.project_id = prj_id

    db.add(device)
    db.commit()

    return RedirectResponse(
        url=f'/devs/org_id={org_id}/obj_id={obj_id}/project_id={project_id}',
        status_code=status.HTTP_302_FOUND)


@router.get('/delete/{dev_id}')
async def dev_delete(request: Request, dev_id: int,
                     db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    device = db.query(models.Device).filter(models.Device.id == dev_id).first()
    if device is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    db.query(models.Device).filter(models.Device.id == dev_id).delete()
    db.commit()

    return RedirectResponse(url=f'/devs/', status_code=status.HTTP_302_FOUND)


@router.get('/org_id={org_id}/obj_id={obj_id}/project_id={project_id}/add')
async def get_add_post_device(request: Request, obj_id: int, org_id: int, project_id: int,
                              db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    projects = db.query(models.Project).filter(models.Project.object_id == obj_id).all()
    subs = db.query(models.Substance).all()
    current_organization = db.query(models.Organization).filter(
        models.Organization.user_id == user.get('user_id')).first()

    return templates.TemplateResponse('docs_app/devs/devs_add.html',
                                      {'request': request, 'projects': projects, 'subs': subs, 'object_id':obj_id,
                                       'current_organization': current_organization, 'project_id': project_id,
                                       'user': user})


@router.post('/objects-for-org={org_id}/projects-for-obj={object_id}/devs-for-project={prj_id}/dev-add',
             response_class=HTMLResponse)
async def post_add_project(request: Request, object_id: int, org_id: int, prj_id: int,
                           dev_name: str = Form(...), dev_volume: str = Form(...),
                           dev_complection: str = Form(...), dev_flow: str = Form(...),
                           dev_shutdown: str = Form(...), dev_pressure: str = Form(...),
                           dev_temp: str = Form(...), dev_spill: str = Form(...),
                           dev_death_man: str = Form(...), dev_injured_man: str = Form(...),
                           dev_view_space: str = Form(...), project_id: str = Form(...),
                           db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    device_model = models.Device()

    device_model.dev_name = dev_name
    device_model.dev_volume = dev_volume
    device_model.dev_complection = dev_complection
    device_model.dev_flow = dev_flow
    device_model.dev_shutdown = dev_shutdown
    device_model.dev_pressure = dev_pressure
    device_model.dev_temp = dev_temp
    device_model.dev_spill = dev_spill
    device_model.dev_death_man = dev_death_man
    device_model.dev_injured_man = dev_injured_man
    device_model.dev_view_space = dev_view_space
    device_model.project_id = project_id

    db.add(device_model)
    db.commit()

    return RedirectResponse(url=f'/devs/objects-for-org={org_id}/projects-for-obj={object_id}/devs-for-project={prj_id}',
                            status_code=status.HTTP_302_FOUND)
