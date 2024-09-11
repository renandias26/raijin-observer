from pydantic import BaseModel, Field

class TypeEnum(BaseModel):
    Text: int = 1
    Image: int = 2
    Audio: int = 3
    Video: int = 4

class SendMessage(BaseModel):
    to: str
    type: TypeEnum | None = None
    body: str
    media_text: str | None = None
    quoted: str | None = None
    view_once: bool | None = None
    mentions: list[str] | None = None

class ReceivedMessage(BaseModel):

    class quotedMap(BaseModel):
        author: str
        message_id: str

    message_id: str
    chat_id: str
    from_number: str
    from_name: str = None
    to_number: str
    type: str
    content: str
    media_text: str = None
    quoted: quotedMap = None
    view_once: bool = False
    mentions: list[str] = None
    timestamp: int

class WhappiMessage(BaseModel):  
    
    class message(BaseModel):
        class textMap(BaseModel):
            body: str

        chat_id: str
        chat_name: str
        whapi_from: str = Field(alias='from')
        from_name: str
        id: str
        text: textMap
        type: str
        timestamp: int

    messages: list[message]

class Config(BaseModel):
    token: str
    phone: str