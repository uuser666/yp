from logging import PlaceHolder
import sys

from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QPushButton, QStackedWidget, QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from api import create_m, log_in
from base import card_holder, get_usr
from schemas import User_data, User_full_data, loginfo


class AuthDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация / Регистрация")
        self.setFixedSize(400, 350)  


        self.stack = QStackedWidget()
        
     
        self.login_page = self.create_login_ui()
        self.register_page = self.create_register_ui()
        
        self.stack.addWidget(self.login_page)    
        self.stack.addWidget(self.register_page) 
        
   
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def create_login_ui(self):
        
        page = QWidget()
        layout = QVBoxLayout()
        
        self.label = QLabel("Введите данные для входа:")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("Пароль")
        
        self.btn_login = QPushButton("Войти")
        self.btn_login.clicked.connect(self.handle_login)
        
        # Синяя ссылка для перехода к регистрации
        self.btn_to_reg = QLabel("Регистрация")
        self.btn_to_reg.setStyleSheet("color: blue; text-decoration: underline;")
        self.btn_to_reg.setCursor(Qt.CursorShape.PointingHandCursor)
        # При клике меняем индекс стека на 1 (регистрация)
        self.btn_to_reg.mousePressEvent = lambda ev: self.stack.setCurrentIndex(1)
        
        layout.addWidget(self.label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_to_reg, alignment=Qt.AlignmentFlag.AlignLeft)
        
        page.setLayout(layout)
        return page

    def create_register_ui(self):
        
        page = QWidget()
        layout = QVBoxLayout()
        form = QFormLayout()
        
        self.label1 = QLabel("Введите данные для регистрации:")
        
        self.reg_fio = QLineEdit()
        form.addRow("ФИО:", self.reg_fio)

        self.reg_login = QLineEdit()
        form.addRow("Логин:", self.reg_login)

        self.reg_pass = QLineEdit()
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Пароль:", self.reg_pass)

        self.reg_card = QLineEdit() 
        form.addRow("Читательский билет:", self.reg_card)
        
        btn_do_register = QPushButton("Зарегистрироваться")
        btn_do_register.clicked.connect(self.handle_registr)

       
        self.btn_to_login = QLabel("Назад к авторизации")
        self.btn_to_login.setStyleSheet("color: blue; text-decoration: underline;")
        self.btn_to_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_to_login.mousePressEvent = lambda ev: self.stack.setCurrentIndex(0)

        layout.addWidget(self.label1)
        layout.addLayout(form)
        layout.addWidget(btn_do_register)
        layout.addWidget(self.btn_to_login, alignment=Qt.AlignmentFlag.AlignLeft)
        
        page.setLayout(layout)
       
        

        return page

    def handle_login(self):
            
        if log_in(loginfo(login = self.login_input.text(),passr=self.pass_input.text())):
            
            self.accept()  
        else:
            self.label.setText("Ошибка: неправильный логин или пароль")

    def handle_registr(self):
        
            new_user = User_full_data(
            fio=self.reg_fio.text(),
            login=self.reg_login.text(),
            password=self.reg_pass.text(),
            card=self.reg_card.text()
        )
            
            self.label1.setText( create_m(new_user))
    def get_data(self) -> User_data:
        ex_u = get_usr(self.login_input.text())
        user = User_data(fullname=ex_u.user_fullname,group=ex_u.user_group,card= card_holder(ex_u.user_login) )  # pyright: ignore[reportOptionalMemberAccess]
        return user
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("брутальная ЭБС")
        self.setFixedSize(1024,700)
        self.setStyleSheet("""
            MainWindow {
                background-image: url('background.jpg'); 
                background-repeat: no-repeat;
                background-position: center;
            }
        """)
        self.show()
        self.open_auth()


    def open_auth(self):
        auth = AuthDialog()

        if auth.exec() == QDialog.DialogCode.Accepted:
            self.User = auth.get_data()
            self.setEnabled(True) 
            self.interface()
        else:
            print("Окно закрыто, выход из приложения")
            sys.exit() 


    def interface(self):
        # Основной виджет и слой
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Создаем вкладки для разных ролей
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # --- 1. ВКЛАДКА КАТАЛОГ (Для всех) ---
        self.catalog_tab = QWidget()
        self.setup_catalog_ui()
        self.tabs.addTab(self.catalog_tab, "Каталог книг")

        # --- 2. ВКЛАДКА МОИ КНИГИ ---
        self.my_books_tab = QWidget()
        self.setup_my_books_ui()
        self.tabs.addTab(self.my_books_tab, "Мои книги")

        # --- 3. ПАНЕЛЬ БИБЛИОТЕКАРЯ  ---
        
        if self.User.group <2: 
            self.librarian_tab = QWidget()
            self.setup_librarian_ui()
            self.tabs.addTab(self.librarian_tab, "Панель библиотекаря")

        # --- 4. ПАНЕЛЬ АДМИНИСТРАТОРА  ---
        
        if self.User.group <1: 
            self.admin_tab = QWidget()
            self.setup_admin_ui()
            self.tabs.addTab(self.admin_tab, "Админ-панель")

    def setup_catalog_ui(self):
        layout = QVBoxLayout(self.catalog_tab)
        self.catalog_table = QTableWidget(0, 5)
        self.catalog_table.setHorizontalHeaderLabels(["Название", "Жанр", "Дата", "Автор", "Действие"])
        self.catalog_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # pyright: ignore[reportOptionalMemberAccess]

        
        layout.addWidget(QLabel("Доступные книги:"))
        layout.addWidget(self.catalog_table)

    def setup_my_books_ui(self):
        layout = QVBoxLayout(self.my_books_tab)
        self.my_books_table = QTableWidget(0, 5)
        self.my_books_table.setHorizontalHeaderLabels(["Название", "Жанр", "Дата", "Автор", "Действие"])
        self.my_books_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # pyright: ignore[reportOptionalMemberAccess]
        
        layout.addWidget(QLabel("Ваши книги:"))
        layout.addWidget(self.my_books_table)

    def setup_librarian_ui(self):
        layout = QVBoxLayout(self.librarian_tab)
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить книгу")
        edit_btn = QPushButton("Редактировать")
        del_btn = QPushButton("Удалить книгу")
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(del_btn)
        
        self.lib_table = QTableWidget(0, 4)
        self.lib_table.setHorizontalHeaderLabels(["Название", "Жанр", "Дата", "Автор"])
        self.lib_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # pyright: ignore[reportOptionalMemberAccess]
        
        layout.addLayout(btn_layout)
        layout.addWidget(self.lib_table)

    def setup_admin_ui(self):
        layout = QVBoxLayout(self.admin_tab)
        
        # Заголовок
        admin_label = QLabel("Управление пользователями и билетами")
        admin_label.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        layout.addWidget(admin_label)

        # Таблица пользователей
        self.user_table = QTableWidget(0, 3)
        self.user_table.setHorizontalHeaderLabels(["Логин", "ФИО", "Номер билета"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # pyright: ignore[reportOptionalMemberAccess]
      
        
        layout.addWidget(self.user_table)

       
        ctrl_layout = QHBoxLayout()
        
        self.delete_user_btn = QPushButton("Удалить выбранного пользователя")
        self.delete_user_btn.setStyleSheet("background-color: #c0392b; color: white; padding: 5px;")
        self.delete_user_btn.clicked.connect(self.delete_selected_user)

        self.add_ticket_btn = QPushButton("Выдать новый чит. билет")
        self.add_ticket_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 5px;")
        self.add_ticket_btn.clicked.connect(self.add_ticket_logic)

        ctrl_layout.addWidget(self.delete_user_btn)
        ctrl_layout.addWidget(self.add_ticket_btn)
        
        layout.addLayout(ctrl_layout)

    def add_user_to_table(self, login, name, ticket):
        row = self.user_table.rowCount()
        self.user_table.insertRow(row)
        self.user_table.setItem(row, 0, QTableWidgetItem(login))
        self.user_table.setItem(row, 1, QTableWidgetItem(name))
        self.user_table.setItem(row, 2, QTableWidgetItem(ticket))

    def delete_selected_user(self):
        current_row = self.user_table.currentRow()
        if current_row > -1:
            
            login = self.user_table.item(current_row, 0).text() # pyright: ignore[reportOptionalMemberAccess]
            self.user_table.removeRow(current_row)
            print(f"Пользователь {login} удален из системы")
        else:
            print("Никто не выбран")

    def add_ticket_logic(self):

        row = self.user_table.rowCount()
        self.user_table.insertRow(row)
        self.user_table.setItem(row, 2, QTableWidgetItem("НОВЫЙ-БИЛЕТ"))
        print("Создана запись для нового читательского билета")