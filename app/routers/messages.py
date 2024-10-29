import json
from requests import post, get
from fastapi import APIRouter, Depends, Request

from ..schemas import SendMessage, WhappiMessage, Config, ReceivedMessage
from ..config import WhapiSettings, get_WhapiSetting

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
        company = 'liveseo'
        for message in messages:
            json_string = message.model_dump()
            url = f'http://{company}.localhost:8000/api/v1/webhook/messages' #TODO: URL in .env

            post(url, json=json_string)
        return

    def convert(whapiMessage: WhappiMessage.message) -> ReceivedMessage:
        Message = ReceivedMessage(
            message_id = whapiMessage.id,
            chat_id = whapiMessage.chat_id,
            from_number = whapiMessage.whapi_from,
            content = whapiMessage.text.body,
            type = whapiMessage.type.capitalize(),
            timestamp= whapiMessage.timestamp,
            from_name=whapiMessage.from_name     
        )
        return Message
    
    lstMessages = [convert(obj) for obj in content.messages]
    sendBack(lstMessages)
    return  

@router.get("/group")
async def group_data(skip: int, take: int, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)):
    result: list = []
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {whapiSetting.Token}'
    }

    def get_messages(groupId):
        group_message: list = []
        messages = get(
            url=f"{whapiSetting.Url}/messages/list/{groupId}?count=10&sort=desc",
            headers=headers
        ).json()

        for message in messages['messages']:
            if (message['type'] != 'text'):
                continue

            message_text = message.get('text', 'Mensagem Texto')
            text_content = 'Sem Conteudo'
            if (not isinstance(message_text, str)):
                text_content = message_text.get('body', 'Conteudo Texto')

            group_message.append({
                'message_id': message['id'],
                'from_name': message.get('from_name', ''),
                'from_number': message['from'],
                'content': text_content, 
                'type': message['type'].capitalize(),
                'timestamp': message['timestamp'],
                'received': True
            })
        return group_message

    url = f'{whapiSetting.Url}/groups?count={take}&offset={skip}'
    response = get(
            url=url,
            headers=headers
        )

    groups = response.json()
    for group in groups["groups"]:        
        group_detail = get(
            url=f"{whapiSetting.Url}/groups/{group['id']}",
            headers=headers
        ).json()

        numbers_array = [item['id'] for item in group['participants']]

        group_message = get_messages(group['id'])

        result.append({
            'chat_id': group['id'],
            'name': group['name'],
            'imageUrl': group_detail.get('chat_pic'),
            'messages': group_message,
            'numbers': numbers_array
        })

    return result

@router.post('/config')
async def config(config: Config, whapiSetting: WhapiSettings = Depends(get_WhapiSetting)):
    whapiSetting.Token = config.token
    whapiSetting.Phone = config.phone
    return