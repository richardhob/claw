
import sys
import ctypes
import dwfconstants 

# CLI Application which can be used to set the output voltage on either (or
# both) Analog output channels
#
# This is basically for debugging.

c_false = ctypes.c_int(0)
c_true = ctypes.c_int(1)

def get_dll():
    ''' Get the DLL based on the system (copied from DWF example) '''
    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    return dwf

def get_device(dll, device_id=-1):
    ''' Use the DLL to get the device instance
    '''
    device_obj = ctypes.c_int()
    dll.FDwfDeviceOpen(device_id, ctypes.byref(device_obj))
    return device_obj

def set_voltage(dll, device, channel, voltage):
    ''' Set the output voltage on the provided channel 

    Args:
         dll: dll (from get_dll)
         device: device (from get_device)
         channel: -1 for both channels, 0 for the first channel, 1 for the
             second channel
         voltage: Voltage to apply (0.0 to 5.0 V)
    '''
    c = ctypes.c_int(channel)
    v = ctypes.c_double(voltage)
    ac = dwfconstants.AnalogOutNodeCarrier

    dll.FDwfDeviceAutoConfigureSet(device, c_false)
    dll.FDwfAnalogOutNodeEnableSet(device, c, ac, c_true)
    dll.FDwfAnalogOutNodeFunctionSet(device, c, ac, dwfconstants.funcDC)
    dll.FDwfAnalogOutNodeOffsetSet(device, c, ac, v)
    dll.FDwfAnalogOutConfigure(device, c, c_true)

def close(dll, device):
    ''' Properly shut down the device. '''
    pass

def main():
    pass

if __name__ == '__main__':
    main()
