from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.database.models import User

from src.repository import public as repository_public
from src.services.auth import auth_service
from schemas import  ShareResponce


router = APIRouter(prefix="/public-shares", tags=['recomendations'])


@router.get('/public-shares', response_model=List[ShareResponce])
async def read_shares(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = repository_public.get_list_users_shares(db, current_user)
    if shares is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shares not found')
    return shares


@router.get("/{share_id}", response_model=ShareResponce)
async def read_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_public.get_user_share(share_id, db, current_user)
    if share is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Share not found')
    return share