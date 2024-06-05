from picoS2000aRealtimeStreaming import get_pico_list


def list_all_devices():
    """
    Returns a list of all available devices.

    This function retrieves a list of devices by calling three different functions:
    - get_pico_list(): Retrieves a list of devices using Pico communication.

    The devices from all three functions are combined into a single list and returned.

    Returns:
        devices (list): A list of all available devices.
    """
    devices = []
    devices += get_pico_list()

    return devices
# Développé avec ❤️ par : www.noasecond.com.