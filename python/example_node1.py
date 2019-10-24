from harmony_device import HarmonyDevice, Attribute

device = HarmonyDevice(id="node1")
other_device = HarmonyDevice(remote=True, id="node2", port=5001, ip="192.168.1.97")

class MsgAttr(Attribute):
    name = 'message'
    description = 'A value to be displayed to and edited by the user'
    def getter(self, params):
        return other_device.get('message')
device.add_attribute(MsgAttr)



device.summary()

device.run()
