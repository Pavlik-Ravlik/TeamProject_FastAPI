from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type

from src.database.models import User, Share, Comment
from schemas import ShareRequest



async def admin_get_list_users_shares(db: Session, current_user: User) -> list[Type[Share]]:
    shares = db.query(Share).filter(Share.user_id != current_user.id).all()

    if not shares:
        raise HTTPException(status_code=404, detail="Shares not found")
    
    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return shares


async def admin_get_user_share(share_id: str, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id != current_user.id)).first()

    if not share:
        raise HTTPException(status_code=404, detail="Share not found.")
    
    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return share


async def admin_update_share(share_id: int, updated_share: ShareRequest, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id != current_user.id)).first()

    if not share:
        raise HTTPException(status_code=404, detail='Share not found')
    
    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    
    for attr, value in updated_share.model_dump().items():
        setattr(share, attr, value)

    db.commit()
    db.refresh(share)
    return share


async def admin_delete_share(share_id: int, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id != current_user.id)).first()

    if not share:
        raise HTTPException(status_code=404, detail='Share not found')

    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power") 

    db.delete(share)
    db.commit()
    return share


async def admin_get_role(user_id: int, role: str, db: Session, current_user: User) -> Type[User]:
    user = db.query(User).filter(and_(User.id == user_id, User.id != current_user.id)).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="You don't have such power")
    
    user.role = role
    db.commit()
    db.refresh(user)
    return user


async def admin_read_comments(db: Session, current_user: User) -> list[Type[Comment]]:
    comments = db.query(Comment).filter(Comment.user_id != current_user.id).all()

    if not comments:
        raise HTTPException(status_code=404, detail='Comments not found.')
    
    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return comments


async def read_comment(comment_id: int, db: Session, current_user: User) -> Type[Comment]:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id != current_user.id))

    if not comment:
        raise HTTPException(status_code=404, detail='Comment not found.')

    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return comment


async def admin_update_comment(comment_id: str, db: Session, current_user: User) -> Type[Comment]:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id != current_user.id))
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")
    
    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return comment


async def admin_delete_comment(comment_id: str, db: Session, current_user: User) -> Type[Comment]:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, User.id != current_user.id))

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found.")

    if current_user.role != 'admin' or current_user.role != 'moder':
        raise HTTPException(status_code=403, detail="You don't have such power")
    return comment
