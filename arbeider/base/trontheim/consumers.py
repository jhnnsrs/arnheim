from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db import models
from rest_framework import serializers

from trontheim.exceptions import ClientError

from larvik.logging import get_module_logger

logger = get_module_logger(__name__)

class OsloConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """

        # Are they logged in?
        if not self.scope["user"]:
            await self.close()
            return
        if self.scope["user"].is_anonymous:
            # Reject the connection
            logger.info("No authentification was provided. Reject connection. Please verify that user has logged in.")
            await self.close()
        else:
            # Accept the connection
            logger.info("Authentification was provided. Accepting the connection")
            await self.accept()


        self.rooms = dict()


        # Store which rooms the user has joined on this connection

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        try:
            if self.rooms:
                for alias, room_id in self.rooms:
                    try:
                        await self.leave_room(alias)
                    except ClientError:
                        pass
        except:
            pass


    async def join_room(self, room_id,alias):
        """
        Called by receive_json when someone sent a join command.
        """

        #TODO: Maybe joining the same room twice is not smart?
        # Store that we're in the room
        self.rooms[alias] = room_id
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room_id,
            self.channel_name,
        )
        # Instruct their client to finish opening the room
        await self.send_json({
            "joined": str(room_id),
            "alias": str(alias)
        })

    async def leave_room(self, alias):
        """
        Called by receive_json when someone sent a leave command.
        """
        room_id = self.rooms[alias]
        # Remove that we're in the room
        # Remove them from the group so they no longer get room messages
        # Instruct their client to finish closing the room
        await self.channel_layer.group_discard(
            room_id,
            self.channel_name,
        )
        await self.send_json({
            "left": str(room_id),
            "alias": alias
        })
        del self.rooms[alias]

    async def receive_json(self, content, **kwargs):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        :param **kwargs:
        """
        command = content.get("command", None)
        alias = content.get("alias",None)
        try:
            if command == "sub":
                # Make them join the room
                await self.join_room(content["room"],alias=alias)
            elif command == "leave":
                # Leave the room
                await self.leave_room(alias)

        except:
            logger.error("Something went wrong")

    async def stream(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        for alias, room_id in self.rooms.items():
            if room_id == event["room"]:
                await self.send_json(
                    {
                        "room": event["room"],
                        "alias": alias,
                        "method": event["method"],
                        "stream": event["stream"],
                        "data": event["data"]
                    },
                )
