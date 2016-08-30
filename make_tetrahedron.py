import math
import bpy
import mathutils

class TetrahedronMakerPanel(bpy.types.Panel) :
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Create"
    bl_label = "Add Tetrahedron"

    def draw(self, context) :
        TheCol = self.layout.column(align = True)
        TheCol.prop(context.scene, "make_tetrahedron_inverted")
        TheCol.operator("mesh.make_tetrahedron", text = "Add Tetrahedron")
    #end draw

#end TetrahedronMakerPanel

class MakeTetrahedron(bpy.types.Operator) :
    bl_idname = "mesh.make_tetrahedron"
    bl_label = "Add Tetrahedron"
    bl_options = {"UNDO"}

    def invoke(self, context, event) :
        Scale = -1 if context.scene.make_tetrahedron_inverted else 1
        Vertices = \
          [
            mathutils.Vector((0, -1 / math.sqrt(3),0)),
            mathutils.Vector((0.5, 1 / (2 * math.sqrt(3)), 0)),
            mathutils.Vector((-0.5, 1 / (2 * math.sqrt(3)), 0)),
            mathutils.Vector((0, 0, Scale * math.sqrt(2 / 3))),
          ]
        NewMesh = bpy.data.meshes.new("Tetrahedron")
        NewMesh.from_pydata \
          (
            Vertices,
            [],
            [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
          )
        NewMesh.update()
        NewObj = bpy.data.objects.new("Tetrahedron", NewMesh)
        context.scene.objects.link(NewObj)
        return {"FINISHED"}
    #end invoke

#end MakeTetrahedron

def register() :
    bpy.utils.register_class(MakeTetrahedron)
    bpy.utils.register_class(TetrahedronMakerPanel)
    bpy.types.Scene.make_tetrahedron_inverted = bpy.props.BoolProperty \
      (
        name = "Upside Down",
        description = "Generate the tetrahedron upside down",
        default = False
      )
#end register

def unregister() :
    bpy.utils.unregister_class(MakeTetrahedron)
    bpy.utils.unregister_class(TetrahedronMakerPanel)
    del bpy.types.Scene.make_tetrahedron_inverted
#end unregister

if __name__ == "__main__" :
    register()
#end if