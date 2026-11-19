# web-browser-server

Локальный браузер на базе Chromium (PyQt6 + QWebEngineView). Предназначен для запуска на сервере: без лишнего интерфейса, с отключённым автовоспроизведением и плагинами.

## Быстрый старт

```bash
git clone https://github.com/Galega-server/web-browser-server.git
cd web-browser-server
pip install PyQt6 PyQt6-WebEngine
python server_browser.py
Стартовая страница — http://localhost.

Запускайте из терминала. При запуске двойным кликом окно может мгновенно исчезнуть — вы не увидите ошибку.

Готовые сборки
Перед публикацией создайте  и вставьте ссылки ниже.

Система	Файл	Статус
Windows	[server-chromium-browser-setup.exe](#)	⬜ TODO
Linux (Debian / Ubuntu)	[server-chromium-browser_1.0.0_amd64.deb](#)	⬜ TODO
Linux (RHEL / Fedora / CentOS)	[server-chromium-browser-1.0.0-1.x86_64.rpm](#)	⬜ TODO
Альтернатива для Linux: один автономный файл (AppImage / pyinstaller --onefile --windowed) — не требует установки пакетов.

Номера версий в именах файлов нужно приводить к формату релиза (например, v1.0.0).

Установка из исходников
bash
git clone https://github.com/Galega-server/web-browser-server.git
cd web-browser-server
pip install PyQt6 PyQt6-WebEngine
python server_browser.py
Важно: для QWebEngineView нужны оба пакета. Одного pip install PyQt6 недостаточно.

Для Linux: python3, а не только python.

Системные требования
Параметр	Минимум	Рекомендация
Python	3.9	3.11+
ОЗУ	1 ГБ	4 ГБ
Сеть	есть	есть
Приложение работает без GPU (--disable-gpu) и в изолированных средах (--no-sandbox, --disable-dev-shm-usage).

Возможности
Вкладки (Ctrl+T, Ctrl+W), закрытие вкладок.
Адресная строка: URL и поисковые запросы.
Выбор поисковой системы («Яндекс», «DuckDuckGo», «Google»).
Тёмная тема (QSS).
Стартовая страница http://localhost.
Отключённое автовоспроизведение и плагины.
Горячие клавиши
Действие	Клавиша
Новая вкладка	Ctrl+T
Закрыть вкладку	Ctrl+W
Фокус в адресную строку	Ctrl+L
Назад	Alt+Left
Вперёд	Alt+Right
Обновить	F5
Поддержка
Если браузер не работает: 

(Для публичного проекта имеет смысл заменить личную почту на Discussion / Issues.)

Как опубликовать сборки
Перейдите в Releases → Create a new release.
Тег: v1.0.0, название: Release v1.0.0.
Choose files — прикрепите .exe, .deb, .rpm.
Опубликовать.
Ссылка на файл будет выглядеть так:

text
https://github.com/Galega-server/web-browser-server/releases/download/v1.0.0/server-chromium-browser-setup.exe
Структура репозитория
server_browser.py — главный скрипт.
.github/workflows/ — шаблоны для сборки (требуют заполнения).
README.md — эта страница.
Это черновик: перед публикацией замените все TODO и номера версий.
