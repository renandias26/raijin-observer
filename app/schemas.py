from pydantic import BaseModel, Field

class TypeEnum(BaseModel):
    Text: int = 1
    Image: int = 2
    Audio: int = 3
    Video: int = 4

class SendMessage(BaseModel):
    to: str
    type: TypeEnum
    content: str
    media_text: str | None
    quoted: str | None
    view_once: bool | None
    mentions: list[str]

class ReceivedMessage():

    class quotedMap():
        author: str
        message_id: str

    message_id: str
    chat_id: str
    message_from: str
    from_name: str
    to: str
    type: str
    content: str
    media_text: str
    quoted: quotedMap
    view_once: str
    mentions: list[str]

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

    messages: list[message]

class Config(BaseModel):
    token: str
    phone: str