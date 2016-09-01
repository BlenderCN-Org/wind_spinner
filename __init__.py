#TODO: Fix this so it reloads script1 when it is reloaded

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

# To support reload properly, try to access a package var, 
# if it's there, reload everything
if "bpy" in locals():
    import imp
    imp.reload(script1)
    #print("Reloaded multifiles")
else:
    from . import script1
    #print("Imported multifiles")

import bpy
import math
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, BoolProperty, StringProperty, IntProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

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
        row.prop(context.scene, 'hub_thickness')
        row = layout.row()
        row.prop(context.scene, 'spinner_radius')
        row = layout.row()
        row.prop(context.scene, 'spinner_hub_radius')
        row = layout.row()
        row.prop(context.scene, 'spinner_start_angle')
        row = layout.row()
        row.prop(context.scene, 'spinner_number')
        row = layout.row()
        row.prop(context.scene, 'spoke_offset')
        row = layout.row()
        row.prop(context.scene, 'spoke_len')
        row = layout.row()
        row.prop(context.scene, 'spoke_number')
        row = layout.row()
        row.prop(context.scene, 'spoke_start_angle')
        row = layout.row()
        row.prop(context.scene, 'linkage_male_len')
        row = layout.row()
        row.prop(context.scene, 'linkage_female_len')
        row = layout.row()
        row.prop(context.scene, 'linkage_incidence')
        row = layout.row()
        row.prop(context.scene, 'linkage_offset')
        row = layout.row()
        row.prop_search(context.scene, 'vane_1', context.scene, "objects")

        TheCol = self.layout.column(align=True)
        TheCol.operator("mesh.add_wind_spinner", text="Add Wind Spinner")

def add_object(self, context):
    from . import script1

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
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(AddWindSpinner)
    #bpy.utils.register_class(WindSpinnerMakerPanel)
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
    bpy.types.Scene.hub_thickness = FloatProperty(
        name='hub thickness',
        default=0.0015,
        subtype="DISTANCE",
        unit='LENGTH',
        description='Spinner hub thickness')
    bpy.types.Scene.spinner_radius = FloatProperty(
        name='spinner radius',
        default=0.25,
        subtype="DISTANCE",
        unit='LENGTH',
        description='Radius of a spinner')
    bpy.types.Scene.spinner_hub_radius = FloatProperty(
        name='spinner hub radius',
        default=0.04,
        subtype="DISTANCE",
        unit='LENGTH',
        description='Radius of a spinner hub')
    bpy.types.Scene.spinner_number = IntProperty(
        name='spinner number',
        default=12,
        description='Number of spinners')
    bpy.types.Scene.spinner_start_angle = FloatProperty(
        name='spinner start angle',
        default=0.0,
        subtype="ANGLE",
        unit='ROTATION',
        description='starting angle for first spinner')
    #TODO: Need spoke_offset?
    bpy.types.Scene.spoke_offset = FloatProperty(
        name='spoke offset',
        default=0.04,
        subtype="DISTANCE",
        unit='LENGTH',
        description='spoke offset from hub center')
    bpy.types.Scene.spoke_len = FloatProperty(
        name='spoke length',
        default=0.23,
        subtype="DISTANCE",
        unit='LENGTH',
        description='length of a spoke')
    bpy.types.Scene.spoke_number = IntProperty(
        name='spoke number',
        default=2,
        description='Number of spokes per spinner')
    bpy.types.Scene.spoke_start_angle = FloatProperty(
        name='spoke start angle',
        default=0.0,
        subtype="ANGLE",
        unit='ROTATION',
        description='starting angle for first spoke on spinner')
    bpy.types.Scene.linkage_male_len = FloatProperty(
        name='male linkage length',
        default=0.12,
        subtype="DISTANCE",
        unit='LENGTH',
        description='length of male linkage')
    bpy.types.Scene.linkage_female_len = FloatProperty(
        name='female linkage length',
        default=0.12,
        subtype="DISTANCE",
        unit='LENGTH',
        description='length of female linkage')
    bpy.types.Scene.linkage_incidence = FloatProperty(
        name='linkage_incidence',
        default=math.pi/3,
        subtype="ANGLE",
        unit='ROTATION',
        description='hub incidence angle for linkage')
    bpy.types.Scene.linkage_offset = FloatProperty(
        name='linkage offset',
        default=0.02,
        subtype="DISTANCE",
        unit='LENGTH',
        description='linkage offset from hub center')
    bpy.types.Scene.vane_1 = StringProperty(
        name='vane 1'
        )

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.utils.unregister_class(AddWindSpinner)
    bpy.utils.unregister_class(WindSpinnerMakerPanel)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)
    del bpy.types.Scene.controller_radius
    del bpy.types.Scene.rim_radius
    del bpy.types.Scene.rim_minor_radius
    #TODO: Complete

if __name__ == "__main__":  
    register()  