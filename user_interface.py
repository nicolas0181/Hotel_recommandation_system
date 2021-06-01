from PyQt5.QtGui import QFont
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QCompleter, QRadioButton, QPushButton, QWidget, QVBoxLayout, QLineEdit, QLabel
from content_based_algorithm import content_recommender as contentBasedML
from content_based_algorithm import pickle_model as contentBasedTrainedModel
from content_based_algorithm import get_hotels
from user_based_algorithm import predict_recommanded
from user_based_algorithm import get_users

class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.setGeometry(600, 400, 600, 400)
        self.initUI()

    def initUI(self):
        self.indices, self.cosine_sim, self.df_hotels = contentBasedTrainedModel()
        list_users = get_users()
        completer_users = QCompleter(list_users)
        completer_users.setCaseSensitivity(0)
        list_hotels = get_hotels()
        completer_hotels = QCompleter(list_hotels)
        completer_hotels.setCaseSensitivity(0)

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Collaborative Filtering")
        self.tabs.addTab(self.tab2, "Content Based")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setCentralWidget(self.tabs)

        #  ==================================================
        self.tab1.layout = QVBoxLayout(self)


        self.button_user = QRadioButton("User based")
        self.button_user.setChecked(True)
        self.tab1.layout.addWidget(self.button_user)

        self.button_item = QRadioButton("Item based")
        self.tab1.layout.addWidget(self.button_item)

        self.userLabel = QLabel(self)
        self.userLabel.setText("Nom de l'user: ")
        self.tab1.layout.addWidget(self.userLabel)

        self.inputUser = QLineEdit(self)
        self.inputUser.setCompleter(completer_users)
        self.tab1.layout.addWidget(self.inputUser)

        self.b1 = QPushButton("OK", self)
        self.b1.clicked.connect(self.clikedUser)
        self.tab1.layout.addWidget(self.b1)

        self.best_hotels_title = QLabel(self)
        self.best_hotels_title.setText("")
        self.best_hotels_title.setFont(QFont('Arial', 17))
        self.best_hotels_title.move(10, 80)
        self.tab1.layout.addWidget(self.best_hotels_title)

        self.hotel1 = QLabel(self)
        self.hotel1.setText("")
        self.hotel1.move(10, 120)
        self.tab1.layout.addWidget(self.hotel1)

        self.hotel2 = QLabel(self)
        self.hotel2.setText("")
        self.hotel2.move(10, 150)
        self.tab1.layout.addWidget(self.hotel2)

        self.hotel3 = QLabel(self)
        self.hotel3.setText("")
        self.hotel3.move(10, 180)
        self.tab1.layout.addWidget(self.hotel3)

        self.hotel4 = QLabel(self)
        self.hotel4.setText("")
        self.hotel4.move(10, 210)
        self.tab1.layout.addWidget(self.hotel4)

        self.hotel5 = QLabel(self)
        self.hotel5.setText("")
        self.hotel5.move(10, 240)
        self.tab1.layout.addWidget(self.hotel5)

        self.tab1.setLayout(self.tab1.layout)

        #  ==================================================
        self.tab2.layout = QVBoxLayout(self)

        self.hotelLabel = QLabel(self)
        self.hotelLabel.setText("Nom de l'hôtel: ")
        self.hotelLabel.move(10, 30)
        self.tab2.layout.addWidget(self.hotelLabel)

        self.inputHotel = QLineEdit(self)
        self.inputHotel.move(120, 30)
        self.inputHotel.setCompleter(completer_hotels)
        self.tab2.layout.addWidget(self.inputHotel)

        self.b2 = QPushButton("OK", self)
        self.b2.clicked.connect(self.clikedContent)
        self.b2.move(250, 30)
        self.tab2.layout.addWidget(self.b2)

        self.best_hotels2_title = QLabel(self)
        self.best_hotels2_title.setText("")
        self.best_hotels2_title.setFont(QFont('Arial', 17))
        self.best_hotels2_title.move(10, 80)
        self.tab2.layout.addWidget(self.best_hotels2_title)

        self.hotel21 = QLabel(self)
        self.hotel21.setText("")
        self.hotel21.move(10, 120)
        self.tab2.layout.addWidget(self.hotel21)

        self.hotel22 = QLabel(self)
        self.hotel22.setText("")
        self.hotel22.move(10, 150)
        self.tab2.layout.addWidget(self.hotel22)

        self.hotel23 = QLabel(self)
        self.hotel23.setText("")
        self.hotel23.move(10, 180)
        self.tab2.layout.addWidget(self.hotel23)

        self.hotel24 = QLabel(self)
        self.hotel24.setText("")
        self.hotel24.move(10, 210)
        self.tab2.layout.addWidget(self.hotel24)

        self.hotel25 = QLabel(self)
        self.hotel25.setText("")
        self.hotel25.move(10, 240)
        self.tab2.layout.addWidget(self.hotel25)

        self.tab2.setLayout(self.tab2.layout)


    def clikedUser(self):
        base = "user"
        if self.button_user.isChecked() == True:
            base = "user"

        if self.button_item.isChecked() == True:
            base = "item"
        list_hotels = predict_recommanded(self.inputUser.text(), 5, base)

        self.best_hotels_title.setText("Les meilleurs suggestions d'hôtels pour " + self.inputUser.text())
        self.best_hotels_title.adjustSize()

        self.hotel1.setText("1 - " + list_hotels[0])
        self.hotel1.adjustSize()

        self.hotel2.setText("2 - " + list_hotels[1])
        self.hotel2.adjustSize()

        self.hotel3.setText("3 - " + list_hotels[2])
        self.hotel3.adjustSize()

        self.hotel4.setText("4 - " + list_hotels[3])
        self.hotel4.adjustSize()

        self.hotel5.setText("5 - " + list_hotels[4])
        self.hotel5.adjustSize()
        
    def clikedItem(self):
        list_hotels = predict_recommanded(self.inputUser.text(), 5, self.base)

        self.best_hotels_title.setText("Les meilleurs suggestions d'hôtels pour " + self.inputUser.text())
        self.best_hotels_title.adjustSize()

        self.hotel1.setText("1 - " + list_hotels[0])
        self.hotel1.adjustSize()

        self.hotel2.setText("2 - " + list_hotels[1])
        self.hotel2.adjustSize()

        self.hotel3.setText("3 - " + list_hotels[2])
        self.hotel3.adjustSize()

        self.hotel4.setText("4 - " + list_hotels[3])
        self.hotel4.adjustSize()

        self.hotel5.setText("5 - " + list_hotels[4])
        self.hotel5.adjustSize()

    def clikedContent(self):
        list_hotels, dest = contentBasedML(self.inputHotel.text(), 5, self.indices, self.cosine_sim, self.df_hotels)
        list_hotels = list_hotels.to_list()
        dest = dest.to_list()

        self.best_hotels2_title.setText("Les meilleurs suggestions d'hôtels pour " + self.inputHotel.text())
        self.best_hotels2_title.adjustSize()

        self.hotel21.setText("1 - " + list_hotels[0] + ", " + dest[0])
        self.hotel21.adjustSize()

        self.hotel22.setText("2 - " + list_hotels[1] + ", " + dest[1])
        self.hotel22.adjustSize()

        self.hotel23.setText("3 - " + list_hotels[2] + ", " + dest[2])
        self.hotel23.adjustSize()

        self.hotel24.setText("4 - " + list_hotels[3] + ", " + dest[3])
        self.hotel24.adjustSize()

        self.hotel25.setText("5 - " + list_hotels[4] + ", " + dest[4])
        self.hotel25.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
