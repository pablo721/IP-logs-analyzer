import sys

from ipcheck import IPAnalyzer
from PyQt5.QtWidgets import QApplication

def main():
    ip = IPAnalyzer()
    ip.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())