import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty

class AddWindSpinner(bpy.types.Operator):
    """Add Wind Spinner"""
    bl_idname = 'object.add_wind_spinner'
    bl_label = 'Add Wind Spinner'
    bl_options = {'REGISTER', 'UNDO'}

    controller_radius = FloatProperty(
    	name='controller radius',
    	default=0.10,
    	subtype="DISTANCE",
    	unit='LENGTH',
    	description='Radius of the spinner rotation controller')

    def execute(self, context):
        #TODO: Finish
        print("Do it!")
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
    	return True

def add_object_button(self, context):
    self.layout.operator(
        AddWindSpinner.bl_idname,
        text=AddWindSpinner.__doc__,
        icon='PLUGIN')

def register():  
    bpy.utils.register_class(AddWindSpinner)
    bpy.types.VIEW3D_MT_object.append(add_object_button)
  
if __name__ == "__main__":  
    register()  