
import ctypes
import unittest.mock as mock

import pytest

import dwfconstants

# Script under test
import set_voltage

@pytest.fixture(scope='function')
def mock_dll():
    return mock.MagicMock()

@pytest.fixture(scope="function")
def mock_device():
    return mock.MagicMock()

def test_get_device(mock_dll):
    device = set_voltage.get_device(mock_dll, "device_id")
    mock_dll.FDwfDeviceOpen.assert_called_once()
    assert mock_dll.FDwfDeviceOpen.call_args_list[0][0][0] == 'device_id'

CHANNELS = [i for i in (-1, 0, 1)]
VOLTAGES = [float(i)/10 for i in range(0, 20, 10)]

@pytest.mark.parametrize("channel", CHANNELS)
@pytest.mark.parametrize("voltage", VOLTAGES)
def test_set_voltage(mock_dll, mock_device, channel, voltage):
    ac = dwfconstants.AnalogOutNodeCarrier.value
    set_voltage.set_voltage(mock_dll, mock_device, channel, voltage)

    # Can't use `assert_called_once_with` because the c_int equality doesn't
    # work. c_int(0) != c_int(0) (at least not right now)
    mock_dll.FDwfDeviceAutoConfigureSet.assert_called_once()
    assert mock_dll.FDwfDeviceAutoConfigureSet.call_args_list[0][0][0] == mock_device
    assert mock_dll.FDwfDeviceAutoConfigureSet.call_args_list[0][0][1].value == 0

    mock_dll.FDwfAnalogOutNodeEnableSet.assert_called_once()
    assert mock_dll.FDwfAnalogOutNodeEnableSet.call_args_list[0][0][0] == mock_device
    assert mock_dll.FDwfAnalogOutNodeEnableSet.call_args_list[0][0][1].value == channel
    assert mock_dll.FDwfAnalogOutNodeEnableSet.call_args_list[0][0][2].value == ac
    assert mock_dll.FDwfAnalogOutNodeEnableSet.call_args_list[0][0][3].value == 1

    mock_dll.FDwfAnalogOutNodeFunctionSet.assert_called_once()
    mock_dll.FDwfAnalogOutNodeFunctionSet.call_args_list[0][0][0] == mock_device
    mock_dll.FDwfAnalogOutNodeFunctionSet.call_args_list[0][0][1].value == channel
    mock_dll.FDwfAnalogOutNodeFunctionSet.call_args_list[0][0][2].value == ac
    mock_dll.FDwfAnalogOutNodeFunctionSet.call_args_list[0][0][3].value == dwfconstants.funcDC.value

    mock_dll.FDwfAnalogOutNodeOffsetSet.assert_called_once()
    mock_dll.FDwfAnalogOutNodeOffsetSet.call_args_list[0][0][0] == mock_device
    mock_dll.FDwfAnalogOutNodeOffsetSet.call_args_list[0][0][1].value == channel
    mock_dll.FDwfAnalogOutNodeOffsetSet.call_args_list[0][0][2].value == ac
    pytest.approx(voltage, mock_dll.FDwfAnalogOutNodeOffsetSet.call_args_list[0][0][3].value)

    mock_dll.FDwfAnalogOutConfigure.assert_called_once()
    mock_dll.FDwfAnalogOutConfigure.call_args_list[0][0][0] == mock_device
    mock_dll.FDwfAnalogOutConfigure.call_args_list[0][0][1].value == channel
    mock_dll.FDwfAnalogOutConfigure.call_args_list[0][0][2].value == 1
