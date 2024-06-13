import datetime
import time
import threading
import sys
import os
import ctypes
from plotting import PicoPlotter
import picoS2000aRealtimeStreaming as pico
from settings import Settings
from PySide6 import QtWidgets, QtCore, QtUiTools, QtGui
from devicesLink import list_all_devices
from logger import log_action, log_values


def loadUiWidget(uifilename, parent=None):
    """
    Load a UI file and return the corresponding widget.

    Parameters:
    - uifilename (str): The path to the UI file.
    - parent (QWidget): The parent widget (default: None).

    Returns:
    - QWidget: The loaded widget.

    """
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui


def init_settings_tab():
    """
    Initializes the settings tab by setting up various UI elements and their corresponding actions.

    This function performs the following tasks:
    - Sets the log path and displays it in the list widget.
    - Sets the log frequency and connects it to the settings file.
    - Sets the file size limit and connects it to the settings file.
    - Sets the log on/off button and connects it to the settings file.
    - Refreshes the list of connected devices and displays them in the list widget.

    Parameters:
    None

    Returns:
    None
    """
    settings = Settings()
    # Log Path
    if not settings.does_setting_exist('logPath'):
        settings.write_to_settings_file('logPath', '/logs/')
    listWidget_logPath = main_window.findChild(
        QtWidgets.QListWidget, "listWidget_logPath")
    listWidget_logPath.addItem(
        os.getcwd()+settings.read_from_settings_file('logPath'))
    # Log Frequency
    doubleSpinBox_logFrequency = main_window.findChild(
        QtWidgets.QDoubleSpinBox, "spinBox_logFrequency")
    if not settings.does_setting_exist('logFrequency'):
        settings.write_to_settings_file(
            'logFrequency', doubleSpinBox_logFrequency.value())
    else:
        doubleSpinBox_logFrequency.setValue(
            float(settings.read_from_settings_file('logFrequency')))
    doubleSpinBox_logFrequency.valueChanged.connect(
        lambda value: settings.write_to_settings_file('logFrequency', value))
    doubleSpinBox_logFrequency.valueChanged.connect(lambda: log_action(
        "Log frequency is set to " + str(doubleSpinBox_logFrequency.value()) + " seconds"))
    # File Size Limit
    spinBox_fileSizeLimit = main_window.findChild(
        QtWidgets.QSpinBox, "spinBox_fileSizeLimit")
    if not settings.does_setting_exist('fileSizeLimit'):
        settings.write_to_settings_file(
            'fileSizeLimit', spinBox_fileSizeLimit.value())
    else:
        spinBox_fileSizeLimit.setValue(
            int(settings.read_from_settings_file('fileSizeLimit')))
    spinBox_fileSizeLimit.valueChanged.connect(
        lambda value: settings.write_to_settings_file('fileSizeLimit', value))
    spinBox_fileSizeLimit.valueChanged.connect(lambda: log_action(
        "File size limit is set to " + str(spinBox_fileSizeLimit.value()) + " megabytes"))
    # Log On/Off
    pushButton_LogOnOff = main_window.findChild(
        QtWidgets.QPushButton, "pushButton_LogOnOff")
    if not settings.does_setting_exist('logOnOff'):
        settings.write_to_settings_file(
            'logOnOff', pushButton_LogOnOff.isChecked())
    else:
        pushButton_LogOnOff.setChecked(
            settings.read_from_settings_file('logOnOff') == 'True')
    pushButton_LogOnOff.setText("On") if settings.read_from_settings_file(
        'logOnOff') == 'True' else pushButton_LogOnOff.setText("Off")
    pushButton_LogOnOff.clicked.connect(lambda: settings.write_to_settings_file(
        'logOnOff', pushButton_LogOnOff.isChecked()))
    pushButton_LogOnOff.clicked.connect(lambda: pushButton_LogOnOff.setText(
        "On") if settings.read_from_settings_file('logOnOff') == 'True' else pushButton_LogOnOff.setText("Off"))
    pushButton_LogOnOff.clicked.connect(lambda: log_action(
        "Logging is turned on" if settings.read_from_settings_file('logOnOff') == 'True' else "Logging is turned off"))
    # Connected devices

    def refresh_ports():
        """
        Refreshes the list of ports in the UI.

        This function clears the existing list of ports in the UI, retrieves the updated list of ports,
        and populates the UI with the new list of ports. If no ports are detected, it displays a message
        indicating that no device is detected.

        Args:
            None

        Returns:
            None
        """
        listWidget_PortList = main_window.findChild(
            QtWidgets.QListView, "listWidget_PortList")
        listWidget_PortList.clear()
        item = QtWidgets.QListWidgetItem("Refreshing...")
        listWidget_PortList.addItem(item)
        ports = list_all_devices()
        if not ports:
            listWidget_PortList.clear()
            item = QtWidgets.QListWidgetItem("No device detected")
            listWidget_PortList.addItem(item)
        else:
            listWidget_PortList.clear()
            for port in ports:
                item = QtWidgets.QListWidgetItem(port)
                listWidget_PortList.addItem(item)
    refresh_ports()
    pushButton_Refresh = main_window.findChild(
        QtWidgets.QPushButton, "pushButton_Refresh")
    pushButton_Refresh.clicked.connect(refresh_ports)
    pushButton_Refresh.clicked.connect(
        lambda: log_action("Refreshing connected devices"))


if __name__ == '__main__':
    # Init app
    if os.name == 'nt':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            'aima.testbench')
    app = QtWidgets.QApplication([])
    main_window = loadUiWidget("GUI.ui")
    main_window.setWindowTitle("AIMA - Test Bench")
    main_window.showFullScreen()
    main_window.showMaximized()
    app_icon = QtGui.QIcon("assets/icon.ico")
    app.setWindowIcon(app_icon)
    tabWidget = main_window.findChild(QtWidgets.QTabWidget, "tabWidget")
    tabWidget.setCurrentIndex(0)

    # Log
    log_action("Application started")

    # Settings
    init_settings_tab()
    
    # Plotting
    try:
        pico.open_pico()
        listWidget_testBench = main_window.findChild(QtWidgets.QWidget, "listWidget_testBench")
        channels = ['PS2000A_CHANNEL_A', 'PS2000A_CHANNEL_B', 'PS2000A_CHANNEL_C']
        plotter = PicoPlotter(channels, "PicoScope", listWidget_testBench)
        
    except Exception as e:
        print("Error : "+str(e))
        
    main_window.show()
    sys.exit(app.exec())
# Développé avec ❤️ par : www.noasecond.com.