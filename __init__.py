### NOTES
# Look at pingpong example for drawing a button on a panel. Use the button execute() to create the spinner.
# https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Panels_and_Operators/Ping_Pong

bl_info = {
    "name": "New Wind Spinner",
    "author": "Mike Gering",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Wind Spinner",
    "description": "Adds a new Wind Spinner Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def add_object(self, context):
    scene = context.scene
    obj_act = scene.objects.active

    scale_x = self.scale.x
    scale_y = self.scale.y

    verts = [Vector((-1 * scale_x, 1 * scale_y, 0)),
             Vector((1 * scale_x, 1 * scale_y, 0)),
             Vector((1 * scale_x, -1 * scale_y, 0)),
             Vector((-1 * scale_x, -1 * scale_y, 0)),
            ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="New Wind Spinner")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)

class AddWindSpinner(bpy.types.Operator, AddObjectHelper):
    """Add Wind Spinner"""
    bl_idname = 'mesh.add_wind_spinner'
    bl_label = 'Add Wind Spinner'
    bl_options = {'REGISTER', 'UNDO'}

    scale = FloatVectorProperty(
            name="scale",
            default=(1.0, 1.0, 1.0),
            subtype='TRANSLATION',
            description="scaling",
            )

    controller_radius = FloatProperty(
    	name='controller radius',
    	default=0.10,
    	subtype="DISTANCE",
    	unit='LENGTH',
    	description='Radius of the spinner rotation controller')

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene, 'controller_radius')
        row = col.row(align=True)
        row.operator('mesh.add_wind_spinner_execute')

    def execute(self, context):
        add_object(self, context)
        return {"FINISHED"}

    ##### POLL #####
    @classmethod
    def poll(cls, context):
        return context.scene != None

class AddWindSpinnerExecute(bpy.types.Operator):
    """Operator to execute spinner addition"""
    bl_idname = 'mesh.add_wind_spinner_execute'
    bl_label = 'Execute Add Wind Spinner'
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Execute spinner add")
        return {'FINISHED'}

# Registration

def add_object_button(self, context):
    self.layout.operator(
        AddWindSpinner.bl_idname,
        text=AddWindSpinner.__doc__,
        icon='PLUGIN')

def register():  
    bpy.utils.register_class(AddWindSpinner)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)
    bpy.utils.register_class(AddWindSpinnerExecute)
    bpy.types.Scene.controller_radius =  FloatProperty(
        name='controller radius',
        default=0.10,
        subtype="DISTANCE",
        unit='LENGTH',
        description='Radius of the spinner rotation controller')


def unregister():
    bpy.utils.unregister_class(AddWindSpinner)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)
    bpy.utils.unregister_class(AddWindSpinnerExecute)
    del bpy.types.Scene.controller_radius

if __name__ == "__main__":  
    register()  