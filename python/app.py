from harmony_device import HarmonyDevice, Attribute


#Create an instance of the class
device = HarmonyDevice()


class MsgAttr(Attribute):
    name = "message"
    msg = "Hello"
    def getter(self, params):
        return self.msg
    def setter(self, value, params):
        self.msg = value
device.add_attribute(MsgAttr)

#Now, simply call the run method to start the harmony device server!
device.run(port=5000)
