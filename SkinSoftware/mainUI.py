from PySide2 import QtCore, QtWidgets, QtGui

class SkinManipulatorUI(QtWidgets.QMainWindow):
    meshSelected = QtCore.Signal()
    loadSkinTriggered = QtCore.Signal()
    partialSkinLoadTriggered = QtCore.Signal()
    saveSkinTriggered = QtCore.Signal()
    createSkinClusterTriggered = QtCore.Signal()
    jointsSelected = QtCore.Signal()

    def __init__(self, parent=None):
        super(SkinManipulatorUI, self).__init__(parent)
        self.setFixedSize(250, 350)
        self.setWindowTitle("Skin Save/Load")
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.wrapWidget = QtWidgets.QWidget()
        self.wrapWidget.setFixedSize(245, 345)
        self.wrapLayout = QtWidgets.QVBoxLayout()
        self.wrapLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.wrapWidget.setLayout(self.wrapLayout)

        self.selectionLabel = QtWidgets.QLabel("None")
        self.selectionLabel.setObjectName("selectionLabel")
        self.selectionLabel.setFixedSize(245, 30)
        self.selectionLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.buttonsLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.infoLayout = QtWidgets.QHBoxLayout()
        self.infoLayout.setAlignment(QtCore.Qt.AlignLeft)

        self.selectJointsButton = QtWidgets.QPushButton("Select joints")
        self.selectJointsButton.setFixedSize(160, 35)
        self.loadButton = QtWidgets.QPushButton("Load and apply skin")
        self.loadButton.setFixedSize(160, 35)
        self.partialLoadButton = QtWidgets.QPushButton("Apply skin on selected")
        self.partialLoadButton.setFixedSize(160, 35)
        self.saveButton = QtWidgets.QPushButton("Save skin")
        self.saveButton.setFixedSize(160, 35)
        self.createSkinClusterButton = QtWidgets.QPushButton("Create skin cluster")
        self.createSkinClusterButton.setFixedSize(160, 35)
        self.createSkinClusterButton.setHidden(True)

        self.numOfJoints = QtWidgets.QLabel("Joints: 0")
        self.maxInfluences = QtWidgets.QLabel("Influences: 0")
        self.skinMethod = QtWidgets.QLabel("Method: 0")

        self.buttonsLayout.addWidget(self.selectJointsButton)
        self.buttonsLayout.addWidget(self.createSkinClusterButton)
        self.buttonsLayout.addWidget(self.loadButton)
        self.buttonsLayout.addWidget(self.partialLoadButton)
        self.buttonsLayout.addWidget(self.saveButton)

        self.infoLayout.addWidget(self.numOfJoints)
        self.infoLayout.addStretch()
        self.infoLayout.addWidget(self.maxInfluences)
        self.infoLayout.addStretch()
        self.infoLayout.addWidget(self.skinMethod)

        self.wrapLayout.addStretch()
        self.wrapLayout.addWidget(self.selectionLabel)
        self.wrapLayout.addStretch()
        self.wrapLayout.addLayout(self.buttonsLayout)
        self.wrapLayout.addStretch()
        self.wrapLayout.addLayout(self.infoLayout)

        self.setStyleSheet("""
        QPushButton {
            color: white;
            font-size: 14px;
            font-weight: bold;
            background-color: rgba(128, 128, 128, 1);
        }
        QPushButton:hover {
            color: white;
            font-size: 14px;
            font-weight: bold;
            background-color: rgba(128, 128, 128, 0.8);
        }
        QPushButton:disabled {
            color: gray;
            background-color: rgba(128, 128, 128, 0.7);
        }
        QLabel {
            color: white;
            font-size: 12px;
        }
        QLabel#selectionLabel {
            color: white;
            background-color: rgba(40, 40, 40, 1);
            font-size: 14px;
        }
        """)

        self.setCentralWidget(self.wrapWidget)

        self.loadButton.clicked.connect(self.loadSkinEmit)
        self.partialLoadButton.clicked.connect(self.partialLoadEmit)
        self.saveButton.clicked.connect(self.saveSkinEmit)
        self.createSkinClusterButton.clicked.connect(self.createSkinClusterEmit)
        self.selectJointsButton.clicked.connect(self.selectJointsEmit)

        #self.partialLoadButton.setDisabled(True)
        #self.partialLoadButton.setToolTip("Comming soon!")

    def setLabelValues(self, joints, influences, method):
        self.numOfJoints.setText("Joints: {}".format(joints))
        self.maxInfluences.setText("Influences: {}".format(influences))
        self.skinMethod.setText("Method: {}".format(method))

        print("Number of joints: {0}, Max influences: {1}, Skin method: {2}".format(joints, influences, method))

    def selectJointsEmit(self):
        self.jointsSelected.emit()

    def setMeshSelected(self, mesh):
        self.selectionLabel.setText(mesh)

    def loadSkinEmit(self):
        self.loadSkinTriggered.emit()

    def partialLoadEmit(self):
        self.partialSkinLoadTriggered.emit()

    def saveSkinEmit(self):
        self.saveSkinTriggered.emit()

    def createSkinClusterEmit(self):
        self.createSkinClusterTriggered.emit()

