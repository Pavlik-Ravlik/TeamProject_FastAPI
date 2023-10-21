from sqlalchemy.orm import Session

from src.database.models import Tag
from schemas import TagRequest
import re



def extract_tags(text):
    tags = re.findall(r'#\w+', text)
    return tags


def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()


def create_tag(db: Session, tag: TagRequest):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
