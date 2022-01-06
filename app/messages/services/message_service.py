from typing import Optional
from app.messages.entities.message_entity import Message
from app.messages.repositories.message_repository import find_message_by_id, find_all_messages, insert_message, increment_messsage_claps_by_id


def get_message_by_id(message_id: int) -> Optional[Message]:
    return find_message_by_id(message_id=message_id)


def get_all_messages() -> list[Message]:
    return find_all_messages()


def create_message(author, message):
    if not author:
        return None, 'Требуется ввести имя отправителя'
    if not message:
        return None, 'Требуется ввести сообщение'

    if len(author) > 30:
        return None, 'Имя автора должно быть от 1 до 30 символов'
    if len(message) > 1000:
        return None, 'Текст сообщения должен быть от 1 до 1000 символов'

    new_message = insert_message(
        Message(author=author, message=message, claps=0))
    return new_message, None


def increment_claps_by_id(message_id) -> int:
    return increment_messsage_claps_by_id(message_id)
