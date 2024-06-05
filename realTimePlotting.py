import time
from PySide6 import QtWidgets
import pyqtgraph as pg
import numpy as np
import threading


class RealTimePlot(QtWidgets.QWidget):
    """
    A class that represents a real-time plot widget.

    Args:
        parent (QWidget): The parent widget.
        title (str): The title of the plot.
        num_of_lines (int): The number of lines to plot.
        legend_labels (list): The legend labels for each line.

    Attributes:
        title (str): The title of the plot.
        num_of_lines (int): The number of lines to plot.
        legend_labels (list): The legend labels for each line.
        data (list): A list of lists to store the data points for each line.
        lock (threading.Lock): A lock to synchronize access to the data.
        running (bool): A flag indicating whether the plot is running.
        thread (threading.Thread): The thread used to update the plot.

    """

    def __init__(self, parent, title, num_of_lines, legend_labels):
        super().__init__(parent)
        self.title = title
        self.num_of_lines = num_of_lines
        self.legend_labels = legend_labels

        self.initUI()

        self.data = [[] for _ in range(num_of_lines)]
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self.update_plot)
        self.thread.start()

    def initUI(self):
        """
        Initializes the user interface of the plot widget.
        """
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.graphWidget = pg.PlotWidget(background='w')
        self.graphWidget.setBackground('w')
        self.graphWidget.getAxis('left').setPen(pg.mkPen(color='k'))
        self.graphWidget.getAxis('bottom').setPen(pg.mkPen(color='k'))

        # Colors list
        colors = [
            (255, 0, 0),    # red
            (0, 255, 0),    # green
            (0, 0, 255),    # blue
            (255, 255, 0),  # yellow
            (255, 0, 255),  # magenta
            (0, 255, 255),  # cyan
            (128, 0, 0),    # maroon
            (128, 128, 0),  # olive
            (0, 128, 0),    # dark green
            (0, 128, 128),  # teal
            (0, 0, 128),    # navy
            (128, 0, 128),  # purple
        ]

        self.lines = []
        for i in range(self.num_of_lines):
            color = colors[i % len(colors)]
            pen = pg.mkPen(color=color, width=3)
            line = self.graphWidget.plot(pen=pen, name=self.legend_labels[i])
            self.lines.append(line)

        self.graphWidget.addLegend()
        layout.addWidget(self.graphWidget)
        
    def add_datas(self, datas):
        """
        Adds new data points to the plot.

        Args:
            datas (list): A list of data points for each line.

        """
        with self.lock:
            if len(datas) != self.num_of_lines:
                print("Number of data points does not match the number of lines")
                return
            for i, data_point in enumerate(datas):
                self.data[i].append(data_point)

    def update_plot(self):
        """
        Updates the plot with the latest data points.
        """
        while self.running:
            with self.lock:
                for i, line in enumerate(self.lines):
                    x_data = np.arange(len(self.data[i]))
                    y_data = np.array(self.data[i])
                    line.setData(x_data, y_data)
            time.sleep(0.01)

    def closeEvent(self, event):
        """
        Handles the close event of the plot widget.

        Args:
            event (QCloseEvent): The close event.

        """
        self.running = False
        self.thread.join()
        event.accept()
# Développé avec ❤️ par : www.noasecond.com.