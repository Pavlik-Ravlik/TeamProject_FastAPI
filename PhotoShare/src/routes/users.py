from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    This function will be activated when the client sends a GET request to this route.

    :param current_user: A contacts for the user.
    :type current_user: User
    :return: Current user.
    :rtype: User
    """
    return current_user


@router.patch("/avatar", response_model=UserDb)
async def update_avatar_user(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Triggered when a client sends a PATCH request to this route.

    :param file: Upload file for a user.
    :type file: UploadFile
    :param current_user: Update avatar user for the user.
    :type current_user: User
    :param db: The database session
    :type db: Session
    :return: User.
    :rtype: User
    """
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
    
    """
    uploaded_file_png = upload(
        file.file, 
        public_id=f'NotesApp/{current_user.username}_png', 
        width=500, 
        height=500, 
        crop='limit', 
        format='png',
    )
    """
    
    # src_url_jpg
    src_url = cloudinary.CloudinaryImage(f"NotesApp/{current_user.username}").build_url( # (f"NotesApp/{current_user.username}_jpg") or (uploaded_file_jpg['public_id']) / (r['public_id'])
        width=500, height=500, crop="limit", format="jpg"
    )
    
    """
    src_url_png = cloudinary.CloudinaryImage(uploaded_file_png['public_id']).build_url(
        width=500, height=500, crop='limit', format='png'
    )
    """

    user = await repository_users.update_avatar(current_user.email, src_url, db) # (current_user.email, src_url_jpg, src_url_png, db)
    return user
