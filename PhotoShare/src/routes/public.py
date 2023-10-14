from fastapi import APIRouter, Depends, Query, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from typing import List
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import Share, User

from src.repository import public as repository_public
from src.services.auth import auth_service
from src.conf.config import settings
from schemas import ShareRequest, ShareResponce



router = APIRouter(prefix="/public-shares", tags=['recomendations'])



@router.get('/public-shares', response_model=List[ShareResponce]) #  , dependencies=[Depends(RateLimiter(times=10, seconds=60)
async def read_shares(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = repository_public.get_list_users_shares(db, current_user)
    return shares


@router.get("/{public-share_id}", response_model=ShareResponce)
async def read_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_public.get_user_share(share_id, db, current_user)
    return share