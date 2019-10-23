import os
import importlib

#Probably terrible practice, but it's convenient...
def auto_load_attrs(device, folder):
    for filename in os.listdir(folder):
        classname = filename[:-3]
        attr = importlib.import_module(classname + '.' + classname)
        device.add_attribute(attr)


