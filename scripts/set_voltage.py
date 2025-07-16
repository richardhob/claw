
import sys
import ctypes
import dwfconstants 

# CLI Application which can be used to set the output voltage on either (or
# both) Analog output channels
#
# This is basically for debugging.

def get_dll():
    ''' Get the DLL based on the system (copied from DWF example) '''
    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    return dwf

def get_device(dll, num=-1):
    ''' Use the DLL to get the device instance
    '''
    pass

def set_voltage(dll, device, channel, voltage):
    ''' Set the output voltage on the provided channel 

    Args:
         dll: dll (from get_dll)
         device: device (from get_device)
         channel: 
         voltage: 
    '''
    pass

def close(dll, device):
    ''' Properly shut down the device. '''
    pass

def main():
    pass

if __name__ == '__main__':
    main()
