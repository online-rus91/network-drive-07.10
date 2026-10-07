import flet as ft
import subprocess
import os


# ---------- КЛАСС СЕТЕВОГО ДИСКА ----------
class NetworkDrive:
    def __init__(self, short_name, description, path, letter=None):
        self.short_name = short_name
        self.description = description
        self.path = path
        self.letter = letter


# ---------- ОБЪЕКТЫ СЕТЕВЫХ ДИСКОВ ----------
MAIN = [
    NetworkDrive(
        "SCAN",
        "Основной диск scan",
        r"\\127.0.0.1\Testshare\scan",
        "Z:"
    ),
    NetworkDrive(
        "EXCHANGE",
        "Основной диск exchange",
        r"\\127.0.0.1\Testshare\exchange",
        "Y:"
    ),
]

EXTRA = [
    NetworkDrive(
        "OID",
        "отд. исполнительной документации",
        r"\\127.0.0.1\Testshare\OID"
    ),
    NetworkDrive(
        "PTO",
        "производственно технический отдел",
        r"\\127.0.0.1\Testshare\PTO"
    ),
    NetworkDrive(
        "IT",
        "информационные технологии",
        r"\\127.0.0.1\Testshare\IT"
    ),
    NetworkDrive(
        "OGE",
        "отд. главного энергетика",
        r"\\127.0.0.1\Testshare\OGE"
    ),
    NetworkDrive(
        "OPB",
        "отд. производственной безопасности",
        r"\\127.0.0.1\Testshare\OPB"
    ),
]

BACKUP = ["V", "U", "T", "S", "R"]


# ---------- КЛАСС ПРИЛОЖЕНИЯ ----------
class NetworkDriveApp:
    def __init__(self, page: ft.Page):
        self.page = page

        self.page.title = "Сетевые диски"
        self.page.window.width = 650
        self.page.window.height = 600

        self.checkboxes = []

        self.log_text = ft.TextField(
            label="Журнал",
            multiline=True,
            read_only=True,
            height=150,
        )

        self.build_ui()

    def build_ui(self):
        # Создание Checkbox для дополнительных дисков
        for drive in EXTRA:
            cb = ft.Checkbox(
                label=f"{drive.short_name} - {drive.description}",
                data=drive,
            )

            self.checkboxes.append(cb)

        # Column - вертикальное расположение элементов
        main_column = ft.Column(
            controls=[
                ft.Text(
                    f"{drive.letter} -> {drive.path}"
                )
                for drive in MAIN
            ]
        )

        # Container - оболочка для списка Checkbox
        extra_container = ft.Container(
            content=ft.Column(
                controls=self.checkboxes,
                scroll=ft.ScrollMode.AUTO,
            ),
            height=190,
            padding=10,
            border=ft.Border.all(1),
        )

        # Row - горизонтальное расположение кнопок
        buttons = ft.Row(
            controls=[
                ft.Button(
                    "Подключить основные",
                    on_click=self.connect_main,
                ),

                ft.Button(
                    "Подключить выбранные",
                    on_click=self.connect_selected,
                ),

                ft.Button(
                    "Отключить выбранные",
                    on_click=self.disconnect_selected,
                ),
            ]
        )

        # Добавление элементов на страницу
        self.page.add(
            ft.Text(
                "Сетевые диски",
                size=28,
            ),

            ft.Divider(),

            ft.Text(
                "Основные:",
                weight=ft.FontWeight.BOLD,
            ),

            main_column,

            ft.Divider(),

            ft.Text(
                "Дополнительные:",
                weight=ft.FontWeight.BOLD,
            ),

            extra_container,

            buttons,

            ft.Divider(),

            self.log_text,
        )

    def log(self, message):
        """
        Добавляет сообщение в журнал.
        """

        self.log_text.value += message + "\n"

        self.page.update()

    def free_drive(self):
        """
        Ищет свободную букву диска.
        """

        for letter in BACKUP:

            if not os.path.exists(
                f"{letter}:\\"
            ):
                return f"{letter}:"

        return None

    def connect_drive(self, drive: NetworkDrive):
        """
        Подключает сетевой диск.
        """

        letter = drive.letter

        # Если буква не задана,
        # ищем свободную
        if letter is None:

            letter = self.free_drive()

        if letter is None:

            self.log(
                "Нет свободных букв"
            )

            return

        try:
            # Формируется системная команда:
            #
            # net use V: \\server\share

            result = subprocess.run(
                [
                    "net",
                    "use",
                    letter,
                    drive.path,
                ],

                capture_output=True,
                text=True,
            )

            # Код 0 означает успешное выполнение
            if result.returncode == 0:

                self.log(
                    f"{letter} подключён: "
                    f"{drive.short_name}"
                )

            else:

                self.log(
                    f"Ошибка подключения: "
                    f"{drive.short_name}"
                )

        except Exception as error:

            self.log(
                f"Ошибка: {error}"
            )

    def connect_main(self, e):
        """
        Подключает основные диски.
        """

        for drive in MAIN:

            self.connect_drive(
                drive
            )

    def connect_selected(self, e):
        """
        Подключает выбранные
        дополнительные диски.
        """

        for cb in self.checkboxes:

            if cb.value:

                # В cb.data хранится
                # объект NetworkDrive
                drive = cb.data

                self.connect_drive(
                    drive
                )

    def disconnect_selected(self, e):
        """
        Отключает выбранные
        сетевые диски.
        """

        for cb in self.checkboxes:

            if cb.value:

                drive = cb.data

                subprocess.run(
                    [
                        "net",
                        "use",
                        drive.path,
                        "/delete",
                        "/y",
                    ],

                    capture_output=True,
                )

                self.log(
                    f"{drive.short_name} отключён"
                )


# ---------- ТОЧКА ВХОДА ----------
def main(page: ft.Page):
    NetworkDriveApp(page)


if __name__ == "__main__":
    ft.run(main)