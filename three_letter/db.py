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
        server_default=sa.sql.functions.current_timestamp(),
    ),
)


def create_table(engine: sa.engine.Connectable) -> None:
    metadata.create_all(engine)


def find_all(engine: sa.engine.Connectable) -> list[Message]:
    """投稿メッセージを全部取得"""
    with engine.connect() as connection:
        query = sa.sql.select(
            (
                message_table.c.id,
                message_table.c.body,
                message_table.c.created_at.label("createdAt"),
            )
        )
        return [Message(**m) for m in connection.execute(query)]


def add(engine: sa.engine.Connectable, message: Message) -> None:
    """メッセージの保存"""
    with engine.connect() as connection:
        query = message_table.insert()
        connection.execute(query, message.dict())
