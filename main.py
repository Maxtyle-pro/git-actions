from datetime import datetime

from fastapi import FastAPI


app = FastAPI(title="Server Time API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Server Time API is running"}


@app.get("/time")
def get_server_time() -> dict[str, str]:
    now = datetime.now().astimezone()

    return {
        "server_time": now.isoformat(),
        "timezone": now.tzname() or "",
    }
