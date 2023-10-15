from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type

from src.database.models import User, Share
from schemas import ShareRequest



async def get_list_users_shares(db: Session, current_user: User) -> list[Type[Share]]:
    shares = db.query(Share).filter(Share.user_id != current_user.id).all()
    return shares


async def get_user_share(share_id: str, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id != current_user.id)).first()
    return share


async def update_share(share_id: int, updated_share: ShareRequest, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id != current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')
    
    for attr, value in updated_share.model_dump().items():
        setattr(share, attr, value)

    db.commit()
    db.refresh(share)
    return share


async def delete_share(share_id: int, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id != current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found') 

    db.delete(share)
    db.commit()
    return share


async def admin_get_role(user_id: int, role: str, db: Session, current_user: User) -> Type[User]:
    user = db.query(User).filter(and_(User.id == user_id, User.id != current_user.id)).first()

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    user.role = role
    db.commit()
    db.refresh(user)
    return user