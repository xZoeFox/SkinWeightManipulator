import maya.cmds as cmds
#import importlib
#import gma.core.app.config
#import gma.core.dcc.maya

import main
import mainUI
import loadSkin
import saveSkin

#importlib.reload(SkinSoftware.main)
#importlib.reload(SkinSoftware.mainUI)
#importlib.reload(SkinSoftware.loadSkin)
#importlib.reload(SkinSoftware.saveSkin)

#cmds.loadPlugin(r"\\g21.thqnordic.net\files\balthazar\software\gatecc\cpp\PropaGate21_2024.mll")
#cmds.loadPlugin(r"\\g21.thqnordic.net\files\balthazar\software\gatecc\cpp\jointsPropaGate2024.mll")
#cmds.loadPlugin(r"\\g21.thqnordic.net\files\balthazar\software\gatecc\cpp\CharacterCustomization2024.mll")
cmds.loadPlugin(r"\\g21.thqnordic.net\files\balthazar\software\AlkimiaMaestroExporter\cpp\PropaGate21_2020.mll")
cmds.loadPlugin(r"\\g21.thqnordic.net\files\balthazar\software\AlkimiaMaestroExporter\cpp\jointsPropaGate2020.mll")
cmds.loadPlugin(r"\\g21.thqnordic.net\files\balthazar\software\AlkimiaMaestroExporter\cpp\CharacterCustomization2020.mll")

#config = gma.core.app.config.Config()
#dcc = gma.core.dcc.maya.Maya()
#dcc.loadMaestroPlugins(config.gmaPluginsPath)
#print("Plugins loaded", config.gmaPluginsPath)

skinSoftware = main.SkinManipulator()

skinSoftware.showUI()

"""
import sys
sys.path.append(r"C:\gtoDevelopment\SkinSoftware")

import runSkinManipulator
reload(runSkinManipulator)
"""