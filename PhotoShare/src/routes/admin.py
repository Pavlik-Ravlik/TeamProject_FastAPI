from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.database.models import User

from src.repository import public as repository_public
from src.repository import admin as repository_admin
from src.services.auth import auth_service
from schemas import  ShareResponce, ShareRequest, Admin


router = APIRouter(prefix="/all-shares", tags=['admin'])


@router.get('/all-shares', response_model=List[ShareResponce])
async def admin_read_shares(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = repository_public.get_list_users_shares(db, current_user)
    return shares


@router.get("/{share_id}", response_model=ShareResponce)
async def admin_read_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_public.get_user_share(share_id, db, current_user)
    return share


@router.put("/{share_id}", response_model=ShareResponce)
async def admin_update_share(share_id: int, update_share: ShareRequest, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.update_share(share_id, update_share, db, current_user)
    return share


@router.delete("/{share_id}", response_model=ShareResponce)
async def admin_delete_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.delete_share(share_id, db, current_user)
    return share


@router.put("/{share_id}", response_model=Admin)
async def admin_transfer_role(user_id: int, role: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.admin_get_role(user_id, role, db, current_user)
    return share 