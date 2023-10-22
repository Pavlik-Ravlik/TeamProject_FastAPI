from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.database.models import User

from src.repository import admin as repository_admin
from src.services.auth import auth_service
from schemas import  ShareResponce, ShareRequest, Admin, CommentResponce


router = APIRouter(prefix="/all-shares", tags=['admin-moder'])


@router.get('/all-shares', response_model=List[ShareResponce])
async def admin_read_shares(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    shares = repository_admin.admin_get_list_users_shares(db, current_user)
    return shares


@router.get("/{share_id}", response_model=ShareResponce)
async def admin_read_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.admin_get_user_share(share_id, db, current_user)
    return share


@router.put("/{share_id}", response_model=ShareResponce)
async def admin_update_share(share_id: int, update_share: ShareRequest, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.admin_update_share(share_id, update_share, db, current_user)
    return share


@router.delete("/{share_id}", response_model=ShareResponce)
async def admin_delete_share(share_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.admin_delete_share(share_id, db, current_user)
    return share


@router.put("/{user_id}", response_model=Admin)
async def admin_transfer_role(user_id: int, role: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = await repository_admin.admin_get_role(user_id, role, db, current_user)
    return share 


@router.get('/all-comments', response_model=CommentResponce)
async def admin_read_comments(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comments = await repository_admin.admin_read_comments(db, current_user)

    if comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found.")
    return comments


@router.get('/{comment_id}', response_model=CommentResponce)
async def admin_read_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_admin.admin_get_comment(comment_id, db, current_user)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")
    return comment


@router.put('/{comment_id}', response_model=CommentResponce)
async def admin_update_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_admin.admin_update_comment(comment_id, db, current_user)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found')
    return comment

@router.delete('/{comment_id}', response_model=CommentResponce)
async def admin_delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await repository_admin.admin_delete_comment(comment_id, db, current_user)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")
    return comment
