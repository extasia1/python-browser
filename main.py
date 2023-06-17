import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class PyBrowser(QMainWindow):
    DEFAULT_URL = "http://google.com"
    WINDOW_TITLE = "PyBrowser"
    BROWSER_ICON = "browser_icon.png"

    def __init__(self, *args, **kwargs):
        super(PyBrowser, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        """Initializes the user interface."""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowIcon(QIcon(self.BROWSER_ICON))

        self.browser = self.create_browser()
        self.setCentralWidget(self.browser)

        navtb = self.create_toolbar()
        self.addToolBar(navtb)

        self.setStyleSheet("""
            QToolBar { border: none; }
            QLineEdit { padding: 5px; font-size: 14px; }
        """)

        self.show()

    def create_browser(self):
        """Creates and returns a QWebEngineView."""
        browser = QWebEngineView()
        browser.setUrl(QUrl(self.DEFAULT_URL))
        browser.urlChanged.connect(self.update_urlbar)
        browser.loadFinished.connect(self.update_title)
        return browser

    def create_toolbar(self):
        """Creates and returns a QToolBar with navigation buttons and a URL bar."""
        navtb = QToolBar()

        back_btn = QAction("ㅤㅤ←ㅤㅤ", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction("ㅤㅤ→ㅤㅤ", self)
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("ㅤㅤ↺ㅤㅤ", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Enter URL")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        return navtb

    def update_title(self):
        """Updates the window title to reflect the current webpage's title."""
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - {self.WINDOW_TITLE}")

    def navigate_to_url(self):
        """Navigates to the URL entered in the URL bar."""
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("https")
        self.browser.setUrl(q)

    def update_urlbar(self, q):
        """Updates the URL bar to reflect the current webpage's URL."""
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.Button, QColor(225, 225, 225))
    app.setPalette(palette)

    window = PyBrowser()
    app.exec_()
