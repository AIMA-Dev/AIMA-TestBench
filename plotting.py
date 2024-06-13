import picoS2000aRealtimeStreaming as pico
from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Signal
import pyqtgraph as pg

class DataFetcher(QThread):
    data_fetched = Signal(list)

    def __init__(self, channels):
        """
        Initialize the Plotting class.

        Args:
            channels (list): A list of channels.

        Attributes:
            channels (list): A list of channels.
            running (bool): A flag indicating if the plotting is running.
        """
        super().__init__()
        self.channels = channels
        self.running = True

    def run(self):
        """
        Continuously fetches data from the specified channels and emits the fetched data.

        This method runs in a loop until the `running` flag is set to False. It fetches data from each channel
        using the `get_value` method of the `pico` object. The fetched data is then emitted using the `data_fetched`
        signal. After emitting the data, the method sleeps for 25 milliseconds using the `msleep` method.

        If an exception occurs while fetching the data, the error message is printed and the `running` flag is set
        to False, terminating the loop.

        Note: This method assumes that the `channels` attribute is a list of valid channel names.

        """
        while self.running:
            try:
                values = [pico.get_value(channel) for channel in self.channels]
                self.data_fetched.emit(values)
                self.msleep(25)  # Sleep for 25ms
            except Exception as e:
                print(f"Error fetching data: {e}")
                self.running = False

    def stop(self):
        """
        Stops the execution of the program.

        Sets the `running` attribute to False, indicating that the program should stop running.
        """
        self.running = False

class PicoPlotter(QtWidgets.QMainWindow):
    def __init__(self, channels, title, parent):
        """
        Initialize the PlottingWidget.

        Args:
            channels (list): A list of channels.
            title (str): The title of the widget.
            parent (QWidget): The parent widget.

        Returns:
            None
        """
        super().__init__(parent)
        self.channels = channels
        self.title = title
        self.widgetParent = parent
        self.initUI(parent)
        self.data = [[] for _ in channels]

        self.data_fetcher = DataFetcher(channels)
        self.data_fetcher.data_fetched.connect(self.update_plot)
        self.data_fetcher.start()

    def initUI(self, parent):
        """
        Initializes the user interface for the plot.

        Args:
            parent: The parent widget.

        Returns:
            None
        """
        layout = QtWidgets.QVBoxLayout(parent)

        self.plotWidget = pg.PlotWidget(title=self.title, parent=parent)
        layout.addWidget(self.plotWidget)

        self.curves = [self.plotWidget.plot(pen=pg.mkPen(color)) for color in ['r', 'g', 'b', 'y', 'm', 'c']]

    def update_plot(self, values):
        """
        Update the plot with new data.

        Args:
            values (list): The new data values for each channel.

        Returns:
            None
        """
        for i, value in enumerate(values):
            self.data[i].append(value)
            self.curves[i].setData(self.data[i])

    def closeEvent(self, event):
        """
        Handle the close event to stop the data fetching thread.

        Args:
            event: The close event.

        Returns:
            None
        """
        self.data_fetcher.stop()
        self.data_fetcher.wait()
        event.accept()
# Développé avec ❤️ par : www.noasecond.com.