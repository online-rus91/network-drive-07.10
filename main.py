import flet as ft
import subprocess
import os


MAIN = [
    ("Z:", r"\\127.0.0.1\Testshare\scan"),
    ("Y:", r"\\127.0.0.1\Testshare\exchange"),
]

EXTRA = [
    ("OID", "отд. исполнительной документации", r"\\127.0.0.1\Testshare\OID"),
    ("PTO", "производственно технический отдел", r"\\127.0.0.1\Testshare\PTO"),
    ("IT", "информационные технологии", r"\\127.0.0.1\Testshare\IT"),
    ("OGE", "отд. главного энергетика", r"\\127.0.0.1\Testshare\OGE"),
    ("OPB", "отд. производственной безопасности", r"\\127.0.0.1\Testshare\OPB"),
]

BACKUP = ["V", "U", "T", "S", "R"]


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
        for short, desc, path in EXTRA:
            cb = ft.Checkbox(label=f"{short} - {desc}", data=path)
            self.checkboxes.append(cb)

        main_column = ft.Column(
            controls=[
                ft.Text(f"{letter} -> {path}")
                for letter, path in MAIN
            ]
        )

        extra_container = ft.Container(
            content=ft.Column(
                controls=self.checkboxes,
                scroll=ft.ScrollMode.AUTO,
            ),
            height=190,
            padding=10,
            border=ft.Border.all(1),
        )

        buttons = ft.Row(
            controls=[
                ft.Button("Подключить основные", on_click=self.connect_main),
                ft.Button("Подключить выбранные", on_click=self.connect_selected),
                ft.Button("Отключить выбранные", on_click=self.disconnect_selected),
            ]
        )

        self.page.add(
            ft.Text("Сетевые диски", size=28),
            ft.Divider(),
            ft.Text("Основные:", weight=ft.FontWeight.BOLD),
            main_column,
            ft.Divider(),
            ft.Text("Дополнительные:", weight=ft.FontWeight.BOLD),
            extra_container,
            buttons,
            ft.Divider(),
            self.log_text,
        )

    def log(self, text):
        self.log_text.value += text + "\n"
        self.page.update()

    def free_drive(self):
        for letter in BACKUP:
            if not os.path.exists(f"{letter}:\\"):
                return f"{letter}:"
        return None

    def connect_drive(self, path, letter=None):
        if letter is None:
            letter = self.free_drive()

        if letter is None:
            self.log("Нет свободных букв")
            return

        try:
            result = subprocess.run(
                ["net", "use", letter, path],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                self.log(f"{letter} подключён")
            else:
                self.log(f"Ошибка подключения: {path}")

        except Exception as error:
            self.log(f"Ошибка: {error}")

    def connect_main(self, e):
        for letter, path in MAIN:
            self.connect_drive(path, letter)

    def connect_selected(self, e):
        for cb in self.checkboxes:
            if cb.value:
                self.connect_drive(cb.data)

    def disconnect_selected(self, e):
        for cb in self.checkboxes:
            if cb.value:
                subprocess.run(
                    ["net", "use", cb.data, "/delete", "/y"],
                    capture_output=True,
                )
                self.log(f"{cb.data} отключён")


def main(page: ft.Page):
    NetworkDriveApp(page)


if __name__ == "__main__":
    ft.run(main)
