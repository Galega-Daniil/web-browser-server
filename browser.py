import sys
import os
import traceback
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QPushButton, QLineEdit, QComboBox,
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QProgressBar, QCheckBox, QLabel
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SEARCH_ENGINES = {
    "Яндекс": "https://yandex.ru",
    "Google": "https://google.com",
    "DuckDuckGo": "https://duckduckgo.com",
}
START_PAGE = "http://localhost"

DARK_STYLE = """
QMainWindow, QDialog { background-color: #1e1e2e; color: #cdd6f4; }
QCheckBox, QLabel { color: #cdd6f4; }
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


class ServerWebPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ignore_ssl = True

    def certificateError(self, error):
        if self.ignore_ssl:
            error.acceptCertificate()
            return True
        return super().certificateError(error)


class SettingsDialog(QDialog):
    def __init__(self, current_engine, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.resize(420, 290)

        layout = QVBoxLayout(self)

        engine_label = QLabel("Поисковая система по умолчанию:")
        layout.addWidget(engine_label)

        self.engine_combo = QComboBox()
        self.engine_combo.addItems(SEARCH_ENGINES.keys())
        self.engine_combo.setCurrentText(current_engine)
        layout.addWidget(self.engine_combo)

        self.js_check = QCheckBox("Включить JavaScript")
        self.img_check = QCheckBox("Загружать изображения")
        self.ssl_check = QCheckBox("Игнорировать ошибки SSL (для самоподписанных сертификатов)")

        layout.addWidget(self.js_check)
        layout.addWidget(self.img_check)
        layout.addWidget(self.ssl_check)

        close_btn = QPushButton("Готово")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        layout.addStretch()

        footer_label = QLabel("2026 Сделано на основе: хрониум автор: Google.Inc")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("color: #a6adc8; font-size: 11px;")
        layout.addWidget(footer_label)


class BrowserTab(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.browser = QWebEngineView()
        self.page = ServerWebPage(self.browser)
        self.page.ignore_ssl = self.window.ignore_ssl
        self.browser.setPage(self.page)

        s = self.browser.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, self.window.js_enabled)
        s.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, self.window.img_enabled)
        s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)

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
        icon_path = os.path.join(BASE_DIR, "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.js_enabled = True
        self.img_enabled = True
        self.ignore_ssl = True

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
        self.url_bar.setPlaceholderText("Введите адрес или поисковый запрос и нажмите Enter")
        self.url_bar.returnPressed.connect(self.navigate)
        self.search_bar = QComboBox()
        self.search_bar.addItems(SEARCH_ENGINES.keys())
        self.settings_btn = QPushButton("⚙")

        toolbar.addWidget(self.back_btn)
        toolbar.addWidget(self.fwd_btn)
        toolbar.addWidget(self.reload_btn)
        toolbar.addWidget(self.home_btn)
        toolbar.addWidget(self.search_bar)

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

        QShortcut(QKeySequence("Ctrl+T"), self, activated=self.add_tab)
        QShortcut(QKeySequence("Ctrl+W"), self, activated=self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+L"), self, activated=self.focus_url_bar)
        QShortcut(QKeySequence("Alt+Left"), self, activated=lambda: self.current().back())
        QShortcut(QKeySequence("Alt+Right"), self, activated=lambda: self.current().forward())
        QShortcut(QKeySequence("F5"), self, activated=lambda: self.current().reload())

        self.add_tab(START_PAGE)

    def current(self):
        return self.tabs.currentWidget().browser

    def add_tab(self, url=START_PAGE):
        tab = BrowserTab(self)
        self.tabs.addTab(tab, "Новая вкладка")
        self.tabs.setCurrentWidget(tab)
        tab.browser.load(QUrl(url))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def close_current_tab(self):
        self.close_tab(self.tabs.currentIndex())

    def focus_url_bar(self):
        self.url_bar.setFocus()
        self.url_bar.selectAll()

    def navigate(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        if not text.startswith(("http://", "https://")):
            if text.startswith(("localhost", "127.0.0.1", "0.0.0.0")):
                text = "http://" + text
            elif " " in text or "." not in text:
                engine = SEARCH_ENGINES[self.search_bar.currentText()]
                text = engine + text
            else:
                text = "https://" + text
        self.current().load(QUrl(text))

    def go_home(self):
        self.current().load(QUrl(START_PAGE))

    def open_settings(self):
        dlg = SettingsDialog(self.search_bar.currentText(), self)
        dlg.js_check.setChecked(self.js_enabled)
        dlg.img_check.setChecked(self.img_enabled)
        dlg.ssl_check.setChecked(self.ignore_ssl)

        if dlg.exec():
            self.search_bar.setCurrentText(dlg.engine_combo.currentText())
            self.js_enabled = dlg.js_check.isChecked()
            self.img_enabled = dlg.img_check.isChecked()
            self.ignore_ssl = dlg.ssl_check.isChecked()

            for i in range(self.tabs.count()):
                tab = self.tabs.widget(i)
                tab.page.ignore_ssl = self.ignore_ssl
                st = tab.browser.settings()
                st.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, self.js_enabled)
                st.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, self.img_enabled)


if __name__ == "__main__":
    sys.argv += [
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--ignore-certificate-errors"
    ]
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(DARK_STYLE)
        window = ServerBrowser()
        window.show()
        sys.exit(app.exec())
    except Exception:
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
