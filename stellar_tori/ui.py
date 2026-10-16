# SPDX-License-Identifier: GPL-3.0-or-later
"""UI: Add > Mesh > Stellar Tori, and the "Stellar Tori" tab in the 3D viewport's sidebar (N)."""

import bpy

from . import live
from . import settings
from .operators import MESH_OT_stellar_tori_add, OBJECT_OT_stellar_tori_detach


def menu_func(self, _context):
    self.layout.separator()
    self.layout.operator(MESH_OT_stellar_tori_add.bl_idname, text="Stellar Tori", icon="MESH_TORUS")


class VIEW3D_PT_stellar_tori(bpy.types.Panel):
    """Edit the active figure's stored settings live, or add a new figure"""

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Stellar Tori"
    bl_label = "Stellar Tori"

    def draw(self, context):
        layout = self.layout
        root = live.figure_root(context.active_object)
        if root is None:
            layout.operator(MESH_OT_stellar_tori_add.bl_idname, text="Add Stellar Tori", icon="MESH_TORUS")
            layout.label(text="Select a figure to edit it here")
            return

        layout.label(text=root.name, icon="OUTLINER_OB_EMPTY")
        col = layout.column()
        col.enabled = context.mode == "OBJECT"
        settings.draw(col, root.stellar_tori)
        layout.separator()
        layout.operator(OBJECT_OT_stellar_tori_detach.bl_idname, icon="UNLINKED")


CLASSES = (VIEW3D_PT_stellar_tori,)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
