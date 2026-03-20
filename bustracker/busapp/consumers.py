import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class BusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.bus_id = self.scope['url_route']['kwargs']['bus_id']
        self.group_name = f"bus_{self.bus_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add("all_buses", self.channel_name)
        await self.accept()

        # Load real bus name and route from DB
        bus = await self.get_bus(self.bus_id)
        self.bus_name  = bus['name']  if bus else f"Bus {self.bus_id}"
        self.bus_route = bus['route'] if bus else "Campus Route"

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_discard("all_buses", self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        if data.get('type') == 'location_update':
            payload = {
                "type":   "location_update",
                "bus_id": self.bus_id,
                "lat":    data.get("lat"),
                "lng":    data.get("lng"),
                "speed":  data.get("speed", 0),
                "name":   self.bus_name,   # real name from DB
                "route":  self.bus_route,  # real route from DB
            }
            await self.channel_layer.group_send(self.group_name, payload)
            await self.channel_layer.group_send("all_buses", payload)
            await self.save_location(data)

    async def location_update(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_bus(self, bus_id):
        try:
            from busapp.models import Bus
            bus = Bus.objects.get(id=bus_id)
            return {'name': bus.name, 'route': bus.route}
        except Exception:
            return None

    @database_sync_to_async
    def save_location(self, data):
        try:
            from busapp.models import Bus, BusLocation
            bus = Bus.objects.get(id=self.bus_id)
            BusLocation.objects.create(
                bus=bus,
                latitude=data.get('lat'),
                longitude=data.get('lng'),
                speed=data.get('speed', 0),
            )
            bus.is_active = True
            bus.save(update_fields=['is_active'])
        except Exception as e:
            print(f"[WS] DB save error: {e}")


class AllBusesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("all_buses", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("all_buses", self.channel_name)

    async def receive(self, text_data):
        pass

    async def location_update(self, event):
        await self.send(text_data=json.dumps(event))