import socket
from http.server import HTTPServer
import requests
import json
from .HarmonyClientRequestHandler import createHarmonyClientRequestHandler

class HarmonyDevice:
    id = socket.gethostbyname(socket.gethostname())
    ip = '0.0.0.0' #socket.gethostbyname(socket.gethostname())
    port = 5000
    attrs = {} 
    event_listeners = []
    event_recipients = {}
    remote = False

    def __init__(self, remote=False, id=socket.gethostbyname(socket.gethostname()), ip='0.0.0.0', port=5000):
        self.remote = remote
        self.id = id
        self.ip = ip
        self.port = port

    def summary(self):

        attrs = self.attrs
        if self.remote:
            attrs = self.list_attrs()

        summary = """
Device ID: {}
IP Address: {}
Harmony Server Port: {}
Attributes ({} total):""".format(self.id, self.ip, self.port, len(attrs))
        for key, attr in attrs.items():
            summary += "\n\t- Name: {}\n".format(attr.name)
            if len(attr.description) > 0:
                summary += "\t  Description: {}\n".format(attr.description)

        print(summary)

    def make_request(self, path, params=None):
        url = "http://" + str(self.ip) + ":" + str(self.port) + "/" + path
        print(url)
        if params:
            url += "?"
            for key, value in params.items():
                url += key + "=" + str(value) + "&"
        url = url[:-1]
        print(url)
        req = requests.get(url)
        return req.json()

    def list_attributes(self):
        attrs = self.attrs
        if self.remote:
            attrs = self.make_request("attributes")["attrs"]
        return attrs

    def add_attribute(self, attribute):
        attr_instance = attribute()
        self.attrs[attr_instance.name] = attr_instance

    def add_attributes(self, attributes):
        for attribute in attributes:
            self.add_attribute(attribute)



    def get(self, attribute, params=None):
        if self.remote:
            if not params:
                params = {}
            params["attribute"] = attribute
            return self.make_request("get", params=params)
        else:
            return self.attrs[attribute].getter(params)

    def set(self, attribute, value, params=None):
        if self.remote:
            if not params:
                params = {}
            params["attribute"] = attribute
            params["value"] = value
            return self.make_request("set", params=params)
        else:
            self.attrs[attribute].setter(value, params)

    #Listens to an event from another device
    def add_listener(self, harmony_device, event, callback):
        if self.remote:
            raise Exception("Not allowed to add listener to remote device")
        if isinstance(harmony_device, HarmonyDevice):
            self.event_listeners.append({ "device": harmony_device, "name": event, "callback": callback })
        else:
            raise ValueError("Listeners must be instances of HarmonyDevice")

    #Adds a device to recieve a specific event
    def add_recipient(self, harmony_device, event):
        if isinstance(harmony_device, HarmonyDevice):
            if event not in self.event_recipients:
                self.event_recipients[event] = []

            self.event_recipients[event].append(harmony_device)

            self.make_request("recipients/add", {
                "id": harmony_device.id,
                "ip": harmony_device.ip,
                "event": event
            })
        else:
            raise ValueError("Recipients must be instances of HarmonyDevice")

    def emit(self, event):
        if self.remote:
            raise Exception("Not allowed to emit events from remote device")
        for recipient in self.event_recipients[ event["name"] ]:
            recipient.recieveNotification(event)

    def recieveNotification(self, event):
        if self.remote:
            self.make_request("notify", {
                "event": event["name"],
                "data": event["data"]
            })
        else:
            for listener in self.event_listeners:
                if listener["name"] == event["name"] and listener["device"] == event["device"]:
                    listener["callback"]()

    def run(self, port=5000):
        if self.remote:
            raise Exception("Cannot run server on remote device")
        self.port = port
        harmonyClientRequestHandler = createHarmonyClientRequestHandler(self)

        httpd = HTTPServer((self.ip, port), harmonyClientRequestHandler)

        print("Starting Harmony Device Server at " + str(self.ip) + ":" + str(port) + "...")

        httpd.serve_forever()
