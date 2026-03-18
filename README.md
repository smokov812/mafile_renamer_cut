# mafile renamer + cut

Простая Windows-программа на Python для обработки `.mafile`:
- берет из каждого файла `shared_secret`, `Session.SteamID` и `account_name`
- удаляет лишние поля
- сохраняет новый `.mafile` в папку `ready`
- переименовывает файл по `account_name`

Текущая версия: `1.0.0`

## Что делает программа

Программа ищет в выбранной папке все файлы с расширением `.mafile`.

Для каждого файла она:
- берет `shared_secret`
- берет `Session.SteamID`
- берет `account_name`
- создает новый файл, где остаются только нужные поля
- сохраняет результат как `<account_name>.mafile`

Если в файле нет обязательных полей, программа пропускает его и пишет ошибку в лог.

## Интерфейс

1. Нажмите `Выбрать папку`
2. Укажите папку с `.mafile`
3. Нажмите `Обработать`
4. Готовые файлы появятся в подпапке `ready`

## Структура результата

Исходный файл:

```json
{
  "shared_secret": "xxx",
  "Session": {
    "SteamID": "123456789"
  },
  "account_name": "my_login",
  "other_data": "..."
}
```

Результат:

```json
{
  "shared_secret": "xxx",
  "Session": {
    "SteamID": "123456789"
  }
}
```

Имя файла:

```text
my_login.mafile
```

## Запуск из исходников

Требования:
- Python 3.10+ (подойдет и более новая версия)
- Windows

Запуск:

```powershell
python .\mafile_renamer___cut.py
```

Либо же просто скачай и запусти mafile_ranamer_cut.exe





