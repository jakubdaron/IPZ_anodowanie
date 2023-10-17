import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit
from PyQt5.uic import loadUi  # Zmieniony sposób wczytywania interfejsu użytkownika
from PyQt5.QtCore import pyqtSignal, QObject, QEventLoop, QTimer, Qt

class Communicate(QObject):
    buttonClicked = pyqtSignal()

class MainWindow(QMainWindow):
    def __init__(self, ui_file, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint)
        self.ui_file = ui_file
        self.communicate = Communicate()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.load_ui()
        self.add_button_handler()

    def load_ui(self):
        loadUi(self.ui_file, self)

    def add_button_handler(self):
        button = self.findChild(QPushButton, "pushButton_2")
        button_2 = self.findChild(QPushButton, "pushButton")

        if button_2:
            button_2.clicked.connect(self.handle_button_click_2)
        if button:
            button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        self.communicate.buttonClicked.emit()

    def handle_button_click_2(self):
        self.communicate.buttonClicked.emit()
        sys.exit(0)

class PromptWindow(QWidget):
    def __init__(self, ui_file, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint)
        self.ui_file = ui_file
        self.communicate = Communicate()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.load_ui()
        self.add_button_handler()

    def load_ui(self):
        loadUi(self.ui_file, self)

    def add_button_handler(self):
        button = self.findChild(QPushButton, "pushButton")
        if button:
            button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        self.communicate.buttonClicked.emit()

class ProcessWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Inicjalizacja widżetu
        self.window = QWidget()

        # Wczytywanie okna procesu
        loadUi("window6.ui", self)

        # Pokazanie okna
        self.show()

def signal_check():
    return True

def wait_for_signal(win_sel):
    event_loop = QEventLoop()
    win_sel.communicate.buttonClicked.connect(event_loop.quit)
    event_loop.exec_()

def wait_for_timer():
    event_loop = QEventLoop()
    timer = QTimer()
    timer.timeout.connect(event_loop.quit)
    timer.start(5000)
    event_loop.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    signal = signal_check()

    if signal == False:
        win2 = PromptWindow('window1.ui')
        win2.communicate.buttonClicked.connect(app.quit)
        wait_for_signal(win2)
        sys.exit()

    while True:
        try:
            win = MainWindow('mainwindow.ui')
            wait_for_signal(win)
            win.setEnabled(False)

            le = win.findChild(QLineEdit, "lineEdit")
            le2 = win.findChild(QLineEdit, "lineEdit_2")
            force = float(le.text())
            cycles = int(le2.text())

            if not (0.5 <= force <= 5.0) or not (1 <= cycles <= 12):
                raise ValueError("Nieprawidłowe wartości force lub cycles")

            print("force:", force)
            print("cycles:", cycles)

            win2 = ProcessWindow()
            wait_for_timer()
            win2.close()

            win2 = PromptWindow('window4.ui')
            wait_for_signal(win2)
            win2.close()

            win2 = ProcessWindow()
            wait_for_timer()
            win2.close()

            win2 = PromptWindow('window3.ui')
            wait_for_signal(win2)
            win2.close()

            win2 = ProcessWindow()
            wait_for_timer()
            win2.close()

            win.setEnabled(True)

        except ValueError as e:
            print("Błąd:", e)
            win2 = PromptWindow('window2.ui')
            wait_for_signal(win2)
            win2.close()
            continue  # Rozpocznij pętlę while od nowa w przypadku błędu

    sys.exit(app.exec())