
import ctypes
import unittest.mock as mock

import pytest

import dwfconstants

# Script under test
import set_voltage

@pytest.fixture(scope='module')
def mock_dll():
    return mock.MagicMock()

def test_get_device(mock_dll):
    set_voltage.get_device(mock_dll, "device_id")
    mock_dll.FDwfDeviceOpen.assert_called_once_with("device_id", ctypes.c_int(0))
