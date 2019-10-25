from http.server import BaseHTTPRequestHandler
import json

#TODO: Create endpoints for subscribing to notifications and emitting notifications
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
                    if params['attribute'] in harmony_device.attrs and harmony_device.attrs[params['attribute']].getter != None:
                        data = harmony_device.get(params["attribute"], params)
                    else:
                        data = { "error": "No getter exists for attribute '{}'".format(params['attribute']) } 

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
                    if params['attribute'] in harmony_device.attrs and harmony_device.attrs[params['attribute']].setter != None:
                        data = harmony_device.set(params["attribute"], params["value"], params)
                    else:
                        data = { "error": "No setter exists for attribute '{}'".format(params['attribute']) } 
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
            if path =="/notify":
                try: 
                    if 'event' not in params:
                        self.wfile.write('{"error": "No event name given"}')
                    else:
                        harmony_device.recieveNotification(params['event'])
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                except Exception as err:
                    print(err)
                    self.send_response(500)
                    self.end_headers()
                    return
                
            return
    return HarmonyClientRequestHandler
