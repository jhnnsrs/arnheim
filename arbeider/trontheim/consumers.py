from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db import models
from rest_framework import serializers

from trontheim.exceptions import ClientError


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
            print("No authentification was provided. Reject connection. Please verify that user has logged in.")
            await self.close()
        else:
            # Accept the connection
            print("Authenntification was provided. Accepting the connection")
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
        print(content)
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
            print("Something went wrong")

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



class OsloJobConsumer(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.publishers = None
        self.job = None
        self.data = None


    async def register(self,data):
        self.publishers = dict(data["publishers"])
        self.job = data["job"]
        self.data = data
        print("Starting a Job" + type(self).__name__)

    async def modelCreated(self, model: models.Model, serializerclass: serializers.ModelSerializer.__class__, method: str):
        '''Make sure to call this if you created a new Model on the Database so that the actionpublishers can do their work'''
        serialized = serializerclass(model)
        stream = str(serialized.Meta.model.__name__).lower()
        if stream in self.publishers.keys():
            print("Found stream {0} in Publishers. Tyring to publish".format(str(stream)))
            await self.publish(serialized, method,self.publishers[stream],stream)

    async def publish(self,serializer, method, publishers,stream):
        if publishers is not None:
            for el in publishers:
                path = ""
                for modelfield in el:
                    try:
                        value = serializer.data[modelfield]
                        path += "{0}_{1}_".format(str(modelfield), str(value))
                    except:
                        print("Modelfield {0} does not exist on {1}".format(str(modelfield), str(stream)))
                        path += "{0}_".format((str(modelfield)))
                path = path[:-1]
                print("Publishing to Channel {0}".format(path))

                await self.channel_layer.group_send(
                    path,
                    {
                        "type": "stream",
                        "stream": stream,
                        "room": path,
                        "method": method,
                        "data": serializer.data
                    }
                )