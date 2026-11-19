import os
import sys
import subprocess
import platform


def get_desktop_dir():
    """Рабочий стол для Windows и Linux."""
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        # Учитываем перенесённый рабочий стол через реестр
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
            ) as key:
                return winreg.QueryValueEx(key, "Desktop")[0]
        except Exception:
            pass
    return os.path.join(home, "Desktop" if platform.system() == "Windows" else "Рабочий стол")


def create_windows_shortcut(target):
    """Создаёт .lnk через PowerShell (без сторонних библиотек)."""
    desktop = get_desktop_dir()
    lnk_path = os.path.join(desktop, "Server Chromium Browser.lnk")

    workdir = os.path.dirname(target)
    ps_script = (
        "$ws = New-Object -ComObject WScript.Shell; "
        f"$sc = $ws.CreateShortcut('{lnk_path}'); "
        f"$sc.TargetPath = '{target}'; "
        f"$sc.WorkingDirectory = '{workdir}'; "
        "$sc.Description = 'Server Chromium Browser'; "
        "$sc.Save()"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_script],
        check=True, capture_output=True
    )
    return lnk_path


def create_linux_shortcut(target):
    """Создаёт .desktop файл на рабочем столе и в меню приложений."""
    home = os.path.expanduser("~")
    desktop_dir = get_desktop_dir()
    content = (
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Server Chromium Browser\n"
        f"Exec=python3 \"{target}\"\n"
        f"Path={os.path.dirname(target)}\n"
        "Icon=web-browser\n"
        "Categories=Network;WebBrowser;\n"
        "Terminal=false\n"
    )

    paths = [
        os.path.join(desktop_dir, "server-chromium-browser.desktop"),
        os.path.join(home, ".local", "share", "applications", "server-chromium-browser.desktop"),
    ]
    for path in paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        # Право на запуск, чтобы рабочий стол считал файл ярлыком
        os.chmod(path, 0o755)
    return paths[0]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(script_dir, "browser.py")

    if not os.path.isfile(target):
        print(f"Не найден файл браузера: {target}")
        print("Положите install_shortcut.py в одну папку с browser.py и запустите снова.")
        return

    system = platform.system()
    if system == "Windows":
        path = create_windows_shortcut(target)
        print(f"Ярлык создан: {path}")
    elif system == "Linux":
        path = create_linux_shortcut(target)
        print(f"Ярлык создан: {path}")
        print("На GNOME может понадобиться разрешить запуск:")
        print(f"  gio set \"{path}\" metadata::trusted true")
    else:
        print(f"Система {system} не поддерживается.")


if __name__ == "__main__":
    main()
    if __name__ == "__main__":
    import traceback
    sys.argv += ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
    try:
        app = QApplication(sys.argv)
        window = ServerBrowser()
        window.show()
        sys.exit(app.exec())
    except Exception:
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise
