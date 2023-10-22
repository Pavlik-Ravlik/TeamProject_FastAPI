from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import HTTPException

from sqlalchemy.orm import Session
from typing import Type

from src.database.models import User, Share
from schemas import ShareRequest
import qrcode as qr
import cloudinary.uploader
from src.repository.tags import create_tag

async def create_share(description: str, url: str,  db: Session, current_user: User) -> Share:
    tags = create_tag(db, description)    
    db_share = Share(url=url, description=description, tag=tags, user=current_user.id)
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

# qrcode
async def generate_qr_code(url: str, name: str, db: Session, current_user: User) -> Share:
    share = db.query(Share).filter(and_(Share.url == url, Share.user_id == current_user.id)).first()

    if share is None:
        raise HTTPException(status_code=404, detail='Share not found')

    combined_data = f"{name}\n{url}"

    image_qr = qr.QRCode(
        error_correction=qr.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    image_qr.add_data(combined_data)
    image_qr.make(fit=True)

    qr_code_data = image_qr.make_image(fill_color="black", back_color="white")
    qr_code_data = qr_code_data.get_image()  # 

    cloudinary_response = cloudinary.uploader.upload(qr_code_data.to_file(), folder="qr_codes")
    image_url = cloudinary_response["secure_url"]

    share.image_qr = image_url

    db.commit()
    db.refresh(share)

    return qr_code_data# qr_code_data.print_ascii(tty=True, invert=True)


async def get_share_by_id(share_id: int, db: Session) -> Share:
    share = db.query(Share).filter(Share.id == share_id)
    return share


