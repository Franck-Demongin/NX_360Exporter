import os
from . import piexif
import bpy


class NX360E_OT_Save360(bpy.types.Operator):
    """Save 360 image and inject required exif"""
    bl_idname = "nx360e.save_360"
    bl_label = "Save 360°"

    make_default = "RICOH"
    model_default = "RICOH THETA S"
    
    filepath: bpy.props.StringProperty(
        name="Filepath",
        default="",
        subtype='FILE_PATH'
    )
    
    make: bpy.props.StringProperty(name="Brand", default="RICOH")
    model: bpy.props.StringProperty(name="Model", default="RICOH THETA S")

    @classmethod
    def poll(cls, context):
        return context.area.type == 'IMAGE_EDITOR'

    def execute(self, context):
        render = context.scene.render
        
        out = os.path.splitext(self.filepath)[0] + '.jpg'

        old_format = render.image_settings.file_format
        render.image_settings.file_format = 'JPEG'

        bpy.ops.image.save_as(filepath=out, save_as_render=True, copy=True)
        
        render.image_settings.file_format = old_format

        zeroth_ifd = {
            piexif.ImageIFD.Make: f"{self.make}",
            piexif.ImageIFD.Model: f"{self.model}"
        }
        exif_dict = {"0th":zeroth_ifd}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, out)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self,context,event):
        return({'FINISHED','PASS_THROUGH'})
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.label(text='EXIF Data')
        col = layout.column(align=True)
        col.prop(self, 'make')
        col = layout.column(align=True)
        col.prop(self, 'model')

        if (
            self.make != self.make_default or 
            self.model != self.model_default
            ):
            col = layout.column(align=True)
            col.operator("wm.operator_defaults", text="Reset to Default")


