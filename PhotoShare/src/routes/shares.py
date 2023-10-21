import os
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import cloudinary
from cloudinary.uploader import upload, upload_image
from cloudinary.utils import cloudinary_url
from typing import List

from src.database.db import get_db
from src.database.models import Share, User

from src.repository import shares as repository_shares
from src.services.auth import auth_service
from src.conf.config import settings
from schemas import ShareRequest, ShareResponce
from sqlalchemy import and_

router = APIRouter(prefix="/shares", tags=['my-shares'])


@router.post('/create', response_model=ShareResponce, status_code=status.HTTP_201_CREATED)
async def upload_share(description: str, file: UploadFile = File(), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )
    
    try:
        if not file.content_type.startswith("image"):
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        result = upload_image(file.file, folder="photo_base",
                              width=360, height=480, crop="fill")
        
        url, _ = cloudinary_url(
            result["public_id"], format=result["format"])
        
        db_share = await repository_shares.create_share(description, url, db, current_user)
        return db_share
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error uploading photo")


@router.post('/qr', response_model=List[ShareResponce]) 
async def get_qrcode(url: str, name: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):

    image_qr = await repository_shares.generate_qr_code(url=url, name=name, db=db, current_user=current_user)
    return image_qr.print_ascii(tty=True, invert=True)

@router.get('/myshares', response_model=List[ShareResponce]) #  , dependencies=[Depends(RateLimiter(times=10, seconds=60)
async def read_shares(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = repository_shares.get_list_shares(db, current_user)
    return shares


@router.get("/{share_id}", response_model=ShareResponce)
async def read_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_shares.get_share(share_id, db, current_user)
    return share


@router.put("/{share_id}", response_model=ShareResponce)
async def update_share(share_id: int, update_share: ShareRequest, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_shares.update_share(share_id, update_share, db, current_user)
    return share


@router.delete("/{share_id}", response_model=ShareResponce)
async def delete_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_shares.delete_share(share_id, db, current_user)
    return share
