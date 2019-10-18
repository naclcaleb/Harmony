from harmony_device import HarmonyDevice

device = HarmonyDevice(id="node2")

def get_message(params):
    return "Hello!"

device.add_getters([{"attribute": "message", "callback": get_message}])

device.run(port=5001)
