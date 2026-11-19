import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit, 
    QPushButton, QComboBox, QDialog, QVBoxLayout, QLabel
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings

class SettingsDialog(QDialog):
    def __init__(self, current_engine, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки браузера")
        self.setFixedSize(360, 200)
        self.parent_browser = parent

        layout = QVBoxLayout()

        # Выбор поисковой системы
        label = QLabel("Поисковая система по умолчанию:")
        layout.addWidget(label)

        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Яндекс", "DuckDuckGo", "Google"])
        self.engine_combo.setCurrentText(current_engine)
        self.engine_combo.currentTextChanged.connect(self.change_engine)
        layout.addWidget(self.engine_combo)

        layout.addStretch()

        # Требуемая подпись внизу настроек
        footer_label = QLabel("2026 Сделано на основе: хрониум автор: Google.Inc")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(footer_label)

        self.setLayout(layout)

    def change_engine(self, text):
        if self.parent_browser:
            self.parent_browser.search_engine = text


class ServerBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Chromium Browser")
        self.resize(1200, 800)

        # Поисковые системы
        self.search_engines = {
            "Яндекс": "https://ya.ru",
            "DuckDuckGo": "https://duckduckgo.com",
            "Google": "https://google.com"
        }
        self.search_engine = "Яндекс"

        # Инициализация движка Chromium
        self.browser = QWebEngineView()
        
        # Оптимизация для серверов (отключаем лишнюю графику/автовоспроизведение)
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)

        # Стартовая страница http://localhost
        self.browser.setUrl(QUrl("http://localhost"))
        self.setCentralWidget(self.browser)

        # Панель навигации
        navbar = QToolBar("Навигация")
        navbar.setMovable(False)
        self.addToolBar(navbar)

        # Кнопки управления
        back_btn = QPushButton("←")
        back_btn.clicked.connect(self.browser.back)
        navbar.addWidget(back_btn)

        forward_btn = QPushButton("→")
        forward_btn.clicked.connect(self.browser.forward)
        navbar.addWidget(forward_btn)

        reload_btn = QPushButton("↻")
        reload_btn.clicked.connect(self.browser.reload)
        navbar.addWidget(reload_btn)

        home_btn = QPushButton("Localhost")
        home_btn.clicked.connect(self.navigate_home)
        navbar.addWidget(home_btn)

        # Адресная / поисковая строка
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Введите URL или поисковый запрос...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Быстрый выбор поисковика на панели
        self.quick_engine_box = QComboBox()
        self.quick_engine_box.addItems(list(self.search_engines.keys()))
        self.quick_engine_box.currentTextChanged.connect(self.sync_engine_from_bar)
        navbar.addWidget(self.quick_engine_box)

        # Кнопка настроек
        settings_btn = QPushButton("⚙ Настройки")
        settings_btn.clicked.connect(self.open_settings)
        navbar.addWidget(settings_btn)

        # Обновление адресной строки при переходе
        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://localhost"))

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return

        # Проверка: это URL (или localhost/IP) или поисковый запрос
        if "." in text or text.startswith("http://") or text.startswith("https://") or text.startswith("localhost"):
            if not text.startswith(("http://", "https://")):
                text = "http://" + text
            url = QUrl(text)
        else:
            search_url = self.search_engines[self.search_engine] + text
            url = QUrl(search_url)

        self.browser.setUrl(url)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def sync_engine_from_bar(self, text):
        self.search_engine = text

    def open_settings(self):
        dialog = SettingsDialog(self.search_engine, self)
        dialog.exec()
        # Синхронизируем выпадающий список на панели после закрытия настроек
        self.quick_engine_box.setCurrentText(self.search_engine)


if __name__ == "__main__":
    # Флаги Chromium для стабильной работы на серверах (в т.ч. без GPU и в Docker/root)
    sys.argv.append("--no-sandbox")
    sys.argv.append("--disable-gpu")
    sys.argv.append("--disable-dev-shm-usage")

    app = QApplication(sys.argv)
    window = ServerBrowser()
    window.show()
    sys.exit(app.exec())
