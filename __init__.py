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
print("initing")
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def add_object(self, context):
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

    def execute(self, context):
        add_object(self, context)
        return {"FINISHED"}

# Registration

def add_object_button(self, context):
    self.layout.operator(
        AddWindSpinner.bl_idname,
        text=AddWindSpinner.__doc__,
        icon='PLUGIN')

def register():  
    bpy.utils.register_class(AddWindSpinner)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(AddWindSpinner)
    bpy.types.INFO_MT_mesh_add.remove(add_object_button)

if __name__ == "__main__":  
    register()  