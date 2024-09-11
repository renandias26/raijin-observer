import json
from fastapi import APIRouter, Depends, Request
from ..schemas import SendMessage, WhappiMessage, Config, ReceivedMessage
from ..config import WhapiSettings, get_WhapiSetting
from requests import post

router = APIRouter()


@router.post("/send-message")
async def send_message(req: Request, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)):
    obj = json.loads(await req.json())
    url = f'{whapiSetting.Url}/messages/text'
    message = SendMessage(
        to=obj['to'],
        body=obj['body']
    )
    payload = {
        "to": message.to,  # "120363217209632703@g.us" RaijinGroupID
        "body": message.body
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {whapiSetting.Token}'
    }

    response = post(url, json=payload, headers=headers)

    return response.json()

@router.post('/received-messages')
async def whatsapp_webhook(content: WhappiMessage, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)):
    def sendBack(messages: list[ReceivedMessage]):
        for message in messages:
            json_string = message.model_dump()
            url = 'http://matera.localhost:8000/api/v1/webhook/messages/' #TODO: URL in .env

            post(url, json=json_string)
        return

    def convert(whapiMessage: WhappiMessage.message) -> ReceivedMessage:
        Message = ReceivedMessage(
            message_id = whapiMessage.id,
            chat_id = whapiMessage.chat_id,
            from_number = whapiMessage.whapi_from,
            to_number = whapiSetting.Phone,
            content = whapiMessage.text.body,
            type = whapiMessage.type.capitalize(),
            timestamp= whapiMessage.timestamp
        )
        return Message
    
    lstMessages = [convert(obj) for obj in content.messages]
    sendBack(lstMessages)
    return  

@router.post('/config')
async def config(config: Config, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)):
    whapiSetting.Token = config.token
    whapiSetting.Phone = config.phone
    return