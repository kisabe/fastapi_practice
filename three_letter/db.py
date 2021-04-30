import sqlalchemy as sa

from three_letter.models import Message

metadata = sa.MetaData()
message_table = sa.Table(
    "messages",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("body", sa.String(256), nullable=False),
    sa.Column(
        "created_at",
        sa.DateTime,
        nullable=False,
    ),
)


def create_table(engine: sa.engine.Connectable) -> None:
    metadata.create_all(engine)


def find_all(engine: sa.engine.Connectable) -> list[Message]:
    """投稿メッセージを全部取得"""
    with engine.connect() as connection:
        query = sa.sql.select(
            (message_table.c.id, message_table.c.body, message_table.c.created_at)
        )
        return [Message(**m) for m in connection.execute(query)]


def add(engine: sa.engine.Connectable, message: Message) -> None:
    """メッセージの保存"""
    with engine.connect() as connection:
        query = message_table.insert()
        connection.execute(query, message.dict())


def remove(engine: sa.engine.Connectable, message_id: int) -> None:
    """メッセージの削除"""
    with engine.connect() as connection:
        query = message_table.delete().where(message_table.c.id == message_id)
        connection.execute(query)


def delete_all(engine: sa.engine.Connectable) -> None:
    """メッセージをすべて消す（テスト用）"""
    with engine.connect() as connection:
        connection.execute(message_table.delete())
