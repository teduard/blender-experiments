import bpy
import os
import math

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='SELECT')

bpy.ops.export_scene.gltf(
    filepath=os.path.join(os. getcwd(), "tmp", f'object.gltf'),
    export_format='GLTF_SEPARATE',
    use_selection=True,
)

def setupCamera():
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.resolution_x = 150
    bpy.context.scene.render.resolution_y = 150
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.cycles.samples = 5

def addTopCamera():
    if bpy.context.scene.camera is not None:
        return None

    ### Creating A New Camera Angle
    scn = bpy.context.scene

    # create the second camera
    cam = bpy.data.cameras.new("Camera")
    cam.name = "myPanelTopCamera"
    cam.lens = 30

    # create the second camera object
    cam_obj = bpy.data.objects.new("Camera", cam)

    cam_obj.name = "myPanelTopCamera"

    # Locations
    cam_obj.location.x = 0
    cam_obj.location.y = 0
    cam_obj.location.z = 10

    # Rotations
    cam_obj.rotation_euler[0] = math.radians(0)
    cam_obj.rotation_euler[1] = math.radians(0)
    cam_obj.rotation_euler[2] = math.radians(0)

    scn.collection.objects.link(cam_obj)

def renderWithTopCamera():
    # Set the Camera to active camera
    if bpy.context.scene.camera is None:
        bpy.context.scene.camera = bpy.data.objects["myPanelTopCamera"]

    # Setting the path for the first image captured in the first camera
    FILE_PATH = os.path.join(os. getcwd(), "tmp", 'render.png')

    # Save Previous Path
    previous_path = bpy.context.scene.render.filepath

    # Render Image
    bpy.context.scene.render.filepath = FILE_PATH
    bpy.ops.render.render(write_still=True)

    # Restore Previous Path
    bpy.context.scene.render.filepath = previous_path


def deleteTopCamera():
    if bpy.context.scene.camera is not None:
        return None

    if bpy.context.mode == 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['myPanelTopCamera'].select_set(True)
    bpy.ops.object.delete()


if bpy.context.scene.camera is not None:
    print("camera is\n")
    print(bpy.context.scene.camera)

setupCamera()
addTopCamera()
renderWithTopCamera()
deleteTopCamera()