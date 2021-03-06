from harmony_device import HarmonyDevice, Attribute

device = HarmonyDevice(id="node2")

class MsgAttr(Attribute):
    name = 'message'
    msg = 'Hello'
    def getter(self, params):
        return self.msg
    def setter(self, value, params):
        self.msg = value

device.add_attribute(MsgAttr)
device.run(port=5001)
