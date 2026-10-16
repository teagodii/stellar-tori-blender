# SPDX-License-Identifier: GPL-3.0-or-later
"""Stellar Tori: generate the 45 Stellar Tori and their 63 configurations as meshes.

Adds Add > Mesh > Stellar Tori: pick a configuration from the Vt / Wt / Mt
grid and adjust it in the redo panel. The figure keeps its settings, so the
"Stellar Tori" tab in the sidebar (N) can change them at any time; Detach
turns it into plain objects.
"""

import bpy

from . import live, operators, ui


def register():
    live.register()
    for cls in operators.CLASSES:
        bpy.utils.register_class(cls)
    ui.register()


def unregister():
    ui.unregister()
    for cls in reversed(operators.CLASSES):
        bpy.utils.unregister_class(cls)
    live.unregister()
