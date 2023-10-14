from sqlalchemy.orm import Session
from sqlalchemy import text, and_

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type

from src.database.models import User, Share
from schemas import ShareRequest



async def get_list_users_shares(db: Session, current_user: User) -> list[Type[Share]]:
    shares = db.query(Share).filter(Share.user_id != current_user.id).all()
    return shares


async def get_user_share(share_id: str, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id == current_user.id)).first()
    return share
