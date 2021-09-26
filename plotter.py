from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout, QGroupBox, QPushButton, QLineEdit, QMessageBox
import sys
from PySide2.QtGui import  QFont
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

matplotlib.use('Qt5Agg')

        
myapp = QApplication(sys.argv)

class Window(QDialog):
    """
        A class to represent window of qt

        ...

        Attributes
        ----------
        button : QPushButton
            a button to plot the function
        minEntry : QLineEdit
            text box to enter min value
        maxEntry : QLineEdit
            text box to enter max value
        functionEntry : QLineEdit
            text box to enter function expression
        errorMessage : string
            save last error in inputs to warn the user about
        min : string
            minimum limit of plotted function
        max : string
            maximum limit of plotted function
        x : Array<number>
            x-axis values of plotted function
        y : Array<number>
            Y-axis values of plotted function

        Methods
        -------
        plot()
            Plot function when plot button is pressed
        function_layout()
            Create function text box layout
        min_max_layout()
            Create min & max values text boxes layout
        plot_button_layout()
            Create plot button layout
        changeMinValue()
            Update min value when new value written into text box
        assertMinValue()
            Make sure min value is correct to be plotted
        changeMaxValue()
            Update max value when new value written into text box
        assertMaxValue()
            Make sure max value is correct to be plotted
        changeFunctionValue()
            Update y value when new value written into text box
        assertFunctionValue()
            Make sure y value is correct to be plotted
        
        """

    button = QPushButton("PLOT")
    minEntry = QLineEdit()
    maxEntry = QLineEdit()
    functionEntry = QLineEdit()
    errorMessage = ""
    min  = "1"
    max  = "100"
    x = np.linspace(eval(min),eval(max),(eval(max)-eval(min))*100)
    y = "x"

    def __init__(self):

        super().__init__()
        # Style of button and text boxes
        self.minEntry.setStyleSheet("background-color: white; color: black; font: bold 17px; color: darkblack")
        self.maxEntry.setStyleSheet("background-color: white; color: black; font: bold 17px; color: darkblack")
        self.functionEntry.setStyleSheet("background-color: white; color: black; font: bold 17px; color: darkblack")
        
        # Style of window
        self.setWindowTitle("Function Plotter")
        self.setGeometry(300,200,1000,800)
        self.setStyleSheet("background-color: LightBlue")

        # Create function figure
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        # Build window layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.function_layout())
        vbox.addWidget(self.min_max_layout())
        vbox.addWidget(self.plot_button_layout())
        self.setLayout(vbox)

        self.show()

    def plot(self):

        """
            Plot function when plot button is pressed


                Returns
                -------
                Array | Boolean
                    an array of y values to be plotted or false is there is an error
                """
        # Check min,max,function before plotting
        if(self.errorMessage == ""): self.assertMinValue()
        if(self.errorMessage == ""): self.assertMaxValue()
        if(self.errorMessage == ""):self.assertFunctionValue()
        if(self.errorMessage != ""):
            QMessageBox.warning(self,"Error",self.errorMessage)
            self.errorMessage = ""
            return False
        else:
            x = np.linspace(eval(self.min),eval(self.max),(eval(self.max)-eval(self.min))*100)
            y = eval(self.y)
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x,y)
            self.canvas.draw()
            return y


    def function_layout(self):
        """
           Create function text box layout

            Returns
            -------
            QGroupBox
                a groupbox of function text box layout
            """
        groupBox = QGroupBox()
        groupBox.setFont(QFont("Impact", 20))

        hbox =QHBoxLayout()

        self.functionEntry.setPlaceholderText("Enter function of x")
        self.functionEntry.textChanged.connect(self.changeFunctionValue)
        hbox.addWidget(self.functionEntry)
        
        groupBox.setLayout(hbox)

        return groupBox

    def min_max_layout(self):
        """
           Create min & max values text boxes layout

            Returns
            -------
            QGroupBox
               a groupbox of min,max text boxes layout
            """
        groupBox = QGroupBox()
        groupBox.setFont(QFont("Impact", 20))
 
        hbox =QHBoxLayout()   

        
        self.minEntry.setPlaceholderText("Enter min x value")
        self.minEntry.textChanged.connect(self.changeMinValue)
        hbox.addWidget(self.minEntry)

        self.maxEntry.setPlaceholderText("Enter max x value")
        self.maxEntry.textChanged.connect(self.changeMaxValue)
        hbox.addWidget(self.maxEntry)
        
        groupBox.setLayout(hbox)

        return groupBox

    def plot_button_layout(self):
        """
           Create plot button layout

            Returns
            -------
            QGroupBox
                a groupbox of plot push button layout
            """
        groupBox = QGroupBox()
        groupBox.setFont(QFont("Impact ", 20))
 
        hbox =QHBoxLayout()

        self.button.setStyleSheet("background-color: white; color: black; font: bold 17px; color: darkblack; border-style: inset;")
        self.button.setMinimumHeight(40)
        self.button.clicked.connect(self.plot)
        hbox.addWidget(self.button)

        groupBox.setLayout(hbox)

        return groupBox

    def changeMinValue(self):
        """
            Update min value when new value written into text box

            Returns
            -------
            string
                updated value
            """
        self.min = self.minEntry.displayText() 
        return self.min
    
    def assertMinValue(self):
        """
           Make sure min value is correct to be plotted

            Returns
            -------
            Boolean | string
                True if min value is correct, or a string descriping the problem
            """    
        try:
            int(self.min)
            try:
                assert int(self.min) < int(self.max)
                return True
            except:
                self.errorMessage = "min must be less than max"
                return self.errorMessage
        except:
            self.errorMessage = "Please enter a number for min value"
            return self.errorMessage
            
    def changeMaxValue(self):
        """
         Update max value when new value written into text box

            Returns
            -------
            string
               updated value
            """
        self.max = self.maxEntry.displayText()
        return self.max
    
    def assertMaxValue(self):
        """
           Make sure max value is correct to be plotted

            Returns
            -------
           Boolean | string
                True if max value is correct, or a string descriping the problem
            """
        try:
            int(self.max)
            try:
                assert int(self.max) > int(self.min)
                return True
            except:
                self.errorMessage = "max must be greater than min"
                return False
        except:
            self.errorMessage = "Please enter a number for max value"
            return False

    def changeFunctionValue(self):
        """
           Update y value when new value written into text box

            Returns
            -------
            string
                updated value
            """
        self.y = self.functionEntry.displayText()
        self.y=self.y.replace("^","**")
        return self.y

    def assertFunctionValue(self):
        """
           Make sure y value is correct to be plotted

            Returns
            -------
            Array | boolean
                Array of the evaluated y values, or false if there is a problem in function expression 
            """
        x= self.x
        try:
            eval(self.y)
            return self.y
        except:
            self.errorMessage = "Please enter a valid function of x"
            return False


def main():
    window = Window()
    myapp.exec_()
    sys.exit()
    
if __name__== "__main__" :
    main()
 