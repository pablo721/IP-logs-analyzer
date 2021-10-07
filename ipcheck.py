from pandas import DataFrame, read_csv
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QTableView, QPushButton, QMainWindow, QApplication, QFileDialog, QCheckBox, QAbstractItemView
from PyQt5.QtCore import QRect
from pandasmodel import PandasModel
import webbrowser


class IPChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('IP Checker')
        self.df1 = None
        self.df2 = None

        self.resize(654, 800)
        self.frame = QFrame(self)
        self.frame.setGeometry(QRect(0, 0, 654, 800))

        self.ip_label = QLabel(self.frame)
        self.ip_label.setGeometry(QRect(10, 10, 30, 27))
        self.ip_label.setText('IP')

        self.ip_line = QLineEdit(self.frame)
        self.ip_line.setGeometry(QRect(50, 10, 130, 27))

        self.browse_button = QPushButton(self.frame)
        self.browse_button.setGeometry(QRect(10, 45, 80, 27))
        self.browse_button.setText('Browse')

        self.check_button = QPushButton(self.frame)
        self.check_button.setGeometry(QRect(100, 45, 80, 27))
        self.check_button.setText('Check IP')

        self.dark_box = QCheckBox(self.frame)
        self.dark_box.setGeometry(QRect(554, 10, 100, 27))
        self.dark_box.setText('dark mode')

        self.table = QTableView(self.frame)
        self.table.setGeometry(QRect(10, 80, 644, 500))
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table2 = QTableView(self.frame)
        self.table2.setGeometry(QRect(10, 590, 634, 200))
        self.table2.setAlternatingRowColors(True)

        self.browse_button.clicked.connect(self.browse_file)
        self.ip_line.textChanged.connect(lambda: self.check_octets(self.ip_line.text()))
        self.dark_box.clicked.connect(self.dark_mode)
        self.check_button.clicked.connect(self.check_ip2)

    def check_ip2(self):
        ip = self.df2.index[self.table.currentIndex().row()]
        webbrowser.open(f'www.scamalytics.com/ip/{ip}')

    def browse_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.exec_()
        filepath = dlg.selectedFiles()
        if not filepath:
            return
        else:
            self.df1 = read_csv(filepath[0])

            self.df2 = DataFrame(self.df1.groupby('ipAddress').describe()['Location'][['count', 'top']])

            self.df2['%'] = (100 * self.df2['count'] / len(self.df1)).astype('float64').round(2)

            self.df3 = DataFrame(self.df1.groupby('Location').count()['Date Created'])
            self.df3.columns = ['count']
            self.df3.sort_values(by='count', ascending=False, inplace=True)
            self.df3['%'] = (100 * self.df3['count'] / len(self.df1)).round(2)

            ip = self.ip_line.text()

            self.df2['octets matching'] = list(map(lambda x: self.matching_octets(ip, x), self.df2.index))
            self.df2.columns = ['count', 'location', '%', 'octets matching']
            self.table.setModel(PandasModel(self.df2))
            self.table2.setModel(PandasModel(self.df3))

    def check_octets(self, ip):
        if not ip:
            return
        else:
            self.df2['octets matching'] = list(map(lambda x: self.matching_octets(ip, x), self.df2.index))
            self.table.setModel(PandasModel(self.df2))

    @staticmethod
    def matching_octets(ip1, ip2):
        splitted_ip1 = ip1.replace(' ', '').split('.')
        splitted_ip2 = ip2.replace(' ', '').split('.')
        if ip1.replace(' ', '') == ip2.replace(' ', ''):
            return 4
        elif splitted_ip1[:3] == splitted_ip2[:3]:
            return 3
        elif splitted_ip1[:2] == splitted_ip2[:2]:
            return 2
        elif splitted_ip1[0] == splitted_ip2[0]:
            return 1
        else:
            return 0

    def dark_mode(self):
        self.setStyleSheet("color:rgb(255,255,255);\n"
                           "background-color:rgb(0, 12, 18)")

        self.ip_line.setStyleSheet("color:rgb(205,255,225);\n"
                           "background-color:rgb(0, 42, 68)")
        for button in [self.browse_button, self.check_button]:
            button.setStyleSheet("color:rgb(205,255,225);\n"
                           "background-color:rgb(0, 22, 38)")

        for table in [self.table, self.table2]:
            table.setStyleSheet("color:rgb(205,255,225);\n"
                           "background-color:rgb(0, 22, 38);\n"
                            "alternate-background-color:rgb(0, 32, 48);\n"
                            "selection-background-color:rgb(0, 68, 68)")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = IPChecker()
    window.show()
    sys.exit(app.exec_())
