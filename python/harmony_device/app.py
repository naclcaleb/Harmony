from harmony import HarmonyDevice

#Create an instance of the class
device = HarmonyDevice()


#Define your getter functions (the params parameter passes any extra parameters from the request to your function)
def message_getter(params):
  #Return the getter data
  with open("./message.txt", "r") as file:
      message = file.read()
  return message

#Define you setter functions
def message_setter(value, params):
  #Set the message
  with open('./message.txt', 'w') as file:
      file.write(value)

  #Return
  return ""

#Now, add the getters and setters to the device
device.add_getters([
  {
    "attribute": "message",
    "callback": message_getter
  }
])

device.add_setters([
  {
    "attribute": "message",
    "callback": message_setter
  }
])

#Now, simply call the run method to start the harmony device server!
device.run(port=5000)
