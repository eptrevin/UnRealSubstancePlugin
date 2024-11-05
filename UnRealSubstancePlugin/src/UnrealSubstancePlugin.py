from unreal import (ToolMenuContext, ToolMenus,
                    uclass, 
                    ufunction, 
                    ToolMenuEntryScript)
# Import necessary Unreal Engine classes and functions

import os
import sys
import importlib
import tkinter
# Import standard Python libraries

srcPath = os.path.dirname(os.path.abspath(__file__)) # Get the directory path of the current script
if srcPath not in sys.path:
    sys.path.append(srcPath)
# Add the script directory to the system path if not already present

import UnrealUtilities
importlib.reload(UnrealUtilities)
# Import and reload the UnrealUtilities module

@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override = True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindBuildBaseMaterial()
# Define a class for the "Build Base Material" menu entry script

@uclass()
class LoadMeshEntryScript(ToolMenuEntryScript):
    @ufunction(override = True)
    def execute(self, context) -> None:
        window = tkinter.Tk()
        window.withdraw()
        importDir = tkinter.filedialog.askdirectory()
        window.destroy()
        UnrealUtilities.UnrealUtility.ImportFromDir(importDir)
# Define a class for the "Load From Directory" menu entry script

class UnrealSubstancePlugin:
    def __init__(self):
        self.submenuName = "UnrealSubstancePlugin"
        self.submenuLabel = "Unreal Substance Plugin"
        self.CreateMenu()
# Initialize the UnrealSubstancePlugin class and create the menu

    def CreateMenu(self):
        mainMenu = ToolMenus.get().find_menu("LEvelEditor.MainMenu")
# Find the main menu in the Level Editor

        existing = ToolMenus.get().find_menu(F"LevelEditor.MainMenu.{self.submenuName}")
        if existing:

            ToolMenus.get().remove_menu(existing.menu_name)
# Remove existing submenu if it exists

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", self.submenuName, self.submenuLabel)
# Add a new submenu to the main menu

        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadfromDirectory", "Load From Directory", LoadMeshEntryScript())
# Add entry scripts to the submenu

        ToolMenus.get().refresh_all_widgets()
# Refresh all widgets to update the menu

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label)
        script.register_menu_entry()
# Initialize and register a menu entry script


UnrealSubstancePlugin()
# Instantiate the UnrealSubstancePlugin class