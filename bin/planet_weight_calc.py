if __name__ == "__main__":
    import sys
    import pwc
    app = QtGui.QApplication(sys.argv)
    pwcd = pwc.PlanetWeightCalculator()
    pwcd.show()
    app.exec_()