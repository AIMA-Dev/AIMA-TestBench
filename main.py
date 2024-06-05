import datetime
import time
import threading
import sys
import os
import ctypes
import realTimePlotting
from settings import Settings
from PySide6 import QtWidgets, QtCore, QtUiTools, QtGui
from devicesLink import list_all_devices
from logger import log_action, log_values
from picoS2000aRealtimeStreaming import open_pico, get_value


def update_data(plot):
    settings = Settings()
    while plot.running:
        plot.add_datas([get_value('PS2000A_CHANNEL_A'), get_value('PS2000A_CHANNEL_B'), get_value('PS2000A_CHANNEL_C')])
        log_values([datetime.datetime.now().strftime("%H:%M:%S"), get_value('PS2000A_CHANNEL_A'), get_value('PS2000A_CHANNEL_B'), get_value('PS2000A_CHANNEL_C')], int(settings.read_from_settings_file('fileSizeLimit')))
        time.sleep(1)


def plotting(parent, title, num_of_lines, legend_labels):
    plot = realTimePlotting.RealTimePlot(parent, title, num_of_lines, legend_labels)
    data_thread = threading.Thread(target=update_data, args=(plot,))
    data_thread.start()
    layout = QtWidgets.QVBoxLayout()
    listWidget_testBench.setLayout(layout)
    layout.addWidget(plot)


def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui

def init_settings_tab():
    settings = Settings()
    # Log Path
    if not settings.does_setting_exist('logPath'):
        settings.write_to_settings_file('logPath', '/logs/')
    listWidget_logPath = main_window.findChild(QtWidgets.QListWidget, "listWidget_logPath")
    listWidget_logPath.addItem(os.getcwd()+settings.read_from_settings_file('logPath'))
    # Log Frequency
    spinBox_logFrequency = main_window.findChild(QtWidgets.QSpinBox, "spinBox_logFrequency")
    if not settings.does_setting_exist('logFrequency'):
        settings.write_to_settings_file('logFrequency', spinBox_logFrequency.value())
    else:
        spinBox_logFrequency.setValue(int(settings.read_from_settings_file('logFrequency')))
    spinBox_logFrequency.valueChanged.connect(lambda value: settings.write_to_settings_file('logFrequency', value))
    spinBox_logFrequency.valueChanged.connect(lambda: log_action("Log frequency is set to " + str(spinBox_logFrequency.value()) + " seconds"))
    # File Size Limit
    spinBox_fileSizeLimit = main_window.findChild(QtWidgets.QSpinBox, "spinBox_fileSizeLimit")
    if not settings.does_setting_exist('fileSizeLimit'):
        settings.write_to_settings_file('fileSizeLimit', spinBox_fileSizeLimit.value())
    else:
        spinBox_fileSizeLimit.setValue(int(settings.read_from_settings_file('fileSizeLimit')))
    spinBox_fileSizeLimit.valueChanged.connect(lambda value: settings.write_to_settings_file('fileSizeLimit', value))
    spinBox_fileSizeLimit.valueChanged.connect(lambda: log_action("File size limit is set to " + str(spinBox_fileSizeLimit.value()) + " megabytes"))
    # Log On/Off
    pushButton_LogOnOff = main_window.findChild(QtWidgets.QPushButton, "pushButton_LogOnOff")
    if not settings.does_setting_exist('logOnOff'):
        settings.write_to_settings_file('logOnOff', pushButton_LogOnOff.isChecked())
    else:
        pushButton_LogOnOff.setChecked(settings.read_from_settings_file('logOnOff') == 'True')
    pushButton_LogOnOff.setText("On") if settings.read_from_settings_file('logOnOff') == 'True' else pushButton_LogOnOff.setText("Off")
    pushButton_LogOnOff.clicked.connect(lambda: settings.write_to_settings_file('logOnOff', pushButton_LogOnOff.isChecked()))
    pushButton_LogOnOff.clicked.connect(lambda: pushButton_LogOnOff.setText("On") if settings.read_from_settings_file('logOnOff') == 'True' else pushButton_LogOnOff.setText("Off"))
    pushButton_LogOnOff.clicked.connect(lambda: log_action("Logging is turned on" if settings.read_from_settings_file('logOnOff') == 'True' else "Logging is turned off"))
    # Connected devices
    def refresh_ports():
        listWidget_PortList = main_window.findChild(QtWidgets.QListView, "listWidget_PortList")
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
    pushButton_Refresh = main_window.findChild(QtWidgets.QPushButton, "pushButton_Refresh")
    pushButton_Refresh.clicked.connect(refresh_ports)
    pushButton_Refresh.clicked.connect(lambda: log_action("Refreshing connected devices"))


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
    
    # Plotting
    open_pico()
    listWidget_testBench = main_window.findChild(QtWidgets.QWidget, "listWidget_testBench")
    plotting(listWidget_testBench, "Titre", 3, ["Channel A", "Channel B", "Channel C"])
    
    # Settings
    init_settings_tab()   

    main_window.show()
    sys.exit(app.exec())
# Développé avec ❤️ par : www.noasecond.com.