from PySide2 import QtCore, QtWidgets
import mainUI
import loadSkin
import saveSkin
import maya.cmds as cmds
import os

class SkinManipulator():
    def __init__(self):
        self.selectedMesh = None
        self.oldMesh = None
        self.indices = []
        self.ui = mainUI.SkinManipulatorUI()
        self.skinLoad = loadSkin.LoadSkin()
        self.skinSave = saveSkin.SaveSkin()
        self.filePath = None
        self.status = None

        self.numOfJoints = 0
        self.maxInfluences = 0
        self.skinMethod = 0

        self.uiEvents()
        self.setMeshSelected()

    def showUI(self):
        self.ui.show()

    def uiEvents(self):
        self.ui.loadSkinTriggered.connect(self.loadSkin)
        self.ui.partialSkinLoadTriggered.connect(self.partialLoad)
        self.ui.saveSkinTriggered.connect(self.saveSkin)
        self.ui.jointsSelected.connect(self.selectJoints)
        #self.ui.createSkinClusterTriggered.connect(self.createSkinCluster)

    def setMeshSelected(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.selectMesh)
        self.timer.setInterval(500)
        self.timer.start()

    def selectMesh(self):
        try:
            selectedObjects = cmds.ls(selection=True)
            self.selectedMesh = str(selectedObjects[0])
            if selectedObjects:
                if self.selectedMesh != self.oldMesh and self.selectedMesh != None:
                    self.oldMesh = self.selectedMesh
                    self.ui.setMeshSelected(self.selectedMesh)
                    self.getSkinClusterData()
                    self.setLabelValues(self.numOfJoints, self.maxInfluences, self.skinMethod)
            else:
                self.selectedMesh = None
                self.ui.setMeshSelected("None")
        except:
            pass

    def getSkinClusterData(self):
        skinCluster = cmds.ls(cmds.listHistory(self.selectedMesh), type='skinCluster')[0]
        self.skinMethod = cmds.getAttr("{}.normalizeWeights".format(skinCluster))
        self.maxInfluences = cmds.getAttr("{}.maxInfluences".format(skinCluster))
        influencingJoints = cmds.skinCluster(skinCluster, query=True, influence=True)
        self.numOfJoints = len(influencingJoints)

    def selectJoints(self):
        self.filePath, self.status = self.openLoadDialog()
        print("Loading joints from {}".format(self.filePath))
        if self.filePath:
            self.skinLoad.loadJoints(self.filePath)

    def saveSkin(self):
        saveInfo, status = self.openSaveDialog()
        fileName = saveInfo[0]
        filePath = saveInfo[1]
        if self.checkIfPathExists(filePath) and self.selectedMesh:
            print("Saving skin for {} at {}{}.ma".format(self.selectedMesh, filePath, fileName))
            self.skinSave.saveSkin(self.selectedMesh, fileName, filePath)

        cmds.select(cl=True)
        cmds.select(self.selectedMesh)

    def checkIfPathExists(self, path):
        if len(path) > 0:
            return True
        else:
            return False

    def loadData(self):
        self.filePath, self.status = self.openLoadDialog()
        if self.checkIfPathExists(self.filePath):
            print("Loading data from: ", self.filePath)
            self.skinLoad.loadExtraData(self.filePath)
        return self.checkIfPathExists(self.filePath)

    def setLabelValues(self, joints, maxInfluences, method):
        self.ui.setLabelValues(joints, maxInfluences, method)

    def loadSkin(self):
        self.filePath, self.status = self.openLoadDialog()
        print("Loading skin for {} from {}".format(self.selectedMesh, self.filePath))
        if self.filePath:
            self.skinLoad.applyVertexWeights(self.filePath)
            self.getSkinClusterData()
            self.setLabelValues(self.numOfJoints, self.maxInfluences, self.skinMethod)
            print("Skin loaded successfully")

        cmds.select(cl=True)
        cmds.select(self.selectedMesh)

    def createSkinCluster(self):
        if self.loadData():
            self.skinLoad.clearSkin(self.selectedMesh)
            self.skinLoad.makeNewClusterForMesh(self.selectedMesh)
            self.setLabelValues()

        cmds.select(cl=True)
        cmds.select(self.selectedMesh)

    def partialLoad(self):
        self.filePath, self.status = self.openLoadDialog()
        print("Loading skin for {} from {}".format(self.selectedMesh, self.filePath))
        if self.filePath:
            self.skinLoad.applySelectedVertexWeights(self.filePath)
            self.getSkinClusterData()
            self.setLabelValues(self.numOfJoints, self.maxInfluences, self.skinMethod)
  
    def openSaveDialog(self):
        current_directory = os.path.join(os.getcwd(), "skins")  
        filename, status = QtWidgets.QFileDialog.getSaveFileName(
            parent=None,
            caption="Save File",
            directory=current_directory,  
            filter="All Files (*.*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )

        fileName = filename.split("/")[-1]
        filePath = filename.replace(fileName, "")

        return [fileName, filePath], status

    def openLoadDialog(self):
        current_directory = os.path.join(os.getcwd(), "skins")  
        filename, status = QtWidgets.QFileDialog.getOpenFileName(
            parent=None,
            caption="Open File",
            directory=current_directory, 
            filter="All Files (*.*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog
        )

        return filename, status


