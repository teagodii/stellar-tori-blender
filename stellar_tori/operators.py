# SPDX-License-Identifier: GPL-3.0-or-later
"""The "Add Stellar Tori" operator: build.Params as properties, with a redo panel."""

import struct

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty

from . import build
from . import geometry
from . import transforms_data as td

NONE = "NONE"  # enum stand-in for an empty column


def _layer_items(options, family):
    items = [(NONE, "None", f"No {family} layer")]
    for option in options:
        count = option[:-2]
        items.append((option, f"{count}-{family}", f"{len(td.LAYERS[option])} tori"))
    return items


def _f32(x):
    return struct.unpack("f", struct.pack("f", x))[0]


def _exact(value, default):
    """Undo float32 storage for defaults: Blender keeps 0.7 as 0.69999998..., so map it back."""
    return default if value == _f32(default) else value


def _distance(name, default, description, soft_max=2.0):
    return FloatProperty(
        name=name, description=description, default=default,
        min=0.0, soft_min=0.0, soft_max=soft_max, step=1, precision=3,
        subtype="DISTANCE", unit="LENGTH",
    )


class MESH_OT_stellar_tori_add(bpy.types.Operator):
    """Add a Stellar Tori configuration: one object per torus at its canonical transform"""

    bl_idname = "mesh.stellar_tori_add"
    bl_label = "Stellar Tori"
    bl_options = {"REGISTER", "UNDO"}

    # --- Configuration: each column takes none or one of its options ---
    vt: EnumProperty(name="Vt", description="Vt layer (origin)",
                     items=_layer_items(td.VT_OPTIONS, "Vt"), default=td.DEFAULT_SELECTION[0])
    wt: EnumProperty(name="Wt", description="Wt layer (inner shell)",
                     items=_layer_items(td.WT_OPTIONS, "Wt"), default=td.DEFAULT_SELECTION[1])
    mt: EnumProperty(name="Mt", description="Mt layer (outer shell)",
                     items=_layer_items(td.MT_OPTIONS, "Mt"), default=td.DEFAULT_SELECTION[2])

    # --- Geometry ---
    geometry_type: EnumProperty(
        name="Geometry", description="Shape placed at each of the canonical transforms",
        items=(("TORI", "Tori", "A torus at each transform"),
               ("PLANES", "Planes", "A square plane at each transform")),
        default="TORI",
    )
    major_radius: FloatProperty(
        name="Major Radius", description="Radius from the torus centre to the middle of the tube",
        default=geometry.MAJOR_RADIUS, min=0.001, soft_min=0.01, soft_max=2.0, step=1, precision=3,
        subtype="DISTANCE", unit="LENGTH",
    )
    minor_radius: FloatProperty(
        name="Minor Radius", description="Radius of the tube (equal to the major radius: a horn torus)",
        default=geometry.MINOR_RADIUS, min=0.001, soft_min=0.01, soft_max=2.0, step=1, precision=3,
        subtype="DISTANCE", unit="LENGTH",
    )
    major_segments: IntProperty(
        name="Major Segments", description="Segments around the ring",
        default=geometry.MAJOR_SEGMENTS, min=geometry.MIN_SEGMENTS, max=432,
    )
    minor_segments: IntProperty(
        name="Minor Segments", description="Segments around the tube",
        default=geometry.MINOR_SEGMENTS, min=geometry.MIN_SEGMENTS, max=432,
    )
    plane_size: FloatProperty(
        name="Plane Size", description="Half the width of each plane",
        default=geometry.PLANE_SIZE, min=0.001, soft_min=0.01, soft_max=2.0, step=1, precision=3,
        subtype="DISTANCE", unit="LENGTH",
    )
    plane_subdivisions: IntProperty(
        name="Subdivisions", description="Grid cells along each side of a plane",
        default=geometry.PLANE_SUBDIVISIONS, min=1, max=64,
    )

    # --- Positions: the four shell offset constants ---
    wt_axial: _distance("Wt Axial", td.OFFSET_DEFAULTS["WT_AXIAL"], "Inner shell distance along the axes")
    wt_diagonal: _distance("Wt Diagonal", td.OFFSET_DEFAULTS["WT_DIAGONAL"],
                           "Inner shell per-axis offset for the 45° tori (canonical 0.7, not 1/√2)")
    mt_axial: _distance("Mt Axial", td.OFFSET_DEFAULTS["MT_AXIAL"], "Outer shell distance along the axes", 4.0)
    mt_diagonal: _distance("Mt Diagonal", td.OFFSET_DEFAULTS["MT_DIAGONAL"],
                           "Outer shell per-axis offset for the 45° tori (canonical 1.7)", 4.0)

    # --- Output ---
    organize: EnumProperty(
        name="Organize", description="How the tori are laid out in the scene",
        items=(("OBJECTS", "Objects", "One object per torus, all sharing one mesh"),
               ("GROUPED", "Grouped", "One object per torus, in a collection per Vt / Wt / Mt layer"),
               ("JOINED", "Joined", "One mesh object per Vt / Wt / Mt family")),
        default="OBJECTS",
    )
    match_app_view: BoolProperty(
        name="Match Viewer Orientation",
        description="Turn the figure +90° about X so it stands as in the web viewer "
                    "(the viewer's default view becomes Front view)",
        default=True,
    )
    smooth: BoolProperty(name="Smooth Shading", description="Shade tori smooth", default=True)

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def params(self):
        """The properties as build.Params, with float32-stored defaults restored exactly."""
        defaults = build.Params()
        values = {}
        for name in build.Params.__dataclass_fields__:
            value = getattr(self, name)
            if name in ("vt", "wt", "mt"):
                value = None if value == NONE else value
            elif isinstance(value, float):
                value = _exact(value, getattr(defaults, name))
            values[name] = value
        return build.Params(**values)

    def execute(self, context):
        try:
            result = build.build(self.params(), collection=context.collection)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        root = result.root
        root.location = context.scene.cursor.location
        for ob in context.selected_objects:
            ob.select_set(False)
        root.select_set(True)
        context.view_layer.objects.active = root
        return {"FINISHED"}

    def draw(self, _context):
        layout = self.layout

        layout.label(text="Configuration")
        grid = layout.row(align=False)
        for name, label in (("vt", "Vt"), ("wt", "Wt"), ("mt", "Mt")):
            col = grid.column(align=True)
            col.label(text=label)
            col.prop(self, name, expand=True)

        layout.separator()
        col = layout.column(align=True)
        col.prop(self, "geometry_type", expand=True)
        col = layout.column(align=True)
        if self.geometry_type == "TORI":
            col.prop(self, "major_radius")
            col.prop(self, "minor_radius")
            col.prop(self, "major_segments")
            col.prop(self, "minor_segments")
        else:
            col.prop(self, "plane_size")
            col.prop(self, "plane_subdivisions")

        layout.separator()
        layout.label(text="Shell Offsets")
        col = layout.column(align=True)
        for name in ("wt_axial", "wt_diagonal", "mt_axial", "mt_diagonal"):
            col.prop(self, name)

        layout.separator()
        layout.prop(self, "organize")
        layout.prop(self, "match_app_view")
        if self.geometry_type == "TORI":
            layout.prop(self, "smooth")


CLASSES = (MESH_OT_stellar_tori_add,)
