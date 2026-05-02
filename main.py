import sys


from PyQt6.QtWidgets import QApplication

from models import Base
from service import MainWindow


from base import engine

def main():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind = engine)
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec()
    

if __name__ == "__main__":
    main()