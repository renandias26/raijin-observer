import json
from fastapi import APIRouter, Depends
from ..schemas import SendMessage, WhappiMessage, Config, ReceivedMessage
from ..config import WhapiSettings, get_WhapiSetting
from requests import post

router = APIRouter()


@router.post("/send-message")
async def send_message(message: SendMessage, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)):
    url = f'{whapiSetting.Url}/messages/text'
    
    payload = {
        "to": message.to,  # "120363217209632703@g.us" RaijinGroupID
        "body": message.content
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {whapiSetting.Token}'
    }

    response = post(url, json=payload, headers=headers)

    return response.json()

@router.post('/received-messages')
async def whatsapp_webhook(content: WhappiMessage):

    def convert(whapiMessage: WhappiMessage.message, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)) -> ReceivedMessage:
        Message = ReceivedMessage()
        Message.message_id = whapiMessage.id
        Message.chat_id = whapiMessage.chat_id
        Message.message_from = whapiMessage.whapi_from
        Message.to = whapiSetting.Phone
        Message.type = whapiMessage.type
        Message.content = whapiMessage.text.body
        return Message
        
    from pprint import pprint
    lstMessages = [convert(obj) for obj in content.messages]
    pprint(lstMessages)

@router.post('/config')
async def config(config: Config, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)):
    whapiSetting.Token = config.token
    whapiSetting.Phone = config.phone
    return