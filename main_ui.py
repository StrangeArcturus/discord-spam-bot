import psutil
import multitasking

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog

from ui.main_window import Ui_MainWindow
from ui.check_pass import Ui_Dialog as UiPassDialog
from ui.token_edit import Ui_Dialog as UiTokenDialog
from ui.chats_ids_edit import Ui_Dialog as UiChatsDialog

from env import config as last_config
from funcs import check_key_on_pretty

import sys
# from time import sleep

import signal
import traceback
from os import name


class PassDialog(UiPassDialog, QDialog):
    def __init__(self, parent: QWidget, my_parent: QMainWindow) -> None:
        super().__init__(parent)
        self.initUI()
        self.status = None
        self.real_parent = my_parent
    
    def initUI(self) -> None:
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.show()
    
    def reject(self) -> None:
        super().reject()
    
    def accept(self) -> None:
        super().accept()
        user_key = self.key_lineEdit.text()
        if check_key_on_pretty(user_key):
            self.real_parent.status_label.setText("Пароль верный, запуск ботов")
            self.real_parent.status_label.setStyleSheet("background-color: cyan;")
            self.status = True
        else:
            self.real_parent.status_label.setText("Пароль неверный")
            self.real_parent.status_label.setStyleSheet("background-color: red;")
            self.status = False


class ChatsDialog(UiChatsDialog, QDialog):
    def __init__(self, parent: QWidget, chats_path: str) -> None:
        super().__init__(parent)
        self.set_chats_ids_path(chats_path)
        self.initUI()
    
    def initUI(self) -> None:
        self.setupUi(self)
        with open(self.chats_path, 'r', encoding='utf-8') as file:
            self.chatsEdit.setPlainText(file.read())
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.show()
    
    def set_chats_ids_path(self, path=last_config["CHATS"]) -> None:
        self.chats_path = path
    
    def accept(self) -> None:
        super().accept()
        with open(self.chats_path, 'w', encoding='utf-8') as file:
            file.write(self.chatsEdit.toPlainText())
        print("OK clicked")
        #self.done(0)
    
    def reject(self) -> None:
        super().reject()
        print("Cancel")
        #self.done(-1)


class TokenDialog(UiTokenDialog, QDialog):
    def __init__(self, parent: QWidget, token_path: str) -> None:
        super().__init__(parent)
        self.set_token_path(token_path)
        self.initUI()

    def initUI(self) -> None:
        self.setupUi(self)
        with open(self.token_path, 'r', encoding='utf-8') as file:
            self.tokensEdit.setPlainText(file.read())

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.show()
    
    def set_token_path(self, path=last_config["TOKENS"]) -> None:
        self.token_path = path
    
    def accept(self) -> None:
        super().accept()
        with open(self.token_path, 'w', encoding='utf-8') as file:
            file.write(self.tokensEdit.toPlainText())
        print("OK clicked")
        #self.done(0)
    
    def reject(self) -> None:
        super().reject()
        print("Cancel")
        #self.done(-1)


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, bots_function) -> None:
        super().__init__()
        self.bots_function = bots_function
        self.initUI()
    
    def initUI(self) -> None:
        self.setupUi(self)
        self.setWindowIcon(QIcon('./ui/discord_img.png'))

        token_file = self.token_lineEdit.text()
        token_file_button_text = self.edit_token_file_button.text().format(token_file)
        self.edit_token_file_button.setText(token_file_button_text)

        chats_file = self.chats_lineEdit.text()
        chats_file_button_text = self.edit_ids_file_button.text().format(chats_file)
        self.edit_ids_file_button.setText(chats_file_button_text)

        self.saveButton.clicked.connect(self._click_save_button)
        self.edit_token_file_button.clicked.connect(self._click_edit_token_button)
        self.edit_ids_file_button.clicked.connect(self._click_edit_chats_button)
        self.start_bots_button.clicked.connect(self._click_start_button)

        self.show()
    
    def _click_save_button(self) -> None:
        config = self.get_config_from_ui()
        data = [
            f"{key} = {repr(value)}" for key, value in config.items()
        ]
        with open('./env.env', 'w', encoding='utf-8') as file:
            file.write('\n'.join(data))
        with open('./config_vars.py', 'w', encoding='utf-8') as file:
            file.write('\n'.join(data))

        token_file = self.token_lineEdit.text()
        token_file_button_text = self.edit_token_file_button.text().split()[0] + f' {token_file}'
        self.edit_token_file_button.setText(token_file_button_text)

        chats_file = self.chats_lineEdit.text()
        chats_file_button_text = self.edit_ids_file_button.text().split()[0] + f' {chats_file}'
        self.edit_ids_file_button.setText(chats_file_button_text)

        self.status_label.setText("Данные успешно сохранены!")
        self.status_label.setStyleSheet("background-color: cyan")
    
    def _click_start_button(self) -> None:
        self.status_label.setText((
            "Данные успешно подготовлены, запуск приложения в консоли немедленно после проверки пароля.\n"
            "Для закрытия: 1. закрыть окно, 2. Ctrl+C в консоли дважды."
        ))
        self.status_label.setStyleSheet("background-color: cyan")
        pass_dialog = PassDialog(self, self)
        pass_dialog.exec()
        if pass_dialog.status == True:
            self.bots_function()
            self.showMinimized()
    
    def _click_edit_token_button(self) -> None:
        edit_token_window = TokenDialog(self, self.token_lineEdit.text())
        edit_token_window.exec()
    
    def _click_edit_chats_button(self) -> None:
        edit_chats_window = ChatsDialog(self, self.chats_lineEdit.text())
        edit_chats_window.exec()
    
    def get_config_from_ui(self) -> dict:
        config = {
            "TOKENS": self.token_lineEdit.text(),
            "CHATS": self.chats_lineEdit.text(),
            "TG_TOKEN": last_config["TG_TOKEN"],
            "MY_TG_ID": self.tg_id_lineEdit.text(),
            "TYPING_MESSAGE_TIME": self.typing_msg_time_lineEdit.text(),
            "IS_DELETING": self.is_deleting_lineEdit.text(),
            "DELETING_DELAY": self.deleting_delay_lineEdit.text(),
            "ANSWER_CHANCE": self.answer_chance_lineEdit.text(),
            "LOGGING_FILE": self.logging_file_lineEdit.text(),
            "TEMPORARY_BOTS_NAMES": last_config["TEMPORARY_BOTS_NAMES"],
            "TEMPORARY_MESSAGE_ID_PATH": last_config["TEMPORARY_MESSAGE_ID_PATH"]
        }
        return config


def kill_me(self, cls):
    #process_name = "python main.py" if name == 'nt' else "python3 main.py"
    process_name = f"python{'' if name == 'nt' else '3'} {__file__}"
    try:
        print(f'Killing processes {process_name}')
        processes = psutil.process_iter()
        for process in processes:
            try:
                print(f'Process: {process}')
                print(f'id: {process.pid}')
                print(f'name: {process.name()}')
                print(f'cmdline: {process.cmdline()}')
                #if process_name == process.name() or process_name in process.cmdline():
                if process_name == ' '.join(process.cmdline()):
                    print(f'found {process.name()} | {process.cmdline()}')
                    process.terminate()
            except Exception:
                print(f"{traceback.format_exc()}")

    except Exception:
        print(f"{traceback.format_exc()}")
    finally:
        multitasking.killall(self, cls)
        exit()


signal.signal(signal.SIGINT, kill_me)


def start_gui(bots_function=lambda: None):
    app = QApplication(sys.argv)
    window = MainWindow(bots_function)

    sys.exit(app.exec_())


if __name__ == "__main__":
    start_gui()
