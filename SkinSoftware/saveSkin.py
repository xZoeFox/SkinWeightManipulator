import saveSkinWeights
import maya.mel as mel

class SaveSkin():
    def __init__(self):
        self.savePath = ""
        self.meshName = ""
        self.fileName = ""

    def saveSkin(self, target, filename, path):
        self.savePath = path
        self.fileName = filename
        self.meshName = target
        cluster = mel.eval("findRelatedSkinCluster {0}".format(self.meshName))
        if cluster != "":
            saveSkinWeights.saveVertexWeightsToFile(r'{}.ma'.format(self.savePath + self.fileName))
            print("Skin saved successfully")
        else:
            print("No skin cluster found")