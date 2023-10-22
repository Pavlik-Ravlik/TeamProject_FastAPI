from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.repository import comments as repository_comment
from src.repository import shares as repository_share
from src.services.auth import auth_service
from schemas import CommentRequest, CommentResponce


router = APIRouter(prefix="/comments", tags=['comment'])


@router.post("/create", response_model=CommentResponce, status_code=status.HTTP_201_CREATED)
async def create_comment(share_id: int, comment: CommentRequest, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    share = repository_share.get_share_by_id(share_id, db)
    
    if share is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Share not found.')
    
    if share.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't coment your personality share." )
    
    comment = await repository_comment.create_comment(share_id, comment, db, current_user)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
     
    return comment


@router.put('/{comment_id}', response_model=CommentResponce)
async def update_comment_id(comment_id: int, new_text: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = repository_comment.update_comment(comment_id, new_text, db, current_user)

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found.')
    
    return comment
