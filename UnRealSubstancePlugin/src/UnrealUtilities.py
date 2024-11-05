from unreal import (
    AssetToolsHelpers, 
    EditorAssetLibrary,
    AssetTools,
    Material,
    MaterialFactoryNew,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSample2D,
    MaterialProperty,
    AssetImportTask,
    FbxImportUI)
# Import necessary Unreal Engine classes and functions

import os
# Import the os module for interacting with the operating system

class UnrealUtility:
    def __init__(self):
        self.substanceRooDir = '/game/Substance'
        self.substanceBaseMatName = 'M_SubstanceBase'
        self.substanceBaseMatPath = self.substanceRooDir + self.substanceBaseMatName
        self.substanceTempFolder = '/game/Substance/temp'
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetalic = "OcclusionRoughnessMetalic"
# Initialize the UnrealUtility class with default paths and names

    def GetAssetTools(self)->AssetTools:
        return AssetToolsHelpers.get_asset_tools()
# Get the AssetTools instance
    
    def ImportFromDir(self, dir):
        for file in os.listdir(dir):
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(dir, file))
# Import all .fbx files from a directory

    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx","")
        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = '/game/' + meshName
        importTask.automated = True
        importTask.save = True
# Set up the asset import task for the mesh

        fbxImportOption = FbxImportUI()
        fbxImportOption.import_mesh = True
        fbxImportOption.import_as_skeletal = False
        fbxImportOption.import_materials = False
        fbxImportOption.static_mesh_import_data.combine_meshes = True
        importTask.options = fbxImportOption
# Configure FBX import options

        self.GetAssetTools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]
# Import the mesh and return the imported object

    def FindOrBuildBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath):
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)
# Check if the base material exists and load it if it does
        
        baseMat = self.GetAssetTools().create_asset(self.substanceBaseMatName, self.substanceRooDir, Material, MaterialFactoryNew())
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB",  MaterialProperty.MP_BASE_COLOR)
# Create the base material and set up the base color texture sample

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)
# Set up the normal texture sample

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalic)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)
# Set up the occlusion, roughness, and metallic texture sample

        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat
# Save the base material and return it