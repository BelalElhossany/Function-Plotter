from plotter import Window
import numpy as np 
from PySide2 import QtCore
import pytest
from pytestqt.qt_compat import qt_api



## Tests using GUI ##
@pytest.fixture
def window(qtbot):        
    window = Window()
    qtbot.addWidget(window)
    return window

def test_change_min_value(qtbot,window):
    qtbot.keyClicks(window.minEntry,"1")

    assert window.min == "1"

def test_change_max_value(qtbot,window):
    qtbot.keyClicks(window.maxEntry,"10")

    assert window.max == "10"

def test_change_function_value(qtbot,window):
    qtbot.keyClicks(window.functionEntry,"x^2+10")

    assert window.y == "x**2+10"

def test_correct_functionality(qtbot,window):
    qtbot.mouseClick(window.button, QtCore.Qt.LeftButton)
    assert window.plot().all() == np.add(np.power(window.x,2), 10).all()

def test_min_less_than_max(qtbot,window):
    qtbot.keyClicks(window.minEntry,"000")
    qtbot.keyClicks(window.maxEntry,"0")
    window.assertMinValue()
    assert window.errorMessage == "min must be less than max" 

def test_max_less_than_min(qtbot,window):
    qtbot.keyClicks(window.maxEntry,"0")
    qtbot.keyClicks(window.minEntry,"0")
    window.assertMaxValue()
    assert window.errorMessage == "max must be greater than min" 

def test_min_value_is_number(qtbot,window):
    qtbot.keyClicks(window.minEntry,"a")
    window.assertMinValue()
    assert window.errorMessage == "Please enter a number for min value"

def test_max_value_is_number(qtbot,window):
    qtbot.keyClicks(window.maxEntry,"a")
    window.assertMaxValue()
    assert window.errorMessage == "Please enter a number for max value"
