from sqlalchemy.orm import Session

from src.database.models import User, Share
from schemas import ShareRequest




# create
async def create_share(share: ShareRequest, db: Session, current_user: User) -> Share:
    pass

# read
async def get_list_shares_for_user(iser_id: int) -> list:
    pass

# update
async def update_share(share: ShareRequest, db: Session, current_user: User) -> Share:
    pass

# delete
async def delete_share() -> None:
    pass
