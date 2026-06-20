from datetime import datetime

from fastapi import FastAPI


app = FastAPI(title="Server Time API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Server Time API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "Server Time API",
    }


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


@app.get("/test")
def test_endpoint() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Test endpoint is working",
    }


@app.get("/time")
def get_server_time() -> dict[str, str]:
    now = datetime.now().astimezone()

    return {
        "server_time": now.isoformat(),
        "timezone": now.tzname() or "",
    }


@app.get("/date")
def get_server_date() -> dict[str, str]:
    now = datetime.now().astimezone()

    return {
        "server_date": now.date().isoformat(),
        "timezone": now.tzname() or "",
    }
