from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from typing import List
#from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import Share, User

from src.repository import shares as repository_shares
from src.services.auth import auth_service
from src.conf.config import settings
from schemas import ShareRequest, ShareResponce
from repository.shares import generate_qr_code

router = APIRouter(prefix="/shares", tags=['my-shares'])


@router.post('/create', response_model=ShareResponce, status_code=status.HTTP_201_CREATED)
async def create_share(share: ShareRequest, file: UploadFile = File(),  db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    # uploaded_file_jpg
    r = cloudinary.uploader.upload(
        file.file,
        public_id=f"NotesApp/{current_user.username}", # NotesApp/{current_user.username}_jpg
        width=500,
        height=500,
        crop="limit",
        format="jpg",
    )

    src_url = cloudinary.CloudinaryImage(f"NotesApp/{current_user.username}").build_url( # (f"NotesApp/{current_user.username}_jpg") or (uploaded_file_jpg['public_id']) / (r['public_id'])
        width=500, height=500, crop="limit", format="jpg"
    )
    
    share = await repository_shares.create_share(share, src_url, db, current_user)
    return share


@router.post('/qr', response_model=List[ShareResponce]) 
async def get_qrcode(url: str, name: str, db: Session, current_user: User):
    image_qr = await generate_qr_code(url=url, name=name, db=db, current_user=current_user)
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
