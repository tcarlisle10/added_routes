from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

user_skills = db.Table(
    "user_skills",
    Base.metadata,
    Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    Column("skill_id", db.ForeignKey("skills.id"), primary_key=True),
    Column("proficiency_level", db.String(50), nullable=True)
)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(50), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(db.String(100), nullable=False)
    rating: Mapped[float] = mapped_column(db.Float, default=0)
    created_at: Mapped[datetime] = mapped_column(db.dateTime, default=datetime.utcnow)

    skills: Mapped[List['Skill']] = relationship(secondary=user_skills, back_populates='users')
    listings: Mapped[List['Listing']] = relationship(back_populates='user')
    transactions: Mapped[List['Transaction']] = relationship(back_populates='requestor')
    reviews_given: Mapped[List['Review']] = relationship(foreign_keys='Review.reviewer_id', back_populates='reviewer')
    reviews_received: Mapped[List['Review']] = relationship(foreign_keys='Review.reviewee_id', back_populates='reviewee')

    
class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    description: Mapped[str] = mapped_column(db.String(250), nullable=True)

# many-to-many with users
    users: Mapped[List['User']] = relationship(secondary=user_skills, back_populates='skills')

    
    
class Listing(Base):
    __tablename__ = 'listings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    skill_id: Mapped[int] = mapped_column(db.ForeignKey('skills.id'))
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    description: Mapped[str] = mapped_column(db.String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(db.dateTime, default=datetime.utcnow)

    user: Mapped['User'] = relationship(back_populates='listings')
    skill: Mapped['Skill'] = relationship()

    
class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(db.ForeignKey('listings.id'))
    requester_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    status: Mapped[str] = mapped_column(db.Enum('pending', 'completed', 'cancelled'), default='pending')
    created_at: Mapped[datetime] = mapped_column(db.dateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(db.dateTime, nullable=True)

    listing: Mapped['Listing'] = relationship()
    requester: Mapped['User'] = relationship(back_populates='transactions')

    
    
class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    reviewer_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    reviewee_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    transaction_id: Mapped[int] = mapped_column(db.ForeignKey('transactions.id'))
    rating: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(db.String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(db.dateTime, default=datetime.utcnow)

    reviewer: Mapped['User'] = relationship(foreign_keys=[reviewer_id], back_populates='reviews_given')
    reviewee: Mapped['User'] = relationship(foreign_keys=[reviewee_id], back_populates='reviews_received')
    
class Exchange(Base):
    __tablename__ = 'exchanges'

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(db.ForeignKey('listings.id'))
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    skill_id: Mapped[int] = mapped_column(db.ForeignKey('skills.id'))
    description: Mapped[str] = mapped_column(db.String(255))
    status: Mapped[str] = mapped_column(db.String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.dateTime, default=datetime.utcnow)

    listing: Mapped['Listing'] = relationship()
    user: Mapped['User'] = relationship()
    skill: Mapped['Skill'] = relationship()