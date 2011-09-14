from PyQt4 import QtGui
from PyQt4 import QtCore
import ui_planet_weight

PLANETS = {
    "sun": 27.94,
    "moon": 0.167,
    "mercury": 0.37,
    "venus": 0.88,
    "mars": 0.38,
    "ceres": 0.0276,
    "jupiter": 2.64,
    "saturn": 1.15,
    "uranus": 1.17,
    "neptune": 1.18,
    "pluto": 0.059
    }

class PlanetWeightCalculator(QtGui.QDialog, 
                             ui_planet_weight.Ui_PlanetWeightDialog):
    def __init__(self, parent=None):
        super(PlanetWeightCalc, self).__init__(parent)
        self.setupUi(self)
        dvl = QtGui.QDoubleValidator(self)
        dvl.setBottom(0.0)
        dvl.setDecimals(1)
        self.weightLineEdit.setValidator(dvl)
        self.updateUi()

    @QtCore.pyqtSignature("QString")
    def on_weightLineEdit_textEdited(self, text):
        self.updateUi()

    @QtCore.pyqtSignature("")
    def on_calcWeightButton_clicked(self):
        self.__weight = float(self.weightLineEdit.text())
        self.__units = self.unitsComboBox.currentText()
        self._writeCalc()

    @QtCore.pyqtSignature("")
    def on_clearButton_clicked(self):
        self.__weight = float("nan")
        self.__units = ""
        self.updateUi()

    @QtCore.pyqtSignature("QString")
    def on_unitsComboBox_currentIndexChanged(self, text):
        if self.weightLineEdit.text().isEmpty():
            return
        else:
            self.__units = text
            self._writeCalc()

    def updateUi(self):
        enable = not self.weightLineEdit.text().isEmpty()
        self.calcWeightButton.setEnabled(enable)

    def _calcWeight(self, factor):
        return self.__weight * factor

    def _writeCalc(self):
        for key in PLANETS:
            value = self._calcWeight(PLANETS[key])
            le = getattr(self, key+"LineEdit")
            le.setText("%.1f %s" % (value, self.__units))
            
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    pwc = PlanetWeightCalc()
    pwc.show()
    app.exec_()
