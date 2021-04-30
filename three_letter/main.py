from typing import Optional

import sqlalchemy as sa
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from three_letter.models import Message
from three_letter.config import Settings
from three_letter import db

app = FastAPI()

# Jinja2
templates = Jinja2Templates(directory="templates")

# SQLAlchemy
setting = Settings()
db_engine = sa.create_engine(setting.db_url, echo=True)
db.create_table(db_engine)


# FastAPIのDI用のメソッド
# cf. https://fastapi.tiangolo.com/tutorial/dependencies/
def get_engine() -> sa.engine.Connectable:
    return db_engine


# GET / と POST / の両方で使うレスポンス作成
def makeResponse(
    request: Request, engine: sa.engine.Connectable, error: Optional[str]
) -> Response:
    messages = db.find_all(engine)
    print(messages)
    context = {"request": request, "messages": messages, "error": error}
    return templates.TemplateResponse("index.html", context)


@app.get("/", response_class=HTMLResponse)
async def get(
    request: Request, engine: sa.engine.Connectable = Depends(get_engine)
) -> Response:
    return makeResponse(request, engine, None)


@app.post("/", response_class=HTMLResponse)
async def post(
    request: Request,
    engine: sa.engine.Connectable = Depends(get_engine),
    message: Optional[str] = Form(None),
) -> Response:
    error_msg = None
    if not message:
        error_msg = "何か書いてください"
    elif len(message) != setting.message_length:
        error_msg = "投稿は3文字限定です"
    else:
        db.add(engine, Message(body=message))

    return makeResponse(request, engine, error_msg)


@app.post("/delete-all", response_class=HTMLResponse)
async def delete_all(
    request: Request,
    engine: sa.engine.Connectable = Depends(get_engine),
) -> Response:
    db.delete_all(engine)
    return makeResponse(request, engine, None)


@app.post("/delete", response_class=HTMLResponse)
async def remove(
    request: Request,
    engine: sa.engine.Connectable = Depends(get_engine),
    delete_id: Optional[str] = Form(None),
) -> Response:
    error_msg = None
    if delete_id is None:
        error_msg = "不正な削除です"
    else:
        delete_id = int(delete_id)
        db.remove(engine, delete_id)

    return makeResponse(request, engine, error_msg)


@app.post("/update/{message_id}", response_class=HTMLResponse)
async def update(
    request: Request,
    message_id: str,
    engine: sa.engine.Connectable = Depends(get_engine),
    bookmark: Optional[bool] = Form(None),
) -> Response:
    message_id = int(message_id)
    error_msg = None
    if bookmark is None:
        error_msg = "不正な更新です"
    else:
        print(f"id:{message_id}のbookmarkを{bookmark}にしました")
        db.update(engine, message_id, bookmark)

    return makeResponse(request, engine, error_msg)
