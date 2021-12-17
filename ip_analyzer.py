from PyQt5 import QtWidgets, QtCore
import os
import pandas as pd
import ipwhois
import webbrowser
from pandasmodel import PandasModel
from gui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.ip_col = 'ipAddress'
        self.df = pd.DataFrame()
        self.df2 = pd.DataFrame(columns=['count', 'location', '%', 'matching digits'])
        self.df3 = pd.DataFrame(columns=['count', 'location', '%'])
        self.format_tables()
        self.tableView.setColumnWidth(3, 250)

        self.lineEdit.textChanged.connect(self.compare_ips)
        self.checkBox.clicked.connect(self.dark_mode)
        self.pushButton.clicked.connect(self.browse_file)
        self.pushButton_2.clicked.connect(self.scamalytics)
        self.pushButton_3.clicked.connect(self.whois)


    def browse_file(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dlg.exec_()
        filepath = dlg.selectedFiles()
        if not filepath:
            return
        else:
            self.df1 = pd.read_csv(filepath[0])
            self.df2 = self.group_by_ip(self.df1)
            self.df2['%'] = (100 * self.df2['count'] / len(self.df1)).astype('float64').round(2)
            self.df3 = pd.DataFrame(self.df1.groupby('Location').count()['Date Created'])
            self.df3.columns = ['count']
            self.df3.sort_values(by='count', ascending=False, inplace=True)
            self.df3['%'] = (100 * self.df3['count'] / len(self.df1)).round(2)
            self.df2.columns = ['count', 'location', '%']
            self.df2['matching digits'] = 0
            self.display_ip_table()
            self.display_loc_table()

    def group_by_ip(self, df):
        return pd.DataFrame(df.groupby(self.ip_col).describe()['Location'][['count', 'top']])

    def display_ip_table(self):
        self.tableView.setModel(PandasModel(self.df2))
        self.tableView.setColumnWidth(3, 220)

    def display_loc_table(self):
        self.tableView_2.setModel(PandasModel(self.df3))

    def format_tables(self):
        for table in [self.tableView, self.tableView_2]:
            table.setAlternatingRowColors(True)
            table.setSortingEnabled(True)
            table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def set_ip_col(self):
        self.ip_col = self.comboBox.currentText()

    def compare_ips(self):
        ip = self.lineEdit.text()
        self.df2['matching digits'] = list(map(lambda x: self.matching_digits(ip, x), self.df2.index))
        self.display_ip_table()


    @staticmethod
    def matching_digits(ip1, ip2):
        n_digits = 0
        ip11, ip22 = tuple(map(lambda x: x.replace('.', ''), [ip1, ip2]))
        for x1, x2 in zip(list(ip11), list(ip22)):
            if x1 == x2:
                n_digits += 1
            else:
                break
        return n_digits

    def scamalytics(self):
        ip = self.df2.index[self.tableView.currentIndex().row()]
        webbrowser.open(f'https://scamalytics.com/ip/{ip}')

    def whois(self):
        ip = self.df2.index[self.tableView.currentIndex().row()]
        data1 = ipwhois.IPWhois(ip).lookup_rdap()
        data2 = data1.pop('network')
        data3 = data1.pop('objects')
        self.whois_window = QtWidgets.QWidget(parent=None)
        self.whois_window.setWindowTitle('Whois lookup')
        self.whois_window.setGeometry(QtCore.QRect(200, 200, 640, 400))
        self.tabs = QtWidgets.QTabWidget(self.whois_window)
        self.tabs.setGeometry(QtCore.QRect(10, 10, 620, 380))

        for data, title in zip([data1, data2, data3], ['basic', 'network', 'objects']):
            tab = QtWidgets.QWidget(self.tabs)
            tab.setGeometry(QtCore.QRect(0, 0, 600, 360))
            table = QtWidgets.QTableView(tab)
            table.setGeometry(QtCore.QRect(10, 10, 580, 330))
            model = PandasModel(self.dict_to_pandasmodel(data))
            table.setModel(model)
            table.setColumnWidth(0, 460)
            self.tabs.addTab(tab, title)

        self.whois_window.show()

    @staticmethod
    def dict_to_pandasmodel(d):
        return pd.DataFrame(index=d.keys(), columns=['data'], data={'data': d.values()})

    def dark_mode(self):
        self.setStyleSheet("color:rgb(255,255,255);\n"
                           "background-color:rgb(0, 12, 18)")

        self.lineEdit.setStyleSheet("color:rgb(205,255,225);\n"
                           "background-color:rgb(0, 42, 68)")
        for button in [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4]:
            button.setStyleSheet("color:rgb(205,255,225);\n"
                           "background-color:rgb(0, 22, 38)")

        for table in [self.tableView, self.tableView_2]:
            table.setStyleSheet("color:rgb(205,255,225);\n"
                           "background-color:rgb(0, 22, 38);\n"
                            "alternate-background-color:rgb(0, 32, 48);\n"
                            "selection-background-color:rgb(0, 68, 68)")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


