import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps
from pico_sdk import PicoDevice
from picosdk.functions import adc2mV, assert_pico_ok
import time

# Global variables to hold the device handle and channel range
chandle = ctypes.c_int16()
channel_range = None
maxADC = ctypes.c_int16()

def close_pico():
    """
    Closes the PicoScope device.

    This function closes the PicoScope device.

    Returns:
        None
    """
    global chandle
    status = ps.ps2000aCloseUnit(chandle)
    assert_pico_ok(status)

def open_pico():
    """
    Opens the PicoScope device and sets up the channels.

    This function opens the PicoScope device, sets up channels A and B, and retrieves the maximum ADC value.

    Returns:
        None
    """
    global chandle, channel_range, maxADC
    status = {}
    status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)
    assert_pico_ok(status["openunit"])
    enabled = 1
    analogue_offset = 0.0
    channel_range = ps.PS2000A_RANGE['PS2000A_2V']

    # Set up channels A and B
    for channel in ['PS2000A_CHANNEL_A', 'PS2000A_CHANNEL_B']:
        status["setChannel"] = ps.ps2000aSetChannel(chandle,
                                                    ps.PS2000A_CHANNEL[channel],
                                                    enabled,
                                                    ps.PS2000A_COUPLING['PS2000A_DC'],
                                                    channel_range,
                                                    analogue_offset)
        assert_pico_ok(status["setChannel"])

    # Get the max ADC value
    status["maximumValue"] = ps.ps2000aMaximumValue(
        chandle, ctypes.byref(maxADC))
    assert_pico_ok(status["maximumValue"])


def get_value(channel):
    """
    Get the voltage value from the specified channel.

    Args:
        channel (int): The channel number.

    Returns:
        float: The voltage value.

    Raises:
        AssertionError: If there is an error in setting the data buffers or running streaming.

    """
    global chandle, channel_range, maxADC
    buffer = np.zeros(shape=1, dtype=np.int16)
    status = {}

    status["setDataBuffers"] = ps.ps2000aSetDataBuffers(chandle,
                                                        ps.PS2000A_CHANNEL[channel],
                                                        buffer.ctypes.data_as(
                                                            ctypes.POINTER(ctypes.c_int16)),
                                                        None,
                                                        1,
                                                        0,
                                                        ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE'])
    assert_pico_ok(status["setDataBuffers"])
    sampleInterval = ctypes.c_int32(250)
    sampleUnits = ps.PS2000A_TIME_UNITS['PS2000A_US']

    status["runStreaming"] = ps.ps2000aRunStreaming(chandle,
                                                    ctypes.byref(
                                                        sampleInterval),
                                                    sampleUnits,
                                                    0,
                                                    1,
                                                    1,
                                                    1,
                                                    ps.PS2000A_RATIO_MODE['PS2000A_RATIO_MODE_NONE'],
                                                    1)
    assert_pico_ok(status["runStreaming"])

    wasCalledBack = False

    def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
        nonlocal wasCalledBack
        wasCalledBack = True

    cFuncPtr = ps.StreamingReadyType(streaming_callback)
    while not wasCalledBack:
        status["getStreamingLastestValues"] = ps.ps2000aGetStreamingLatestValues(
            chandle, cFuncPtr, None)

    voltage = adc2mV(buffer, channel_range, maxADC)
    status["stop"] = ps.ps2000aStop(chandle)
    assert_pico_ok(status["stop"])

    return voltage[0]


def get_pico_list():
    """
    Retrieves a list of PicoScope devices connected to the system.

    Returns:
        list: A list of strings representing the PicoScope devices, each string
        contains the device variant and serial number.
    """
    device_list = []
    found = PicoDevice.enumerate()
    for device in found:
        device_list.append(
            "PicoScope " + device.variant + " with serial " + device.serial)
    return device_list
# Développé avec ❤️ par : www.noasecond.com.