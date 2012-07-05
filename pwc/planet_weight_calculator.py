from PyQt4 import QtGui
from PyQt4 import QtCore
import ui
import info
import version

class PlanetWeightCalculator(QtGui.QDialog, ui.Ui_PlanetWeightDialog):
    def __init__(self, parent=None):
        super(PlanetWeightCalculator, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":/pwc.svg"))
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
            if self.__units != text and self.__units != "":
                check = (self.__units, text)
                if check == ("lbs", "N"):
                    self._convertWeight(info.LBS_TO_NEWTONS)
                elif check == ("N", "lbs"):
                    self._convertWeight(1.0 / info.LBS_TO_NEWTONS)
                elif check == ("lbs", "st"):
                    self._convertWeight(info.LBS_TO_STONES)
                elif check == ("st", "lbs"):
                    self._convertWeight(1.0 / info.LBS_TO_STONES)
                elif check == ("N", "st"):
                    self._convertWeight(info.NEWTONS_TO_STONES)
                else:
                    self._convertWeight(1.0 / info.NEWTONS_TO_STONES)
                self.weightLineEdit.setText("%.1f" % self.__weight)
            self.__units = text
            self._writeCalc()
            
    @QtCore.pyqtSignature("")
    def on_aboutButton_clicked(self):
        QtGui.QMessageBox.about(self, "About Planet Weight Calculator",
                                """
                                <b>Planet Weight Calculator</b> v%s
                                <p>This application calculates your weight
                                on the different Solar System planets and 
                                the sun.
                                """ % version.version)

    def updateUi(self):
        enable = not self.weightLineEdit.text().isEmpty()
        self.calcWeightButton.setEnabled(enable)

    def _calcWeight(self, factor):
        return self.__weight * factor

    def _convertWeight(self, factor):
        self.__weight *= factor

    def _writeCalc(self):
        for key in info.PLANETS:
            value = self._calcWeight(info.PLANETS[key])
            le = getattr(self, key+"LineEdit")
            le.setText("%.1f %s" % (value, self.__units))
            

