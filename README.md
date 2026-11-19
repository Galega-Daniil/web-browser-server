# web-browser-server

Локальный браузер на базе Chromium (`PyQt6` + `QWebEngineView`). Предназначен для запуска на сервере: без лишнего интерфейса, с отключённым автовоспроизведением и плагинами.

---

## Быстрый старт

```bash
git clone https://github.com/Galega-server/web-browser-server.git
cd web-browser-server
pip install PyQt6 PyQt6-WebEngine
python server_browser.py
```

Стартовая страница — `http://localhost`.

> Запускайте из терминала. При запуске двойным кликом окно может мгновенно исчезнуть — вы не увидите ошибку.

---

## Готовые сборки

| Система | Файл |
|---|---|
| Windows | `[server-chromium-browser-setup.exe](#)` |
| Linux (Debian / Ubuntu) | `[server-chromium-browser_1.0.0_amd64.deb](#)` |
| Linux (RHEL / Fedora / CentOS) | `[server-chromium-browser-1.0.0-1.x86_64.rpm](#)` |

Для Linux также подойдёт один автономный файл (AppImage / `pyinstaller --onefile --windowed`).

---

## Установка из исходников

```bash
git clone https://github.com/Galega-server/web-browser-server.git
cd web-browser-server
pip install PyQt6 PyQt6-WebEngine
python server_browser.py
```

**Важно:** для `QWebEngineView` нужны оба пакета (`PyQt6` и `PyQt6-WebEngine`). Одного `PyQt6` недостаточно. На Linux предпочтительнее `python3`, а не `python`.

---

### Системные требования

| Параметр | Минимум | Рекомендация |
|---|---|---|
| Python | 3.9 | 3.11+ |
| ОЗУ | 1 ГБ | 4 ГБ |
| Сеть | есть | есть |

Приложение работает без GPU (`--disable-gpu`) и в изолированных средах (`--no-sandbox`, `--disable-dev-shm-usage`).

---

### Возможности

- Вкладки (`Ctrl+T`, `Ctrl+W`), закрытие вкладок.
- Адресная строка: URL и поисковые запросы.
- Выбор поисковой системы («Яндекс», «DuckDuckGo», «Google»).
- Тёмная тема (QSS).
- Стартовая страница `http://localhost`.
- Отключённое автовоспроизведение и плагины.

---

### Горячие клавиши

| Действие | Клавиша |
|---|---|
| Новая вкладка | `Ctrl+T` |
| Закрыть вкладку | `Ctrl+W` |
| Фокус в адресную строку | `Ctrl+L` |
| Назад | `Alt+Left` |
| Вперёд | `Alt+Right` |
| Обновить | `F5` |

---

### Поддержка

Если браузер не работает: **daniilgalega@mail.ru**

---

Перед публикацией замените `#` в ссылках на реальные из Release, формат:

```text
https://github.com/Galega-server/web-browser-server/releases/download/v1.0.0/имя-файла
```
