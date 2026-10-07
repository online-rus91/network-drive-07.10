import flet as ft
import subprocess
import os


# Базовый класс
class Disk:
    def __init__(self, name, path, letter=None):
        self.name = name
        self.path = path
        self.letter = letter


# Дочерний класс
class NetworkDrive(Disk):
    def __init__(self, name, description, path, letter=None):
        super().__init__(name, path, letter)
        self.description = description


# Не менее 5 объектов
MAIN = [
    NetworkDrive("SCAN", "Сканирование", r"\\127.0.0.1\Testshare\scan", "Z:"),
    NetworkDrive("EXCHANGE", "Обмен", r"\\127.0.0.1\Testshare\exchange", "Y:"),
]

EXTRA = [
    NetworkDrive("OID", "Исполнительная документация", r"\\127.0.0.1\Testshare\OID"),
    NetworkDrive("PTO", "Производственно-технический отдел", r"\\127.0.0.1\Testshare\PTO"),
    NetworkDrive("IT", "Информационные технологии", r"\\127.0.0.1\Testshare\IT"),
]

BACKUP = ["V", "U", "T", "S", "R"]


def free_drive():
    for letter in BACKUP:
        if not os.path.exists(f"{letter}:\\"):
            return f"{letter}:"
    return None


def connect_drive(drive, log):
    letter = drive.letter or free_drive()

    if not letter:
        log("Нет свободных букв")
        return

    result = subprocess.run(
        ["net", "use", letter, drive.path],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        log(f"{drive.name}: подключён как {letter}")
    else:
        log(f"{drive.name}: ошибка подключения")


def main(page: ft.Page):
    page.title = "Сетевые диски"

    log_text = ft.TextField(
        label="Журнал",
        multiline=True,
        read_only=True,
        height=140,
    )

    checkboxes = []

    for drive in EXTRA:
        cb = ft.Checkbox(label=f"{drive.name} - {drive.description}")
        cb.data = drive
        checkboxes.append(cb)

    def log(message):
        log_text.value += message + "\n"
        page.update()

    def connect_main(e):
        for drive in MAIN:
            connect_drive(drive, log)

    def connect_selected(e):
        for cb in checkboxes:
            if cb.value:
                connect_drive(cb.data, log)

    def disconnect_selected(e):
        for cb in checkboxes:
            if cb.value:
                subprocess.run(
                    ["net", "use", cb.data.path, "/delete", "/y"],
                    capture_output=True,
                )
                log(f"{cb.data.name}: отключён")

    # Column — вертикальное расположение
    main_column = ft.Column(
        [ft.Text(f"{drive.letter} -> {drive.path}") for drive in MAIN]
    )

    # Container — контейнер со списком Checkbox
    extra_container = ft.Container(
        content=ft.Column(checkboxes),
        padding=10,
        border=ft.border.all(1),
    )

    # Row — горизонтальное расположение кнопок
    buttons = ft.Row([
        ft.Button("Подключить основные", on_click=connect_main),
        ft.Button("Подключить выбранные", on_click=connect_selected),
        ft.Button("Отключить выбранные", on_click=disconnect_selected),
    ])

    page.add(
        ft.Text("Сетевые диски", size=28),
        ft.Text("Основные:", weight="bold"),
        main_column,
        ft.Text("Дополнительные:", weight="bold"),
        extra_container,
        buttons,
        log_text,
    )


ft.run(main)
