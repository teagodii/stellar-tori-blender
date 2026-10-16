# SPDX-License-Identifier: GPL-3.0-or-later
"""Stellar Tori: generate the 45 Stellar Tori and their 63 configurations as meshes.

Adds Add > Mesh > Stellar Tori: pick a configuration from the Vt / Wt / Mt
grid and adjust it in the redo panel.
"""

import bpy

from . import operators, ui


def register():
    for cls in operators.CLASSES:
        bpy.utils.register_class(cls)
    ui.register()


def unregister():
    ui.unregister()
    for cls in reversed(operators.CLASSES):
        bpy.utils.unregister_class(cls)
