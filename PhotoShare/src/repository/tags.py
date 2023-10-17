from sqlalchemy.orm import Session
from sqlalchemy import text, and_

from src.database.models import Tag
from schemas import TagRequest
import re



def extract_tags(text):
    # Використовуйте регулярний вираз для вилучення тегів, які починаються з "#" та закінчуються пробілом
    tags = re.findall(r'#\w+', text)
    return tags



# Функція для отримання тега за іменем
def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()



# Функція для створення нового тега
def create_tag(db: Session, tag: TagRequest):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
