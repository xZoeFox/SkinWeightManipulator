import maya.cmds as cmds
import maya.mel as mel
import loadSkinWeights

class LoadSkin():
    def __init__(self):
        self.extraData = None
        self.skinCluster = None
        self.joints = []
        self.jointsMasterList = ["faceJoints_tempRoot", "face_C_faceRoot", "face_C_skull", "face_C_forehead", "face_L_foreheadIn", "face_L_foreheadIn_01", "face_L_foreheadIn_02", "face_L_foreheadIn_03", "face_L_foreheadIn_04", "face_L_foreheadIn_05", "face_R_foreheadIn", "face_R_foreheadIn_01", "face_R_foreheadIn_02", "face_R_foreheadIn_03", "face_R_foreheadIn_04", "face_R_foreheadIn_05", "face_L_foreheadMid", "face_L_foreheadMid_01", "face_L_foreheadMid_02", "face_R_foreheadMid", "face_R_foreheadMid_01", "face_R_foreheadMid_02", "face_L_foreheadOut", "face_L_foreheadOut_01", "face_L_foreheadOut_02", "face_R_foreheadOut", "face_R_foreheadOut_01", "face_R_foreheadOut_02", "face_L_eyesackUpper", "face_L_eyesackUpper_01", "face_L_eyesackUpper_02", "face_R_eyesackUpper", "face_R_eyesackUpper_01", "face_R_eyesackUpper_02", "face_L_eyelidUpperFurrow", "face_L_eyelidUpperFurrow_01", "face_L_eyelidUpperFurrow_02", "face_R_eyelidUpperFurrow", "face_R_eyelidUpperFurrow_01", "face_R_eyelidUpperFurrow_02", "face_L_eyelidUpper", "face_L_eyelidUpper_01", "face_L_eyelidUpper_02", "face_R_eyelidUpper", "face_R_eyelidUpper_01", "face_R_eyelidUpper_02", "face_L_eyeball", "face_R_eyeball", "face_L_eyelidLower", "face_L_eyelidLower_01", "face_L_eyelidLower_02", "face_R_eyelidLower", "face_R_eyelidLower_01", "face_R_eyelidLower_02", "face_L_eyeCornerOuter", "face_R_eyeCornerOuter", "face_L_eyeCornerInner", "face_R_eyeCornerInner", "face_L_eyesackLower", "face_L_eyesackLower_01", "face_L_eyesackLower_02", "face_R_eyesackLower", "face_R_eyesackLower_01", "face_R_eyesackLower_02", "face_L_cheekOuter04", "face_R_cheekOuter04", "face_L_cheekInner", "face_R_cheekInner", "face_L_cheekOuter", "face_L_cheekOuter_01", "face_L_cheekOuter_02", "face_L_cheekOuter_03", "face_R_cheekOuter", "face_R_cheekOuter_01", "face_R_cheekOuter_02", "face_R_cheekOuter_03", "face_C_noseBridge", "face_C_noseUpper", "face_L_noseUpper", "face_R_noseUpper", "face_L_nasolabialBulge", "face_L_nasolabialBulge_02", "face_L_nasolabialBulge_01", "face_R_nasolabialBulge", "face_R_nasolabialBulge_02", "face_R_nasolabialBulge_01", "face_L_nasolabialBulge_03", "face_R_nasolabialBulge_03", "face_L_nasolabialBulge_04", "face_R_nasolabialBulge_04", "face_L_nasolabialFurrow", "face_L_nasolabialFurrow_01", "face_L_nasolabialFurrow_02", "face_R_nasolabialFurrow", "face_R_nasolabialFurrow_01", "face_R_nasolabialFurrow_02", "face_L_cheekLower", "face_L_cheekLower_01", "face_L_cheekLower_02", "face_R_cheekLower", "face_R_cheekLower_01", "face_R_cheekLower_02", "face_L_ear", "face_R_ear", "face_C_nose", "face_C_noseLower", "face_C_noseTip", "face_L_nostril", "face_L_nostrilThickness", "face_R_nostril", "face_R_nostrilThickness", "face_C_lipUpperOuter", "face_L_lipUpperOuter", "face_R_lipUpperOuter", "face_L_lipCornerUpperOuter", "face_R_lipCornerUpperOuter", "face_C_teethUpper", "face_C_lipHolderUpper", "face_C_lipUpper", "face_C_upperSticky", "face_C_lipUpper_thickness", "face_L_lipUpper_01", "face_L_upperSticky", "face_L_lipUpper_01_thickness", "face_L_lipUpper_02", "face_L_upperOuterSticky", "face_L_lipUpper_02_thickness", "face_L_lipCorner", "face_L_lipCornerInterior", "face_R_lipCorner", "face_R_lipCornerInterior", "face_R_lipUpper_01", "face_R_upperSticky", "face_R_lipUpper_01_thickness", "face_R_lipUpper_02", "face_R_upperOuterSticky", "face_R_lipUpper_02_thickness", "face_C_jaw", "face_C_chin", "face_L_chinSide", "face_R_chinSide", "face_C_lipLowerOuter", "face_L_lipLowerOuter", "face_R_lipLowerOuter", "face_L_lipCornerLowerOuter", "face_R_lipCornerLowerOuter", "face_L_jawLine_01", "face_R_jawLine_01", "face_C_lipHolderLower", "face_R_lipLower_02", "face_R_lowerOuterSticky", "face_R_lipLower_02_thickness", "face_R_lipLower_01", "face_R_lowerSticky", "face_R_lipLower_01_thickness", "face_C_lipLower", "face_C_lowerSticky", "face_C_lipLower_thickness", "face_L_lipLower_01", "face_L_lowerSticky", "face_L_lipLower_01_thickness", "face_L_lipLower_02", "face_L_lowerOuterSticky", "face_L_lipLower_02_thickness", "face_C_teethLower", "face_C_tongue_01", "face_C_tongue_02", "face_C_tongue_03", "face_C_tongue_04", "face_R_chinSkin_01", "face_R_chinSkin_02", "face_R_chinSkin_03", "face_C_chinSkin_03", "face_C_chinSkin_02", "face_C_chinSkin_01", "face_L_chinSkin_03", "face_L_chinSkin_02", "face_L_chinSkin_01", "face_L_jawLine_02", "face_L_jawRecess", "face_R_jawRecess", "face_L_masseter", "face_R_masseter", "face_C_underChin", "face_L_underChin", "face_R_underChin", "face_L_temple", "face_R_temple", "face_L_forehead_01", "face_L_forehead_02", "face_L_forehead_03", "face_R_forehead_01", "face_R_forehead_02", "face_R_forehead_03", "face_R_jawLine_02", "face_C_neckRoot", "face_C_adamsApple", "face_L_neck_01", "face_R_neck_01", "face_R_neck_02", "face_L_neck_02", "face_L_neck_03", "face_R_neck_03", "face_L_neck_04", "face_R_neck_04"]
        self.maxInfluences = 0
        self.skinMethod = 0

    def applyVertexWeights(self, filePath):
        loadSkinWeights.applyVertexWeights(filePath)

    def applySelectedVertexWeights(self, filePath):
        loadSkinWeights.applyWeightsToSelectedVertices(filePath)

    def loadJoints(self, filePath):
        loadSkinWeights.selectJointsFromFile(filePath)

    def makeSkinCluster(self, joints, mesh):
        cmds.select(cl=True)
        self.skinCluster = cmds.skinCluster(joints, mesh, tsb=True, n="{}_skinClusterGto".format(mesh))[0]
        cmds.skinCluster(self.skinCluster, e=True, nw=0)
        cmds.skinCluster(self.skinCluster, e=True, nw=1)
        cmds.skinCluster(self.skinCluster, e=True, nw=2)
        cmds.skinCluster(self.skinCluster, e=True, nw=1)

    def loadExtraData(self, inputPath):
        self.extraData = self.prepareAndLoadSkinExtraData(inputPath)
        self.joints = self.extraData[2:len(self.extraData)]
        self.maxInfluences = int(self.extraData[0])
        self.skinMethod = int(self.extraData[1])
        print("Joints: ", self.joints)

    def makeNewClusterForMesh(self, mesh):
        self.skinCluster = self.makeNewCluster(mesh, self.joints, self.maxInfluences, self.skinMethod)
        print("Skin cluster created successfully")

    def clearSkin(self, obj):
        skin = None
        history = cmds.listHistory(obj)
        for i in history:
            if "skinCluster" in i:
                skin = i
                break
        self.delete(skin)
        print("Skin cluster removed")

    def setWeightsFromFile(self, filePath): #gateSetSkinWeights
        self.extraData = cmds.gateSetSkinWeights(destination="{}.weights".format(self.skinCluster), source=filePath, extra=False)
        print("Weights set successfully")

    def checkSkinCluster(self, mesh):
        if mel.eval("findRelatedSkinCluster {0}".format(mesh)):
            self.skinCluster = mel.eval("findRelatedSkinCluster {0}".format(mesh))
            print("Skin cluster already exists")
        else:
            self.clearSkin(mesh)
            self.makeNewClusterForMesh(mesh)
            print("Creating skin cluster")

    #------------------------------------------dcc-------------------------------------------------------

    def delete(self, target):
        if type(target) == list:
            cmds.select(*target, r=True)
            cmds.delete(*target)
        elif type(target) == str:
            cmds.select(target, r=True)
            cmds.delete(target)

    def prepareAndLoadSkinExtraData(self, path):
        cmds.select(cl=True)
        dummySphere = cmds.polySphere(n="dummyGeo")[0]
        cmds.select(dummySphere, r=True)
        dummyMixer = cmds.deformer(type="GateSkinMixerCluster", n="TempDummyMixer")[0]
        extraData = cmds.gateSetSkinWeights(
            destination="{0}.skinWeightsInputs[0]".format(dummyMixer, 0),
            source=path,
            extra=True
            )
        cmds.select(cl=True)
        cmds.delete(dummyMixer)
        cmds.delete(dummySphere)
        print("EXTRA DATA: ", extraData)
        return extraData

    def makeNewCluster(self, mesh, joints, maxInfluences, skinMethod):
        cmds.select(cl=True)
        cmds.select(joints[0])
        skinCluster = cmds.skinCluster(joints[0], mesh, tsb=True)[0]

        cmds.skinCluster(skinCluster, e=True, maximumInfluences=int(maxInfluences))
        cmds.skinCluster(skinCluster, e=True, skinMethod=int(skinMethod))
        cmds.skinCluster(skinCluster, e=True, obeyMaxInfluences=True)
        cmds.skinCluster(skinCluster, e=True, nw=0)
        cmds.select(*joints[1:], r=True)
        cmds.skinCluster(skinCluster, e=True, addInfluence=joints[1:], weight=0, tsb=True)

        print(cmds.skinCluster(skinCluster, inf=True, q=True))
        
        return skinCluster