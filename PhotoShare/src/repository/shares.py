from sqlalchemy.orm import Session

from src.database.models import User, Share
from schemas import ShareRequest





async def create_share(share: ShareRequest, db: Session, current_user: User) -> Share:
    pass