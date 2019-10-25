# Welcome to Harmony!
With all the different IoT providers out there, it's not easy for developers to get them to talk to each other. That's what Harmony is for.

## About
Harmony is a protocol for how IoT devices should be defined, and how they should communicate with each other.

Each Harmony device defines a list of "getters" and "setters", which are used to pass information to and from devices. They also have the ability to emit and listen to events from other Harmony devices.

## Installation
To install harmony for Python, run `pip install harmony-device`

## Definitions
Harmony uses a few special terms to describe the interactions between devices.
- Device - A device or node is simply an instance of the Harmony server. You can have multiple harmony devices running on the same computer, or have them running on separate computers.
- Attribute - An attribute is some piece of data that is assosciated with a device. The attributes of a harmony device give other devices a simple interface to read and/or write the state of that device. For example, if your device was a thermostat, it might have a `temperature` attribute, so other harmony devices can easily read the temperature.
- Getter - A getter is a function within an attribute that contains the actual code necessary to get the required data. Going back to the thermostat example, you may not be able to simply read the temperature from a variable - you might have to retrieve through some device-specific code.
- Setter - A setter is a function within an attribute that contains the code necessary to change the required data. Like the getter, it is not always relevant, but between the two you should be able to do any operation you need.

## Using Harmony
Creating your first harmony device is extremely simple:
```
#Import the HarmonyDevice and Attribute classes
from harmony_device import HarmonyDevice, Attribute

#Create an instance of the class
device = HarmonyDevice()

#For each attribute you need in your device, add a subclass of Attribute
class MsgAttr:
    #Give the attribute a name. This must be unique.
    name = 'message'

    #Optionally give the attribute a description
    description = 'Manages a message to be viewed and edited by the user'

    #Your attributes can retrieve data from anyplace you like - files, sensors, etc.
    #You can also define class variables to store information as seen here: 
    msg = 'Hello, World!'

    #Neither the getter or the setter function is required (i.e. you can make a getter but not a setter and vice versa, or an attribute with no getter or setter at all). 
    #These functions open the attribute to be viewed (getter) or edited (setter) by other devices.

    #The getter function requires the `params` parameter. This parameter carries miscellaneous information sent from the device requesting the attribute (for example, if you wanted to have 4 messages, you might choose one by adding a `messageId` in the parameters when asking for the attribute) 
    def getter(self, params):
        #The getter must return a JSON-serializable object (str, int, dict, list, etc.)
        return msg

    #The setter function requires the `params` parameter, which works just like the getter, and also a `value`- i.e., the value to set the attribute to. 
    def setter(self, value, params):
        msg = value #The setter doesn't necessarily have to return anything
        



#Now, simply call the run method to start the harmony device server!
device.run(port=5000)
```

### Using Listeners
Sometimes, you may want one device to run some code when a certain event occurs on another device. For example, you might have a system where a camera performs facial recognition on people at the front door, and when it determines whether they are allowed in, it unlocks the door.

In harmony, this can be accomplished using *Listeners*. Listeners allow one device to "listen" for when another device emits a certain event. The other device doesn't need to know anything about the listening device, it just tells that device when an event occurs.

Here's an example of how you might add a listener:

On the first device:
```
from harmony_device import HarmonyDevice, Listener, Attribute

device = HarmonyDevice(id='listener')
other_device = HarmonyDevice(id='emitter', port=5001)

class MessageChangedListener(Listener):
    event = "message_changed"
    device = other_device
    
    def callback(self, data):
        print("The message on the other device was changed to: '{}''".format(data['message']))


device.add_listener(MessageChangedListener)

device.run(port=5000) 

```

On the second device:
```
from harmony_device import HarmonyDevice, Attribute

device = HarmonyDevice(port=5001)

class MsgAttr(Attribute):
    name = 'message'
    msg = 'Hello, World!'    

    def getter(self, params):
        return self.msg
    def setter(self, value, params):
        self.msg = value
        
        #Now we emit the 'message_changed' event
        device.emit('message_changed')


```


*Note that the second device has to be running in order for the first device to listen to it. This means your devices may have to be started up in a certain order.*


You also might wonder whether you can emit an event from some other file running a different piece of code. You certainly can! You just have to import your `device` variable into that file using Python's singleton pattern, and then you can emit the events from that file.

This really only works if the harmony server is written in the same language as the one you are wanting to emit events from. Unfortunately, we only support Python as of right now, though I plan to add C++, Java, and JavaScript versions at some point as well.


## Disclaimer

This system is not meant to magically work with every IoT device. It's an abstraction layer that allows us to write code that can *potentially* work with many IoT devices - so long as they have their getters and setters defined correctly.


## Supported Languages
Currently, Python is the only supported language, but I'm hoping to add C++, Java, and NodeJS as well.
