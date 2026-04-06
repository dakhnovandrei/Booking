from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from UOW import get_uow
from schemas.exception_schemas import InvalidUserType, RoomNotFound
from schemas.room_schemas import RoomCreate, RoomDTO, RoomUpdate, RoomSearchParams
from jwt_functions import get_current_user
from services.room_service import RoomService

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.post('/create', response_model=RoomDTO)
async def create_room(room_data: RoomCreate, user=Depends(get_current_user), uow=Depends(get_uow)) -> RoomDTO:
    room_service = RoomService(uow)
    try:
        reg_room = await room_service.create_room(user, room_data)
        room_dto = RoomDTO.model_validate(reg_room)
        return room_dto
    except InvalidUserType:
        raise HTTPException(status_code=403, detail="Данный тип пользователя не может создавать объявления")


@router.patch('/update', response_model=RoomCreate)
async def update_room(room_data: RoomUpdate, room_id: int = Query(...), user=Depends(get_current_user),
                      uow=Depends(get_uow)):
    room_service = RoomService(uow)
    try:
        updated_room = await room_service.update_room(room_id, user, room_data)
        return updated_room
    except RoomNotFound:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    except InvalidUserType:
        raise HTTPException(status_code=403, detail='Пользователь не может создавать объявления')


@router.get('/search', response_model=List[RoomDTO])
async def search_room(room_params: RoomSearchParams = Depends(), uow=Depends(get_uow)):
    room_service = RoomService(uow)
    try:
        rooms = await room_service.search_room(room_params)
        return rooms
    except RoomNotFound:
        raise HTTPException(status_code=404, detail='По вашему запросу ничего не найдено')


@router.get('/', response_model=RoomDTO)
async def get_room(room_id: int = Query(...), uow=Depends(get_uow)):
    room_service = RoomService(uow)
    try:
        room = await room_service.get_room_by_id(room_id)
        return room
    except RoomNotFound:
        raise HTTPException(status_code=404, detail='Данной комнаты не существует')
    except Exception:
        raise HTTPException(status_code=404, detail='Ошибка в поиске комнаты')
