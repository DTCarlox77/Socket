from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['code']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        return await super().disconnect(close_code)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        
        if data['type'] == 'message':
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message', # Necesito generar ahora un método que tenga exactamente este nombre
                    'message': data['message'],
                }
            )
            
        elif data['type'] == 'alert':
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'alert',
                    'message': data['message'],
                }
            )
            
    async def alert(self, event):
        
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'type': 'alert',
            'message': message,
        }))
            
    async def chat_message(self, event):
        
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'timestamp': timezone.now().time().strftime('%H:%M:%S')
        }))