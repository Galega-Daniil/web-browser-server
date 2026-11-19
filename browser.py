import sys
import os
import platform
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QPushButton, QLineEdit, QComboBox,
    QLabel, QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QProgressBar, QCheckBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DARK_STYLE = """
QMainWindow, QDialog { background-color: #1e1e2e; }
QToolBar { background: #181825; border: none; spacing: 4px; padding: 4px; }
QPushButton {
    background: #313244; color: #cdd6f4; border: none;
    border-radius: 6px; padding: 6px 12px; min-width: 30px;
}
QPushButton:hover { background: #45475a; }
QLineEdit, QComboBox {
    background: #313244; color: #cdd6f4; border: 1px solid #45475a;
    border-radius: 6px; padding: 6px; selection-background-color: #585b70;
}
QTabWidget::pane { border: none; }
QTabBar::tab {
    background: #313244; color: #cdd6f4; padding: 6px 14px;
    border-top-left-radius: 6px; border-top-right-radius: 6px;
    margin-right: 2px; max-width: 220px;
}
QTabBar::tab:selected { background: #45475a; }
QProgressBar { background: #313244; border: none; max-height: 3px; }
QProgressBar::chunk { background: #89b4fa; }
"""


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.resize(420, 200)

        self.js_check = QCheckBox("Включить JavaScript")
        self.img_check = QCheckBox("Загружать изображения")

        layout = QVBoxLayout(self)
        layout.addWidget(self.js_check)
        layout.addWidget(self.img_check)

        close_btn = QPushButton("Готово")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class BrowserTab(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.browser = QWebEngineView()
        s = self.browser.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)

        self.progress = QProgressBar()
        self.progress.setMaximumHeight(3)
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)

        layout.addWidget(self.progress)
        layout.addWidget(self.browser)

        self.browser.loadProgress.connect(self.on_progress)
        self.browser.loadFinished.connect(lambda _: self.progress.setVisible(False))
        self.browser.urlChanged.connect(self.on_url_changed)
        self.browser.titleChanged.connect(self.on_title_changed)

    def on_progress(self, value):
        self.progress.setVisible(0 < value < 100)
        self.progress.setValue(value)

    def on_url_changed(self, url):
        idx = self.window.tabs.indexOf(self)
        if idx >= 0 and self.window.tabs.currentWidget() is self:
            self.window.url_bar.setText(url.toString())

    def on_title_changed(self, title):
        idx = self.window.tabs.indexOf(self)
        if idx >= 0:
            self.window.tabs.setTabText(idx, title[:20] or "Новая вкладка")


class ServerBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Chromium Browser")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, "icon.ico")))

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        self.back_btn = QPushButton("←")
        self.fwd_btn = QPushButton("→")
        self.reload_btn = QPushButton("⟳")
        self.home_btn = QPushButton("⌂")
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите адрес и нажмите Enter")
        self.url_bar.returnPressed.connect(self.navigate)
        self.settings_btn = QPushButton("⚙")

        toolbar.addWidget(self.back_btn)
        toolbar.addWidget(self.fwd_btn)
        toolbar.addWidget(self.reload_btn)
        toolbar.addWidget(self.home_btn)

        url_container = QWidget()
        url_layout = QHBoxLayout(url_container)
        url_layout.setContentsMargins(0, 0, 0, 0)
        url_layout.addWidget(self.url_bar)
        toolbar.addWidget(url_container)

        toolbar.addWidget(self.settings_btn)

        self.back_btn.clicked.connect(lambda: self.current().back())
        self.fwd_btn.clicked.connect(lambda: self.current().forward())
        self.reload_btn.clicked.connect(lambda: self.current().reload())
        self.home_btn.clicked.connect(self.go_home)
        self.settings_btn.clicked.connect(self.open_settings)

        self.add_tab("https://ya.ru")

    def current(self):
        return self.tabs.currentWidget().browser

    def add_tab(self, url="https://ya.ru"):
        tab = BrowserTab(self)
        self.tabs.addTab(tab, "Новая вкладка")
        self.tabs.setCurrentWidget(tab)
        tab.browser.load(QUrl(url))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def navigate(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        if not text.startswith(("http://", "https://")):
            if " " in text or "." not in text:
                text = "https://yandex.ru/search/?text=" + text
            else:
                text = "https://" + text
        self.current().load(QUrl(text))

    def go_home(self):
        self.current().load(QUrl("https://ya.ru"))

    def open_settings(self):
        dlg = SettingsDialog(self)
        s = self.current().settings()
        dlg.js_check.setChecked(s.testAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled))
        dlg.img_check.setChecked(s.testAttribute(
            QWebEngineSettings.WebAttribute.AutoLoadImages))
        if dlg.exec():
            for i in range(self.tabs.count()):
                st = self.tabs.widget(i).browser.settings()
                st.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled,
                                dlg.js_check.isChecked())
                st.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages,
                                dlg.img_check.isChecked())


if __name__ == "__main__":
    import traceback
    sys.argv += ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(DARK_STYLE)
        window = ServerBrowser()
        window.show()
        sys.exit(app.exec())
    except Exception:
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise
