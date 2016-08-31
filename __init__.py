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
from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty, StringProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from . import script1

class WindSpinnerMakerPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Create"
    bl_label = "Add Wind Spinner"

    def draw(self, context):
        layout = self.layout
        #layout.label(text="Some stuff:")
        row = layout.row()
        row.prop(context.scene, 'controller_radius')
        row = layout.row()
        row.prop(context.scene, 'rim_radius')
        row = layout.row()
        row.prop(context.scene, 'rim_minor_radius')
        row = layout.row()
        row.prop_search(context.scene, 'vane_1', context.scene, "objects")

        TheCol = self.layout.column(align=True)
        TheCol.operator("mesh.add_wind_spinner", text="Add Wind Spinner")

def add_object(self, context):
    rim = script1.add_rim()
    spinners = script1.add_spinners(rim)
    return
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
    bl_options = {'UNDO'}

    scale = FloatVectorProperty(
            name="scale",
            default=(1.0, 1.0, 1.0),
            subtype='TRANSLATION',
            description="scaling",
            )

    def invoke(self, context, event):
        add_object(self, context)
        return {"FINISHED"}

    ##### POLL #####
    @classmethod
    def poll(cls, context):
        return context.scene != None

# Registration

def add_object_button(self, context):
    self.layout.operator(
        AddWindSpinner.bl_idname,
        text=AddWindSpinner.__doc__,
        icon='PLUGIN')

def register():  
    bpy.utils.register_class(AddWindSpinner)
    bpy.utils.register_class(WindSpinnerMakerPanel)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)

    # Properties
    bpy.types.Scene.controller_radius = FloatProperty(
        name='controller radius',
        default=0.10,
        subtype="DISTANCE",
        unit='LENGTH',
        description='Radius of the spinner rotation controller')
    bpy.types.Scene.rim_radius =  FloatProperty(
        name='rim radius',
        default=0.25,
        subtype="DISTANCE",
        unit='LENGTH',
        description='Radius of the spinner rim')
    bpy.types.Scene.rim_minor_radius = FloatProperty(
        name='rim minor radius',
        default=0.005,
        subtype="DISTANCE",
        unit='LENGTH',
        description='Radius of the rim ring')
    bpy.types.Scene.vane_1 = StringProperty(
        name='vane 1'
        )


def unregister():
    bpy.utils.unregister_class(AddWindSpinner)
    bpy.utils.unregister_class(WindSpinnerMakerPanel)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)
    del bpy.types.Scene.controller_radius
    del bpy.types.Scene.rim_radius
    del bpy.types.Scene.rim_minor_radius

if __name__ == "__main__":  
    register()  