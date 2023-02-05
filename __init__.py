# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "NX_360Exporter",
    "author" : "Franck Demongin",
    "description" : "Save the render in JPEG and insert EXIF data to create a 360 panorama",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "Image Editor > Image > Save > Save 360",
    "warning" : "",
    "category" : "Import-Export"
}

import bpy
from . nex_op import NX360E_OT_Save360

def draw_item(self, context):
    layout = self.layout

    layout.row().separator()
    layout.operator_context = 'INVOKE_DEFAULT'
    layout.operator('nx360e.save_360')


def register():
    bpy.utils.register_class(NX360E_OT_Save360)
    bpy.types.IMAGE_MT_image.append(draw_item)


def unregister():
    bpy.utils.unregister_class(NX360E_OT_Save360)
    bpy.types.IMAGE_MT_image.remove(draw_item)
