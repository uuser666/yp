
from sqlalchemy import false

from base import card_holder, check_card_exists, check_user_exists, create_user,password_from_db
from schemas import User_full_data, loginfo
from werkzeug.security import check_password_hash, generate_password_hash



def create_m(us_date: User_full_data):
    if check_user_exists(us_date.login):
        return "Логин занят, попробуйте другой"
    elif not check_card_exists(us_date.card):
        return "Регистрация не успешна, а ваша карта не действительна"
    elif card_holder(us_date.card):
         return "Негодяй, не твоя это карта"
    else:
        us_date.password = generate_password_hash(us_date.password)
        create_user(us_date)
        return "Регистрация успешна, вы Богоподобны!"


def log_in(log : loginfo):
    password = password_from_db(log.login)
    if password:
        if check_password_hash(password, log.passr):
            return True
        else: return False
    else: return False