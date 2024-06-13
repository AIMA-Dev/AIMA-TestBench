import picoS2000aRealtimeStreaming as pico
from PySide6 import QtWidgets
from PySide6.QtCore import QTimer
import pyqtgraph as pg

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
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(25)  # Frequency in ms

    def update_plot(self):
        """
        Update the plot with new data.

        This method fetches data from the specified channels and updates the plot with the new values.
        It appends the fetched values to the existing data and sets the curves to display the updated data.

        Raises:
            Exception: If there is an error fetching the data.

        """
        try:
            values = [pico.get_value(channel) for channel in self.channels]
            for i, value in enumerate(values):
                self.data[i].append(value)
                self.curves[i].setData(self.data[i])
        except Exception as e:
            print(f"Error fetching data: {e}")
            self.timer.stop()
