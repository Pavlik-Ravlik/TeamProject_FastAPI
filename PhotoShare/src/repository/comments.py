from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from fastapi import HTTPException

from src.database.models import User, Comment
from schemas import CommentRequest


async def create_comment(share_id: int, comment: CommentRequest, db: Session, current_user: User) -> Comment:
    comment = db.query(Comment).filter(Comment.description == comment.description).first()
    if comment is None:
        raise HTTPException(status_code=400, detail='You comment is already exist.')
    
    
    comment = Comment(share=share_id, description=comment.description, user=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def update_comment(comment_id: int, new_text: str ,db: Session, current_user: User) -> Comment:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail='You are not allowed to edit this comment.')
    
    comment.description = new_text
    db.commit()
    db.refresh(comment)
    return comment