# SPDX-License-Identifier: GPL-3.0-or-later
"""Menu entry: Add > Mesh > Stellar Tori."""

import bpy

from .operators import MESH_OT_stellar_tori_add


def menu_func(self, _context):
    self.layout.separator()
    self.layout.operator(MESH_OT_stellar_tori_add.bl_idname, text="Stellar Tori", icon="MESH_TORUS")


def register():
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
