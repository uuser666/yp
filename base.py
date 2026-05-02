


import re

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from models import LibraryCard, Users
from schemas import User_full_data


engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")


Local = sessionmaker(autoflush=False, autocommit=False, bind=engine)
def get_usr(username : str):
    with Local() as session:
        existing_user = session.query(Users).filter(Users.user_login == username).first()
        if existing_user:
            return existing_user
        
def check_user_exists(username: str) -> bool:

    sql = text('SELECT EXISTS(SELECT 1 FROM "Users" WHERE user_login = :login)')
    
    with Local() as session:

        result = session.execute(sql, {"login": username}).scalar()
        return bool(result)



def create_user(Us: User_full_data):
 
    
    new_user = Users(
        user_fullname=Us.fio,
        user_login=Us.login,
        user_pass_h=Us.password
    )
    
    with Local() as session:
        session.add(new_user)
        session.flush()
        existing_card = session.query(LibraryCard).filter(LibraryCard.card_name == Us.card).first() 
        if existing_card:
            existing_card.user_fid = new_user.user_id



        session.commit()
        
def check_card_exists(cardname: str) -> bool:

    sql = text('SELECT EXISTS(SELECT 1 FROM "Library_cards" WHERE card_name = :login)')
    
    with Local() as session:

        result = session.execute(sql, {"login": cardname}).scalar()
        return bool(result)

def card_holder(cardname: str) -> int|None:
    with Local() as session:
        existing_card = session.query(LibraryCard).filter(LibraryCard.card_name == cardname).first()
        if existing_card:
            return existing_card.user_fid
def password_from_db(username : str):
        U =  get_usr(username)
        if U:
            return U.user_pass_h
        

def create_card(name:str):
    new_card = LibraryCard(card_name = name)
    with Local() as session:
        session.add(new_card)
        session.commit()
        session.refresh(new_card)
        return new_card

if __name__ == "__main__":
    
    print(create_card("олег").card_name)