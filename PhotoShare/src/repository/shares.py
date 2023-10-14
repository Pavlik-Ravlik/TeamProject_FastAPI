from sqlalchemy.orm import Session
from sqlalchemy import text, and_

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Type

from src.database.models import User, Share
from schemas import ShareRequest





# create
async def create_share(share: ShareRequest, src_url: str, db: Session, current_user: User) -> Share:
    if db.query(Share).filter(Share.url == share.url).first():
        raise HTTPException(status_code=400, detail='This share is already exists.')
    
    db_share = Share(**share.model_dump(), user=current_user)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share

# read shares
async def get_list_shares(db: Session, current_user: User) -> list[Type[Share]]:
    shares = db.query(Share).filter(Share.user_id == current_user.id).all()
    return shares


#read share
async def get_share(share_id: int, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id == current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')
    return share


# update
async def update_share(share_id: int, updated_share: ShareRequest, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id == current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')
    
    for attr, value in updated_share.model_dump().items():
        setattr(share, attr, value)

    db.commit()
    db.refresh(share)
    return share


# delete
async def delete_share(share_id: int, db: Session, current_user: User) -> Type[Share]:
    share = db.query(Share).filter(and_(Share.id == share_id, Share.user_id == current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found') 

    db.delete(share)
    db.commit()
    return share 
