from sqlalchemy.orm import Session

from src.database.models import Tag
import re



def extract_tags(text):
    tags = re.findall(r'#\w+', text)
    return tags


def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).all()


def create_tag(db: Session, description: str) -> Tag:
    exstract = extract_tags(description)
    exist_tag = get_tag_by_name(db, exstract[0])

    if exist_tag:
        return exist_tag
    
    new_tag = Tag(name=exstract[0])
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag
