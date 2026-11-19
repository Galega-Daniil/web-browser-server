import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QPushButton, QLineEdit, QComboBox,
    QLabel, QDialog, QVBoxLayout, QTabWidget, QWidget, QVBoxLayout as VLayout,
    QProgressBar
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings


# ---------- Настройки ----------

class SettingsDialog(QDialog):
    def __init__(self, current_engine, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки браузера")
        self.setFixedSize(360, 220)
        self.parent_browser = parent

        layout = QVBoxLayout()

        label = QLabel("Поисковая система по умолчанию:")
        layout.addWidget(label)

        self.engine_combo = QComboBox()
        self.engine_combo.addItems(list(parent.search_engines.keys()) if parent else [])
        self.engine_combo.setCurrentText(current_engine)
        self.engine_combo.currentTextChanged.connect(self.change_engine)
        layout.addWidget(self.engine_combo)

        layout.addStretch()

        footer_label = QLabel("2026 Сделано на основе: хрониум автор: Google.Inc")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(footer_label)

        self.setLayout(layout)

    def change_engine(self, text):
        if self.parent_browser:
            self.parent_browser.search_engine = text


# ---------- Вкладка браузера ----------

class BrowserTab(QWidget):
    """Виджет одной вкладки: страница + индикатор загрузки."""

    def __init__(self, parent_browser, start_url="http://localhost"):
        super().__init__()
        self.parent_browser = parent_browser
        layout = VLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.view = QWebEngineView()

        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)

        self.progress = QProgressBar()
        self.progress.setMaximumHeight(4)
        self.progress.setTextVisible(False)
        self.progress.hide()

        layout.addWidget(self.progress)
        layout.addWidget(self.view)

        self.view.loadProgress.connect(self.on_progress)
        self.view.loadFinished.connect(lambda ok: self.progress.hide())
        self.view.urlChanged.connect(self.parent_browser.update_url_bar)
        self.view.titleChanged.connect(self.parent_browser.update_tab_title)
        self.view.loadFinished.connect(self.parent_browser.update_tab_icon)

        self.view.setUrl(QUrl(start_url))

    def on_progress(self, value):
        self.progress.show()
        self.progress.setValue(value)


# ---------- Главное окно ----------

DARK_QSS = """
QMainWindow, QDialog { background-color: #1e1f24; }
QToolBar { background: #26272e; border: none; spacing: 4px; padding: 4px; }
QPushButton {
    background: #33343d; color: #e6e6e6; border: none; border-radius: 6px;
    padding: 6px 12px; font-size: 13px;
}
QPushButton:hover { background: #43454f; }
QPushButton:pressed { background: #4d4f5c; }
QLineEdit, QComboBox {
    background: #33343d; color: #e6e6e6; border: 1px solid #43454f;
    border-radius: 6px; padding: 6px 10px; font-size: 13px;
}
QLineEdit:focus { border: 1px solid #5b84ee; }
QTabWidget::pane { border: none; }
QTabBar::tab {
    background: #26272e; color: #b9bac2; padding: 8px 14px;
    border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px;
}
QTabBar::tab:selected { background: #1e1f24; color: #ffffff; }
QTabBar::tab:hover { color: #ffffff; }
QProgressBar { background: transparent; border: none; }
QProgressBar::chunk { background: #5b84ee; border-radius: 2px; }
QLabel { color: #e6e6e6; }
"""


class ServerBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Chromium Browser")
        self.resize(1200, 800)
        self.setStyleSheet(DARK_QSS)

        self.search_engines = {
            "Яндекс": "https://yandex.ru/search/?text=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Google": "https://www.google.com/search?q=",
        }
        self.search_engine = "Яндекс"

        # --- Вкладки ---
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tabs)

        self.add_tab()

        # --- Панель навигации ---
        navbar = QToolBar("Навигация")
        navbar.setMovable(False)
        self.addToolBar(navbar)

        for icon, slot, hint in [
            ("←", self.navigate_back, "Назад (Alt+Left)"),
            ("→", self.navigate_forward, "Вперёд (Alt+Right)"),
            ("↻", self.navigate_reload, "Обновить (F5)"),
            ("⌂", self.navigate_home, "На главную"),
        ]:
            btn = QPushButton(icon)
            btn.setFixedWidth(36)
            btn.setToolTip(hint)
            btn.clicked.connect(slot)
            navbar.addWidget(btn)

        navbar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите URL или поисковый запрос…")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setClearButtonEnabled(True)
        navbar.addWidget(self.url_bar, 1)  # растягивается на всё свободное место

        self.quick_engine_box = QComboBox()
        self.quick_engine_box.addItems(list(self.search_engines.keys()))
        self.quick_engine_box.currentTextChanged.connect(self.sync_engine_from_bar)
        navbar.addWidget(self.quick_engine_box)

        settings_btn = QPushButton("⚙")
        settings_btn.setFixedWidth(36)
        settings_btn.setToolTip("Настройки")
        settings_btn.clicked.connect(self.open_settings)
        navbar.addWidget(settings_btn)

        new_tab_btn = QPushButton("+")
        new_tab_btn.setFixedWidth(30)
        new_tab_btn.setToolTip("Новая вкладка (Ctrl+T)")
        new_tab_btn.clicked.connect(lambda: self.add_tab())
        navbar.addWidget(new_tab_btn)

        # --- Горячие клавиши ---
        shortcuts = [
            (QKeySequence("Ctrl+T"), lambda: self.add_tab()),
            (QKeySequence("Ctrl+W"), self.close_current_tab),
            (QKeySequence("Ctrl+L"), self.focus_url_bar),
            (QKeySequence("Alt+Left"), self.navigate_back),
            (QKeySequence("Alt+Right"), self.navigate_forward),
            (QKeySequence("F5"), self.navigate_reload),
        ]
        for seq, slot in shortcuts:
            action = QAction(self)
            action.setShortcut(seq)
            action.triggered.connect(slot)
            self.addAction(action)

    # --- Работа с вкладками ---

    def current_tab(self):
        return self.tabs.currentWidget()

    def add_tab(self, url="http://localhost"):
        tab = BrowserTab(self, url)
        idx = self.tabs.addTab(tab, "Новая вкладка")
        self.tabs.setCurrentIndex(idx)
        self.focus_url_bar()
        return tab

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            widget.view.stop()
            self.tabs.removeTab(index)
        else:
            self.close()

    def close_current_tab(self):
        self.close_tab(self.tabs.currentIndex())

    def on_tab_changed(self, index):
        tab = self.current_tab()
        if tab:
            self.update_url_bar(tab.view.url())

    def update_tab_title(self, title):
        tab = self.sender().parent() or self.current_tab()
        # Надёжнее: находим вкладку по сигналу
        view = self.sender()
        for i in range(self.tabs.count()):
            if self.tabs.widget(i).view is view:
                self.tabs.setTabText(i, title[:24] or "Новая вкладка")
                break

    def update_tab_icon(self, ok):
        view = self.sender()
        for i in range(self.tabs.count()):
            if self.tabs.widget(i).view is view:
                self.tabs.setTabIcon(i, view.icon())
                break

    # --- Навигация ---

    def navigate_home(self):
        tab = self.current_tab()
        if tab:
            tab.view.setUrl(QUrl("http://localhost"))

    def navigate_back(self):
        tab = self.current_tab()
        if tab and tab.view.history().canGoBack():
            tab.view.back()

    def navigate_forward(self):
        tab = self.current_tab()
        if tab and tab.view.history().canGoForward():
            tab.view.forward()

    def navigate_reload(self):
        tab = self.current_tab()
        if tab:
            tab.view.reload()

    def navigate_to_url(self):
        tab = self.current_tab()
        if not tab:
            return

        text = self.url_bar.text().strip()
        if not text:
            return

        url = QUrl.fromUserInput(text)
        # QUrl.fromUserInput распознаёт и домены, и IP, и localhost;
        # если это явно не ссылка — уходим в поиск
        if url.host() and "." in url.host() or url.host() == "localhost":
            pass
        else:
            url = QUrl(self.search_engines[self.search_engine] + QUrl.toPercentEncoding(text).data().decode())

        tab.view.setUrl(url)
        tab.view.setFocus()

    def update_url_bar(self, url):
        tab = self.current_tab()
        if tab and url.toString() != self.url_bar.text():
            self.url_bar.setText(url.toString())

    def focus_url_bar(self):
        tab = self.current_tab()
        if tab:
            self.url_bar.setText(tab.view.url().toString())
        self.url_bar.setFocus()
        self.url_bar.selectAll()

    def sync_engine_from_bar(self, text):
        self.search_engine = text

    def open_settings(self):
        dialog = SettingsDialog(self.search_engine, self)
        dialog.exec()
        # Синхронизируем выпадающий список на панели после закрытия настроек
        self.quick_engine_box.blockSignals(True)
        self.quick_engine_box.setCurrentText(self.search_engine)
        self.quick_engine_box.blockSignals(False)


if __name__ == "__main__":
    # Флаги Chromium для стабильной работы на серверах (в т.ч. без GPU и в Docker/root)
    sys.argv += ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]

    app = QApplication(sys.argv)
    window = ServerBrowser()
    window.show()
    sys.exit(app.exec())
