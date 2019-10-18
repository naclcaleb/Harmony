from harmony_device import HarmonyDevice

device = HarmonyDevice(id="node1")
other_device = HarmonyDevice(remote=True, id="node2", port=5001, ip="192.168.1.97")

def get_message(params):
    return other_device.get("message")

device.add_getters([{"attribute": "message", "callback": get_message}])

device.run()
