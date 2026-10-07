# Короткое описание для ответа

Проект создан через `flet create`, поэтому основной файл находится в `src/main.py`.

`Disk` — базовый класс. Он хранит общие данные диска:
`name`, `path`, `letter`.

`NetworkDrive` — дочерний класс:

```python
class NetworkDrive(Disk):
```

Он наследует поля `Disk` и добавляет поле `description`.

`super().__init__(...)` вызывает конструктор базового класса.

В программе создано 5 объектов `NetworkDrive`:
SCAN, EXCHANGE, OID, PTO, IT.

`MAIN` и `EXTRA` — списки объектов.

В интерфейсе Flet:
- `Column` располагает элементы вертикально;
- `Row` располагает элементы горизонтально;
- `Container` является оболочкой для `Column` с `Checkbox`;
- `Checkbox` используется для выбора дополнительного диска.

В `cb.data` хранится объект `NetworkDrive`.

Команда Windows `net use` запускается через модуль Python `subprocess`.
