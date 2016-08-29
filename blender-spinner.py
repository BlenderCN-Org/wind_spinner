import bpy

class AddWindSpinner(bpy.types.Operator):
	bl_idname = 'object.add_wind_spinner'
	bl_label = 'Add Wind Spinner'

	def execute(self, context):
		#TODO: Finish
		return {"FINISHED"}

def register():  
    bpy.utils.register_class(AddWindSpinner)  
  
if __name__ == "__main__":  
    register()  