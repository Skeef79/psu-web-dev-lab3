from typing import Optional


class Message:
    def __init__(self, author: str,  message: str, id: Optional[int] = None,  claps: Optional[int] = None):
        self.id = id
        self.author = author
        self.message = message
        self.claps = claps if claps else 0
