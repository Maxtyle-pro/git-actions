# Server Time API

Простой тестовый бэкенд на FastAPI, который возвращает текущее время сервера.

## Запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

## Запуск в Docker

```powershell
docker build -t server-time-api .
docker run --rm -p 8000:8000 server-time-api
```

После запуска API будет доступно по адресу:

- `GET http://127.0.0.1:8000/` - проверка, что сервис работает
- `GET http://127.0.0.1:8000/health` - проверка состояния приложения
- `GET http://127.0.0.1:8000/time` - текущее время сервера
- `GET http://127.0.0.1:8000/date` - текущая дата сервера
