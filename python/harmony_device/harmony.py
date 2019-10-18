import socket
from http.server import HTTPServer
import requests
import json
from .HarmonyClientRequestHandler import createHarmonyClientRequestHandler

class HarmonyDevice:
    id = socket.gethostbyname(socket.gethostname())
    ip = socket.gethostbyname(socket.gethostname())
    port = 5000
    getters = {}
    setters = {}
    event_listeners = []
    event_recipients = {}
    remote = False

    def __init__(self, remote=False, id=socket.gethostbyname(socket.gethostname()), ip=socket.gethostbyname(socket.gethostname()), port=5000):
        self.remote = remote
        self.id = id
        self.ip = ip
        self.port = port

    def summary(self):

        getters = self.add_getters
        setters = self.setters

        if self.remote:
            getters = self.list_getters()
            setters = self.list_setters()

        summary = """
        Device ID: {}
        IP Address: {}
        Harmony Server Port: {}
        Getters: {}
        Setters: {}
        """.format(self.id, self.ip, self.port, getters, setters)

        print(summary)

    def make_request(self, path, params=None):
        url = "http://" + str(self.ip) + ":" + str(self.port) + "/" + path
        print(url)
        if params:
            url += "?"
            for key, value in params.items():
                url += key + "=" + json.dumps(value) + "&"
        url = url[:-1]

        req = requests.get(url)
        return req.json()

    def list_getters(self):
        req = self.make_request("getters")
        return req["getters"]

    def list_setters(self):
        req = self.make_request("setters")
        return req["setters"]


    def get(self, attribute, params=None):
        if self.remote:
            if not params:
                params = {}
            params["attribute"] = attribute
            return self.make_request("get", params=params)
        else:
            return self.getters[attribute](params)

    def set(self, attribute, value, params=None):
        if self.remote:
            if not params:
                params = {}
            params["attribute"] = attribute
            params["value"] = value
            return self.make_request("set", params=params)
        else:
            self.setters[attribute](value, params)

    def add_getters(self, getters):
        if self.remote:
            raise Exception("Not allowed to add getters to remote device")
        for getter in getters:
            if "attribute" in getter and "callback" in getter:
                self.getters[ getter["attribute"] ] = getter["callback"]
            elif "attribute" in getter and "callback" not in getter:
                raise ValueError("Getter '{}' has no callback'".format(getter["attribute"]))
            elif "callback" in getter and "attribute" not in getter:
                raise ValueError("Can't add getter with no attribute")
            else:
                raise ValueError("Getters must be a dict with attribute and callback")

    def add_setters(self, setters):
        if self.remote:
            raise Exception("Not allowed to add setters to remote device")
        for setter in setters:
            if "attribute" in setter and "callback" in setter:
                self.setters[ setter["attribute"] ] = setter["callback"]
            elif "attribute" in setter and "callback" not in setter:
                raise ValueError("Setter '{}' has no callback'".format(setter["attribute"]))
            elif "callback" in setter and "attribute" not in setter:
                raise ValueError("Can't add setter with no attribute")
            else:
                raise ValueError("Setters must be a dict with attribute and callback")
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

        httpd = HTTPServer(('localhost', port), harmonyClientRequestHandler)

        print("Starting Harmony Device Server at localhost:" + str(port) + "...")

        httpd.serve_forever()
