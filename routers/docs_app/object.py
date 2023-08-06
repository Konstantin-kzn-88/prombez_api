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
    prefix='/objects',
    tags=['objects'],
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
async def get_add_object(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    all_organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()
    return templates.TemplateResponse('docs_app/objects/objects_add.html',
                                      {'request': request, 'all_organizations': all_organizations, 'user': user})


@router.post('/add', response_class=HTMLResponse)
async def post_add_object(request: Request,
                          name_object: str = Form(...), address_object: str = Form(...),
                          reg_number_object: str = Form(...),
                          class_object: str = Form(...), org_id: str = Form(...),
                          db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    object_model = models.Object()
    object_model.name_object = name_object
    object_model.address_object = address_object
    object_model.reg_number_object = reg_number_object
    object_model.class_object = class_object
    object_model.org_id = org_id

    db.add(object_model)
    db.commit()

    return RedirectResponse(url='/objects', status_code=status.HTTP_302_FOUND)


@router.get('/')
async def get_select_organization(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    all_organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()

    return templates.TemplateResponse('docs_app/objects/objects.html',
                                      {'request': request, 'all_organizations': all_organizations, 'user': user})


@router.get('/{org_id}', response_class=HTMLResponse)
async def get_all_objects_for_organization(request: Request, org_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    objects = db.query(models.Object).filter(models.Object.org_id == org_id).all()
    current_organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return templates.TemplateResponse('docs_app/objects/objects_for_organization.html',
                                      {'request': request, 'objects': objects,
                                       'current_organization': current_organization, 'user': user})


@router.get('/edit/{object_id}', response_class=HTMLResponse)
async def object_edit(request: Request, object_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    object = db.query(models.Object).filter(models.Object.id == object_id).first()
    all_organizations = db.query(models.Organization).filter(models.Organization.user_id == user.get('user_id')).all()
    return templates.TemplateResponse('docs_app/objects/objects_edit.html',
                                      {'request': request, 'object': object, 'all_organizations': all_organizations,
                                       'user': user})


@router.post('/edit/{object_id}', response_class=HTMLResponse)
async def post_object(request: Request, object_id: int,
                      name_object: str = Form(...), address_object: str = Form(...),
                      reg_number_object: str = Form(...),
                      class_object: str = Form(...), org_id: str = Form(...),
                      db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    object = db.query(models.Object).filter(models.Object.id == object_id).first()

    object.name_object = name_object
    object.address_object = address_object
    object.reg_number_object = reg_number_object
    object.class_object = class_object
    object.org_id = org_id

    db.add(object)
    db.commit()

    id = object.org_id

    return RedirectResponse(url=f'/objects/{id}', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{object_id}')
async def project_delete(request: Request, object_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    object = db.query(models.Object).filter(models.Project.id == object_id).first()
    org_id = object.org_id
    if object is None:
        return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)

    db.query(models.Object).filter(models.Object.id == object_id).delete()
    db.commit()

    return RedirectResponse(url=f'/objects/{org_id}', status_code=status.HTTP_302_FOUND)
