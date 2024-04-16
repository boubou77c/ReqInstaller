import threading
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QLineEdit,QPushButton,QGridLayout,QFileDialog
from PyQt5 import QtGui,uic
import os

class Window(QMainWindow):
    #Initialize the constructor
    def __init__(self):
        super().__init__()
        self.init_Ui()

    def init_Ui(self):
        #Load the UI
        ui = uic.loadUi('reqinstaller.ui',self)
        #set window name
        self.setWindowTitle('ReqInstaller-Boubou')
        #Set fixed sized
        self.setFixedSize(442,536)
        #Set icon
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        #Set custom font for the title
        font_path = os.path.join("font","Anton-Regular.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)
        custom_font = QtGui.QFont("Anton")
        custom_font.setPointSize(52)
        custom_font.setUnderline(True)

        #Get the button,label and more
        self.file_state = ui.findChild(QLabel,'file_state')

        #GRID / editLine / But file dialog
        self.grid = ui.findChild(QGridLayout,"gridLayout")
        self.fdial_but = ui.findChild(QPushButton,"put_path_but")
        self.edit_line = ui.findChild(QLineEdit,"lineEdit")

        #But download / label_state
        self.but_dl = ui.findChild(QPushButton,"but_dl")
        self.state_lb = ui.findChild(QLabel,"state_lb")

        #Add a custom font for the title
        title = ui.findChild(QLabel,"title")
        title.setFont(custom_font)


        #Connect the methods to the but
        self.fdial_but.clicked.connect(self.load_path)

        self.get_path = ""

        self.but_dl.clicked.connect(lambda: self.thread_download_rq(self.get_path))


    #Load the requierements.txt path
    def load_path(self) -> bool:
        # _ : -> catch the file filter value
        self.file_name,_ = QFileDialog.getOpenFileName(self,directory="",caption="Open requirements.txt",filter="*.txt")

        #If it exists -> Change the edit line with it
        if self.file_name:
            self.edit_line.setText(self.file_name)
            self.file_state.setText("File exists : Yes")
            return True
        #Else, show an error
        else:
            self.file_state.setText("File exists : No")
            return False


    def thread_download_rq(self,path:str):
        #Get the text in the lineedit
        path = self.edit_line.text()
        #Create a threade
        thread_dl = threading.Thread(target=self.dl_console_rq, args=(path,))
        start = thread_dl.start()


    def dl_console_rq(self,path:str) -> bool:
        # Command to install the requirements
        req_cmd = f"pip install -r \"{path}\""
        # run the command
        self.state_lb.setText("Downloading...")
        print("Running command:", req_cmd)
        install = os.system(req_cmd)
        print("Install result:", install)
        #If it is downloaded -> print finished
        if (install == 0):
            self.state_lb.setText("Downloaded successfully !")
            return True
        # else -> error
        else:
            self.state_lb.setText("Download -rq Error")
            return False



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())