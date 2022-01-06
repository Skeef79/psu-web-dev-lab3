from typing import Optional
import psycopg2
from app.messages.entities.message_entity import Message
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

conn_params = {
    'dbname': os.environ.get('DBNAME'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT')
}

conn = psycopg2.connect(**conn_params)


def convert_to_classes(messages):
    return [Message(id=msg[0], author=msg[1], message=msg[2], claps=msg[3]) for msg in messages]


def insert_message(message: Message) -> Message:
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO messages(author, message,claps) VALUES(%s,%s,%s) RETURNING id',
                       (message.author,  message.message, message.claps))
        id = cursor.fetchone()[0]
        conn.commit()
        return Message(id, message.author, message.message, message.claps)


def find_message_by_id(message_id) -> Optional[Message]:
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM messages WHERE id = %s', (message_id,))
        messages = cursor.fetchall()
        if not messages:
            return None

        message = convert_to_classes(messages)[0]        
        return message


def find_all_messages() -> list[Message]:
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM messages ORDER BY claps DESC')
        messages = cursor.fetchall()
        return convert_to_classes(messages)


def increment_messsage_claps_by_id(message_id: int) -> int:
    with conn.cursor() as cursor:
        cursor.execute(
            'UPDATE messages SET claps = claps+1 WHERE id = %s', (message_id,))
        
        message = find_message_by_id(message_id=message_id)
        if not message:
            return None
        return message.claps

