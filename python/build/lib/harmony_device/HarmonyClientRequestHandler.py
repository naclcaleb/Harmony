from http.server import BaseHTTPRequestHandler
import json


def createHarmonyClientRequestHandler(harmony_device):
    class HarmonyClientRequestHandler(BaseHTTPRequestHandler):

        harmony_device = None

        def __init__(self, *args, **kwargs):
            self.harmony_device = harmony_device
            super(HarmonyClientRequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):
            url = self.path.split("?")
            path = url[0]
            params_list = []
            print(url)
            if len(url) > 1:
                params_list = url[1].split("&")
            params = {}
            for param in params_list:
                components = param.split("=")
                params[ components[0] ] = components[1]
            if path == "/get":
                try:
                    data = harmony_device.get(params["attribute"], params)

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
                    return
                except Exception as err:
                    print(err)
                    self.send_response(500)
                    self.end_headers()
                    return
            if path == "/set":
                try:
                    data = harmony_device.set(params["attribute"], params["value"], params)
                    if not data:
                        data = "success"
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
                    return
                except Exception as err:
                    print(err)
                    self.send_response(500)
                    self.end_headers()
                    return
            return
    return HarmonyClientRequestHandler
