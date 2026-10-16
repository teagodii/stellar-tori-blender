# SPDX-License-Identifier: GPL-3.0-or-later
"""build.Params as Blender properties, shared by the operator and the settings stored on a figure.

``properties()`` defines one property per ``Params`` field, so the "Add Stellar
Tori" operator and the live settings on a figure's root (``live.py``) can't
drift apart. ``to_params`` / ``from_params`` convert between the two, and
``draw`` lays them out for the redo panel and the sidebar alike.
"""

import struct

from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty

from . import build
from . import geometry
from . import transforms_data as td

NONE = "NONE"  # enum stand-in for an empty column
LAYER_FIELDS = ("vt", "wt", "mt")


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


def properties(update=None):
    """{field: property} for every build.Params field, in Params order.

    ``update`` is called after any of them changes (the stored settings use it
    to regenerate). None of them is animatable: a keyframe wouldn't regenerate.
    """
    common = {"options": set()}
    if update is not None:
        common["update"] = update

    def distance(name, default, description, soft_max=2.0):
        return FloatProperty(
            name=name, description=description, default=default,
            min=0.0, soft_min=0.0, soft_max=soft_max, step=1, precision=3,
            subtype="DISTANCE", unit="LENGTH", **common,
        )

    def radius(name, default, description):
        return FloatProperty(
            name=name, description=description, default=default,
            min=0.001, soft_min=0.01, soft_max=2.0, step=1, precision=3,
            subtype="DISTANCE", unit="LENGTH", **common,
        )

    return {
        # --- Configuration: each column takes none or one of its options ---
        "vt": EnumProperty(name="Vt", description="Vt layer (origin)",
                           items=_layer_items(td.VT_OPTIONS, "Vt"), default=td.DEFAULT_SELECTION[0], **common),
        "wt": EnumProperty(name="Wt", description="Wt layer (inner shell)",
                           items=_layer_items(td.WT_OPTIONS, "Wt"), default=td.DEFAULT_SELECTION[1], **common),
        "mt": EnumProperty(name="Mt", description="Mt layer (outer shell)",
                           items=_layer_items(td.MT_OPTIONS, "Mt"), default=td.DEFAULT_SELECTION[2], **common),
        # --- Geometry ---
        "geometry_type": EnumProperty(
            name="Geometry", description="Shape placed at each of the canonical transforms",
            items=(("TORI", "Tori", "A torus at each transform"),
                   ("PLANES", "Planes", "A square plane at each transform")),
            default="TORI", **common,
        ),
        "major_radius": radius("Major Radius", geometry.MAJOR_RADIUS,
                               "Radius from the torus centre to the middle of the tube"),
        "minor_radius": radius("Minor Radius", geometry.MINOR_RADIUS,
                               "Radius of the tube (equal to the major radius: a horn torus)"),
        "major_segments": IntProperty(
            name="Major Segments", description="Segments around the ring",
            default=geometry.MAJOR_SEGMENTS, min=geometry.MIN_SEGMENTS, max=432, **common,
        ),
        "minor_segments": IntProperty(
            name="Minor Segments", description="Segments around the tube",
            default=geometry.MINOR_SEGMENTS, min=geometry.MIN_SEGMENTS, max=432, **common,
        ),
        "plane_size": radius("Plane Size", geometry.PLANE_SIZE, "Half the width of each plane"),
        "plane_subdivisions": IntProperty(
            name="Subdivisions", description="Grid cells along each side of a plane",
            default=geometry.PLANE_SUBDIVISIONS, min=1, max=64, **common,
        ),
        # --- Positions: the four shell offset constants ---
        "wt_axial": distance("Wt Axial", td.OFFSET_DEFAULTS["WT_AXIAL"], "Inner shell distance along the axes"),
        "wt_diagonal": distance("Wt Diagonal", td.OFFSET_DEFAULTS["WT_DIAGONAL"],
                                "Inner shell per-axis offset for the 45° tori (canonical 0.7, not 1/√2)"),
        "mt_axial": distance("Mt Axial", td.OFFSET_DEFAULTS["MT_AXIAL"], "Outer shell distance along the axes", 4.0),
        "mt_diagonal": distance("Mt Diagonal", td.OFFSET_DEFAULTS["MT_DIAGONAL"],
                                "Outer shell per-axis offset for the 45° tori (canonical 1.7)", 4.0),
        # --- Output ---
        "match_app_view": BoolProperty(
            name="Match Viewer Orientation",
            description="Turn the figure +90° about X so it stands as in the web viewer "
                        "(the viewer's default view becomes Front view)",
            default=True, **common,
        ),
        "organize": EnumProperty(
            name="Organize", description="How the tori are laid out in the scene",
            items=(("OBJECTS", "Objects", "One object per torus, all sharing one mesh"),
                   ("GROUPED", "Grouped", "One object per torus, in a collection per Vt / Wt / Mt layer"),
                   ("JOINED", "Joined", "One mesh object per Vt / Wt / Mt family")),
            default="OBJECTS", **common,
        ),
        "smooth": BoolProperty(name="Smooth Shading", description="Shade tori smooth", default=True, **common),
    }


def to_params(data):
    """``data``'s properties as build.Params, with float32-stored defaults restored exactly."""
    defaults = build.Params()
    values = {}
    for name in build.Params.__dataclass_fields__:
        value = getattr(data, name)
        if name in LAYER_FIELDS:
            value = None if value == NONE else value
        elif isinstance(value, float):
            value = _exact(value, getattr(defaults, name))
        values[name] = value
    return build.Params(**values)


def from_params(data, params):
    """Write build.Params onto ``data``'s properties."""
    for name in build.Params.__dataclass_fields__:
        value = getattr(params, name)
        if name in LAYER_FIELDS and value is None:
            value = NONE
        setattr(data, name, value)


def draw(layout, data):
    """The settings layout, shared by the redo panel and the sidebar."""
    layout.label(text="Configuration")
    grid = layout.row(align=False)
    for name, label in (("vt", "Vt"), ("wt", "Wt"), ("mt", "Mt")):
        col = grid.column(align=True)
        col.label(text=label)
        col.prop(data, name, expand=True)

    layout.separator()
    col = layout.column(align=True)
    col.prop(data, "geometry_type", expand=True)
    col = layout.column(align=True)
    if data.geometry_type == "TORI":
        col.prop(data, "major_radius")
        col.prop(data, "minor_radius")
        col.prop(data, "major_segments")
        col.prop(data, "minor_segments")
    else:
        col.prop(data, "plane_size")
        col.prop(data, "plane_subdivisions")

    layout.separator()
    layout.label(text="Shell Offsets")
    col = layout.column(align=True)
    for name in ("wt_axial", "wt_diagonal", "mt_axial", "mt_diagonal"):
        col.prop(data, name)

    layout.separator()
    layout.prop(data, "organize")
    layout.prop(data, "match_app_view")
    if data.geometry_type == "TORI":
        layout.prop(data, "smooth")
