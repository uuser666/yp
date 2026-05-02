import datetime
from typing import Optional
from datetime import date
from sqlalchemy import  DateTime, ForeignKey, String,LargeBinary
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()

class books(Base):
    __tablename__ = "Books"
    book_id: Mapped[int] = mapped_column(primary_key= True,autoincrement=True)
    book_name: Mapped[str]
    book_author: Mapped[str]
    book_date :Mapped[date]
    book_genre: Mapped[str] = mapped_column(String(19))
    book_assign: Mapped[int] = mapped_column(default=0)

class Users(Base):
    __tablename__ = "Users"
    user_id: Mapped[int] = mapped_column(primary_key= True,autoincrement=True)
    user_fullname: Mapped[str] 
    user_login: Mapped[str] = mapped_column(String(28),unique=True)
    user_group: Mapped[int] = mapped_column(default=2)
    user_pass_h: Mapped[str]
    


class LibraryCard(Base):
        __tablename__ = "Library_cards"
        card_id: Mapped[int] = mapped_column(primary_key= True,autoincrement=True)
        card_name: Mapped[str] = mapped_column(String(18),unique= True)
        user_fid:Mapped[Optional[int]] = mapped_column(ForeignKey("Users.user_id",ondelete="SET NULL"),unique=True,nullable=True,default=None)

class queue(Base):
     __tablename__ = "Queue"
     id: Mapped[int] = mapped_column(primary_key= True,autoincrement=True)
     book_fid:  Mapped[int] = mapped_column(ForeignKey("Library_cards.card_id"))
     user_fid:  Mapped[int] = mapped_column(ForeignKey("Users.user_id"))


    