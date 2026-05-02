class User_full_data:
    def __init__(self, fio, login, password, card):
        self.fio = fio
        self.login = login
        self.password = password
        self.card = card


class loginfo:
    def __init__(self,login,passr,card = None) -> None:
        self.login = login
        self.passr = passr
        self.card = None


class User_data:
    def __init__(self,fullname,group,card) -> None:
        self.fullname = fullname
        self.group = group
        self.card = card
        
