# SPDX-License-Identifier: GPL-3.0-or-later
"""Operators: "Add Stellar Tori" (build.Params as properties, with a redo panel) and "Detach"."""

import bpy

from . import build
from . import live
from . import settings


class MESH_OT_stellar_tori_add(bpy.types.Operator):
    """Add a Stellar Tori configuration: one object per torus at its canonical transform"""

    bl_idname = "mesh.stellar_tori_add"
    bl_label = "Stellar Tori"
    bl_options = {"REGISTER", "UNDO"}

    __annotations__ = settings.properties()

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def params(self):
        """The properties as build.Params, with float32-stored defaults restored exactly."""
        return settings.to_params(self)

    def execute(self, context):
        params = self.params()
        try:
            result = build.build(params, collection=context.collection)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        live.adopt(result, params)
        root = result.root
        root.location = context.scene.cursor.location
        for ob in context.selected_objects:
            ob.select_set(False)
        root.select_set(True)
        context.view_layer.objects.active = root
        return {"FINISHED"}

    def draw(self, _context):
        settings.draw(self.layout, self)


class OBJECT_OT_stellar_tori_detach(bpy.types.Operator):
    """Make the active Stellar Tori figure plain objects. Its settings are dropped, so it no longer regenerates"""

    bl_idname = "object.stellar_tori_detach"
    bl_label = "Detach"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and live.figure_root(context.active_object) is not None

    def execute(self, context):
        root = live.figure_root(context.active_object)
        name = root.name
        live.detach(root)
        self.report({"INFO"}, f"Detached {name}")
        return {"FINISHED"}


CLASSES = (MESH_OT_stellar_tori_add, OBJECT_OT_stellar_tori_detach)
