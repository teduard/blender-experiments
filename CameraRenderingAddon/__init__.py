"""
Camera Rendering Addon for easy rendering using multiple view points at once
"""

bl_info = {
    "name": "CameraRenderingAddon",
    "author": "teduard",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "location": "3D Viewport > Sidebar > myPanel",
    "description": "My custom panel",
    "category": "Development",
}

import os
import bpy
import math

class CustomCamera:
    def __init__(self, x, y, z, name, filename, radx, rady, radz):
        self._x = x
        self._y = y
        self._z = z
        self._radx = radx
        self._rady = rady
        self._radz = radz
        self._name = name
        self._filepath = "//output/" + filename
    
    def _addCamera(self):
        ### Creating A New Camera Angle
        scn = bpy.context.scene

        # create the second camera
        cam = bpy.data.cameras.new("Camera")
        cam.name = self._name
        cam.lens = 30

        # create the second camera object
        cam_obj = bpy.data.objects.new("Camera", cam)

        cam_obj.name = self._name

        # Locations
        cam_obj.location.x = self._x
        cam_obj.location.y = self._y
        cam_obj.location.z = self._z

        # Rotations
        cam_obj.rotation_euler[0] = math.radians(self._radx)
        cam_obj.rotation_euler[1] = math.radians(self._rady)
        cam_obj.rotation_euler[2] = math.radians(self._radz)

        scn.collection.objects.link(cam_obj)
    
    def _deleteCamera(self):
        if bpy.context.mode == 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[self._name].select_set(True)
        bpy.ops.object.delete()

    def _renderWithCamera(self):
        # Set the Camera to active camera
        bpy.context.scene.camera = bpy.data.objects[self._name]

        # Save Previous Path
        previous_path = bpy.context.scene.render.filepath

        # Render Image
        bpy.context.scene.render.filepath = self._filepath
        bpy.ops.render.render(write_still=True)

        # Restore Previous Path
        bpy.context.scene.render.filepath = previous_path

    def render(self):
        self._addCamera()
        self._renderWithCamera()
        self._deleteCamera()

frontCamera = CustomCamera(0, -10, 1, "myPanelFrontCamera", "01_rendered_with_FrontCamera.png", 90, 0, 0)
backCamera = CustomCamera(0, 10, 1, "myPanelBackCamera", "02_rendered_with_BackCamera.png", 90, 0, 180)
topCamera = CustomCamera(0, 0, 10, "myPanelTopCamera", "03_rendered_with_TopCamera.png", 0, 0, 0)
leftCamera = CustomCamera(-10, 0, 1, "myPanelLeftCamera", "04_rendered_with_LeftCamera.png", 90, 0, -90)
rightCamera = CustomCamera(10, 0, 1, "myPanelRightCamera", "05_rendered_with_RightCamera.png", 90, 0, 90)

class BTN_render_with_Front_camera(bpy.types.Operator):
    bl_idname = "object.render_with_front_camera"
    bl_label = "render with Front camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        frontCamera.render()
        return {"FINISHED"}

class BTN_render_with_Back_camera(bpy.types.Operator):
    bl_idname = "object.render_with_back_camera"
    bl_label = "render with Back camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        backCamera.render()
        return {"FINISHED"}

class BTN_render_with_Top_camera(bpy.types.Operator):
    bl_idname = "object.render_with_top_camera"
    bl_label = "render with Top camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        topCamera.render()
        return {"FINISHED"}

class BTN_render_with_Left_camera(bpy.types.Operator):
    bl_idname = "object.render_with_left_camera"
    bl_label = "render with Left camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        leftCamera.render()
        return {"FINISHED"}

class BTN_render_with_Right_camera(bpy.types.Operator):
    bl_idname = "object.render_with_right_camera"
    bl_label = "render with Right camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        rightCamera.render()
        return {"FINISHED"}

class BTN_render_with_All_camera(bpy.types.Operator):
    bl_idname = "object.render_with_all_camera"
    bl_label = "render with All camera"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        frontCamera.render()
        backCamera.render()
        topCamera.render()
        leftCamera.render()
        rightCamera.render()
        return {"FINISHED"}

class VIEW3D_PT_my_custom_panel(bpy.types.Panel):  
    # where to add the panel in the UI
    bl_space_type = "VIEW_3D"  # 3D Viewport area (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items)
    bl_region_type = "UI"  # Sidebar region (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items)

    # add labels
    bl_category = "mPanel"  # found in the Sidebar
    bl_label = "myPanel"   # found at the top of the Panel

    def draw(self, context):
        """define the layout of the panel"""
        row = self.layout.row()
        row.operator("object.render_with_front_camera", text="Render With Front Camera")
        row = self.layout.row()
        row.operator("object.render_with_back_camera", text="Render With Back Camera")
        row = self.layout.row()
        row.operator("object.render_with_top_camera", text="Render With Top Camera")
        row = self.layout.row()
        row.operator("object.render_with_left_camera", text="Render With Left Camera")
        row = self.layout.row()
        row.operator("object.render_with_right_camera", text="Render With Right Camera")

        self.layout.separator()
        row = self.layout.row()
        row.operator("object.render_with_all_camera", text="Render With All Cameras")
    
# register the panel with Blender
def register():
    bpy.utils.register_class(VIEW3D_PT_my_custom_panel)
    bpy.utils.register_class(BTN_render_with_Front_camera)
    bpy.utils.register_class(BTN_render_with_Back_camera)
    bpy.utils.register_class(BTN_render_with_Top_camera)
    bpy.utils.register_class(BTN_render_with_Left_camera)
    bpy.utils.register_class(BTN_render_with_Right_camera)
    bpy.utils.register_class(BTN_render_with_All_camera)

def unregister():
    bpy.utils.unregister_class(BTN_render_with_Front_camera)
    bpy.utils.unregister_class(BTN_render_with_Back_camera)
    bpy.utils.unregister_class(BTN_render_with_Top_camera)
    bpy.utils.unregister_class(BTN_render_with_Left_camera)
    bpy.utils.unregister_class(BTN_render_with_Right_camera)
    bpy.utils.unregister_class(BTN_render_with_All_camera)
    bpy.utils.unregister_class(VIEW3D_PT_my_custom_panel)

if __name__ == "__main__":
    register()