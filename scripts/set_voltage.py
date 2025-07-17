
import sys
import ctypes
import argparse

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
        dwf = ctypes.cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = ctypes.cdll.LoadLibrary("libdwf.so")

    return dwf

def get_device(dll, device_id=-1):
    ''' Use the DLL to get the device instance
    '''
    device_obj = ctypes.c_int()
    dll.FDwfDeviceOpen(device_id, ctypes.byref(device_obj))
    return device_obj

def dll_set_param(dll, param, value):
    ''' Configure a DLL parameter.

    Example: Configure the device to continue running on close

    >>> dll_set_param(dll, dwfconstants.DwfParamOnClose, ctypes.c_int(0))
    '''
    dll.FDwfParamSet(param, value)

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
    dll.FDwfDeviceClose(device)

def main(args):
    dll = get_dll()

    # 0 continue, 1 stop, 2 shutdown
    dll_set_param(dll, dwfconstants.DwfParamOnClose, ctypes.c_int(0))

    # Not sure if I need this one - 0 disable, 1 enable
    dll_set_param(dll, dwfconstants.DwfParamAnalogOut, ctypes.c_int(1))

    device = get_device(dll, args.device)
    set_voltage(dll, device, args.channel, args.voltage)

def parse():
    parser = argparse.ArgumentParser("")
    parser.add_argument("channel", help="Channel to configure. -1, 0, 1 (-1 for both)", type=int)
    parser.add_argument("voltage", help="Voltage to set (0 to 5 V)", type=float)
    parser.add_argument("--device", help="Device ID. Default is -1 (first found device)", type=int)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse()
    main(args)
