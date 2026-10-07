# Flet Disks — учебный проект ООП

Проект создаётся стандартной командой Flet:

```powershell
flet create flet_disks_final
cd flet_disks_final
flet run
```

После `flet create` основной код находится в `src/main.py`.

## Требования задания

- базовый класс `Disk`;
- дочерний класс `NetworkDrive`;
- наследование `NetworkDrive(Disk)`;
- не менее 5 объектов;
- графический интерфейс Flet;
- `Column`, `Row`, `Container`, `Checkbox`;
- работа с системной командой Windows `net use`.

В проекте создано 5 объектов `NetworkDrive`:
SCAN, EXCHANGE, OID, PTO, IT.
