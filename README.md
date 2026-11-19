# Server Chromium Browser

Лёгкий браузер на базе **Chromium** (`PyQt6` + `QWebEngineView`) для серверов (VPS/VDS, Docker, Linux без GPU), автоматически открывающий `http://localhost`.

---

## Возможности

* **Стартовая страница:** `http://localhost` с кнопкой быстрого возврата (`⌂`).
* **Поисковые системы:** переключатель на панели инструментов (Яндекс, Google, DuckDuckGo).
* **Умная адресная строка:** поддержка локальных адресов (`localhost:8080`, `127.0.0.1`), доменов и поисковых запросов.
* **Вкладки и темы:** работа с несколькими сервисами одновременно и тёмная тема (QSS).
* **Серверная оптимизация:** флаги `--no-sandbox`, `--disable-gpu`, `--disable-dev-shm-usage`, отключение лишних плагинов и управление JavaScript/изображениями.

---

## Скачивание готовых сборок (`.exe`, `.deb`, `.rpm`, `.zip`)

Сборки для Windows и Linux создаются автоматически через **GitHub Actions**:

1. Откройте вкладку **[Actions](https://github.com)** в репозитории.
2. Выберите последний успешный запуск.
3. Скачайте нужный архив из раздела **Artifacts**:
   * **`Windows-EXE-and-ZIP`** (`ServerBrowser.exe`, `ServerBrowser-Windows.zip`).
   * **`Linux-DEB-RPM-ZIP`** (`.deb`, `.rpm` и портативный `server-browser-linux.zip`).

### Установка

* **Windows:** Распакуйте архив и запустите `ServerBrowser.exe`.
* **Debian / Ubuntu (`.deb`):**
  ```bash
  sudo apt update && sudo apt install -y ./server-browser_1.0.0_amd64.deb libxcb-cursor0 libnss3
  server-browser
  ```
* **Fedora / RHEL (`.rpm`):**
  ```bash
  sudo dnf install -y ./server-browser-1.0.0-1.x86_64.rpm
  server-browser
  ```

> *Примечание для headless-серверов:* используйте `xvfb-run server-browser` или SSH-проброс (`ssh -X user@server`).

---

## Запуск из исходного кода

```bash
git clone https://github.com
cd web-browser-server
pip install PyQt6 PyQt6-WebEngine
python browser.py
```
*(Для Linux используйте `python3` и `pip3`).*

---

## Горячие клавиши и системные требования

| Действие | Клавиши |
| :--- | :--- |
| Новая вкладка / Закрыть | `Ctrl + T` / `Ctrl + W` |
| Адресная строка / Обновить | `Ctrl + L` / `F5` |
| Назад / Вперёд | `Alt + Left` / `Alt + Right` |

* **ОС:** Windows 10/11, Ubuntu 20.04+, Debian 11+, Fedora 36+
* **Python:** 3.9+ (рекомендуется 3.11+)
* **ОЗУ / GPU:** от 1 ГБ ОЗУ (рекомендуется 2–4 ГБ); видеокарта не требуется.

---

## Поддержка

При ошибках проверяйте `error.log` или обращайтесь на почту: **daniilgalega@mail.ru**

---
*2026 Основано на Chromium (Google Inc.)*
