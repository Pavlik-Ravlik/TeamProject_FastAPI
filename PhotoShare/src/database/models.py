from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship


Base = declarative_base()


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), unique=True)
    share_id = Column('shares_id', ForeignKey('shares.id', ondelete='CASCADE'), default=None)
    share = relationship('Share', backref='tags')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    share_id = Column('shares_id', ForeignKey('shares.id', ondelete='CASCADE'), default=None)
    share = relationship('Share', backref='comments')
    user_id = Column('users_id', ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', backref='users')



class Share(Base):
    __tablename__ = 'shares'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    image_qr = Column(String, index=True, nullable=True)
    description = Column(String, index=True, nullable=False)
    tags = Column(String, index=True, nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    comment_id = Column('comments_id', ForeignKey('comments.id', ondelete='CASCADE'))
    comment = relationship('Comment', backref='comments')
    user_id = Column('users_id', ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', backref='shares')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
    role = Column(String, index=True, default='user')
    confirmed = Column(Boolean, default=False)
