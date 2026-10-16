# SPDX-License-Identifier: GPL-3.0-or-later
"""Build a Stellar Tori configuration as Blender objects from plain parameters.

``build(params)`` doesn't depend on operators, UI context or ``bpy.ops``, so the
"Add Stellar Tori" operator and a later live-regenerate path can share it.

Result, for the default 9Vt + 18Wt + 18Mt:

    Tessarakontakaipenta-tori (9Vt + 18Wt + 18Mt)    collection, linked under the target
    ├── Tessarakontakaipenta-tori (9Vt + 18Wt + 18Mt)  root empty, +90° about X
    └── 1t … 45t                                     one object per torus, parented to the root

Per-torus transforms are copied exactly, in the web viewer's Y-up frame. The
root's +90° turn about X makes the figure read as the viewer shows it, with the
viewer's default view becoming Blender's Front view. Organize modes:

- ``OBJECTS``: every torus is its own object, all sharing one mesh.
- ``GROUPED``: the same objects, split into one sub-collection per family,
  named by the selected layer (for example "9Vt", "18Wt", "18Mt").
- ``JOINED``: one mesh object per family (named by its layer). Each torus's
  transform is baked into the vertices in double precision.

Names are deterministic. Blender adds ".001"-style suffixes only when a name is
already taken.
"""

import math
from dataclasses import dataclass, field

import bpy

from . import geometry
from . import transforms_data as td

FAMILIES = ("Vt", "Wt", "Mt")
FAMILY_OPTIONS = {"Vt": td.VT_OPTIONS, "Wt": td.WT_OPTIONS, "Mt": td.MT_OPTIONS}
GEOMETRY_TYPES = ("TORI", "PLANES")
ORGANIZE_MODES = ("OBJECTS", "GROUPED", "JOINED")

# +90° about X takes the viewer's +Y (up) to Blender's +Z.
APP_VIEW_ROTATION = (math.cos(math.pi / 4), math.sin(math.pi / 4), 0.0, 0.0)
IDENTITY_ROTATION = (1.0, 0.0, 0.0, 0.0)


@dataclass
class Params:
    """Every build setting as a flat field, ready to mirror as Blender properties."""

    vt: str | None = td.DEFAULT_SELECTION[0]
    wt: str | None = td.DEFAULT_SELECTION[1]
    mt: str | None = td.DEFAULT_SELECTION[2]
    geometry_type: str = "TORI"
    major_radius: float = geometry.MAJOR_RADIUS
    minor_radius: float = geometry.MINOR_RADIUS
    major_segments: int = geometry.MAJOR_SEGMENTS
    minor_segments: int = geometry.MINOR_SEGMENTS
    plane_size: float = geometry.PLANE_SIZE
    plane_subdivisions: int = geometry.PLANE_SUBDIVISIONS
    wt_axial: float = td.OFFSET_DEFAULTS["WT_AXIAL"]
    wt_diagonal: float = td.OFFSET_DEFAULTS["WT_DIAGONAL"]
    mt_axial: float = td.OFFSET_DEFAULTS["MT_AXIAL"]
    mt_diagonal: float = td.OFFSET_DEFAULTS["MT_DIAGONAL"]
    match_app_view: bool = True
    organize: str = "OBJECTS"
    smooth: bool = True

    def offsets(self):
        return {
            "WT_AXIAL": self.wt_axial,
            "WT_DIAGONAL": self.wt_diagonal,
            "MT_AXIAL": self.mt_axial,
            "MT_DIAGONAL": self.mt_diagonal,
        }


@dataclass
class BuildResult:
    collection: bpy.types.Collection
    root: bpy.types.Object
    objects: list = field(default_factory=list)  # the torus / family objects, in build order


# ============================================
# PURE HELPERS
# ============================================

def selection(params):
    """[(family, layer, indices)] for the families the selection uses, in Vt, Wt, Mt order."""
    chosen = []
    for family in FAMILIES:
        layer = getattr(params, family.lower())
        if layer is None:
            continue
        if layer not in FAMILY_OPTIONS[family]:
            raise ValueError(f"{family} must be one of {FAMILY_OPTIONS[family]} or None, got {layer!r}")
        chosen.append((family, layer, td.LAYERS[layer]))
    if not chosen:
        raise ValueError("the selection is empty: choose at least one of Vt, Wt, Mt")
    return chosen


def configuration_name(params):
    """'<formal name> (<layers>)', for example 'Tri-tori (3Vt)'."""
    layers = [layer for _, layer, _ in selection(params)]
    count = sum(len(indices) for _, _, indices in selection(params))
    return f"{td.FORMAL_NAMES[count]} ({' + '.join(layers)})"


def torus_position(index, offsets):
    """Local position of torus ``index`` with the given offset constants."""
    return tuple(0.0 if ref is None else ref[0] * offsets[ref[1]] for ref in td.POSITIONS[index])


def torus_rotation(index):
    return td.QUATERNIONS[td.ROTATIONS[index]]


def rotate(q, v):
    """Rotate vector v by unit quaternion q = (w, x, y, z), in double precision."""
    w, x, y, z = q
    vx, vy, vz = v
    tx = 2.0 * (y * vz - z * vy)
    ty = 2.0 * (z * vx - x * vz)
    tz = 2.0 * (x * vy - y * vx)
    return (
        vx + w * tx + (y * tz - z * ty),
        vy + w * ty + (z * tx - x * tz),
        vz + w * tz + (x * ty - y * tx),
    )


def _validate(params):
    if params.geometry_type not in GEOMETRY_TYPES:
        raise ValueError(f"geometry_type must be one of {GEOMETRY_TYPES}, got {params.geometry_type!r}")
    if params.organize not in ORGANIZE_MODES:
        raise ValueError(f"organize must be one of {ORGANIZE_MODES}, got {params.organize!r}")
    selection(params)


def _local_lattice(params):
    """(verts, faces) of one torus or plane in its own frame."""
    if params.geometry_type == "TORI":
        args = (params.major_radius, params.minor_radius, params.major_segments, params.minor_segments)
        return geometry.torus_vertices(*args), geometry.torus_faces(*args[2:])
    return (geometry.plane_vertices(params.plane_size, params.plane_subdivisions),
            geometry.plane_faces(params.plane_subdivisions))


# ============================================
# BUILD
# ============================================

def build(params=None, collection=None):
    """Create the configuration under ``collection`` (default: the scene's master collection)."""
    params = params or Params()
    _validate(params)
    target = collection if collection is not None else bpy.context.scene.collection
    name = configuration_name(params)
    offsets = params.offsets()

    config = bpy.data.collections.new(name)
    target.children.link(config)

    root = bpy.data.objects.new(name, None)
    root.empty_display_type = "PLAIN_AXES"
    root.rotation_mode = "QUATERNION"
    root.rotation_quaternion = APP_VIEW_ROTATION if params.match_app_view else IDENTITY_ROTATION
    config.objects.link(root)

    result = BuildResult(collection=config, root=root)
    if params.organize == "JOINED":
        _build_joined(params, offsets, config, root, result)
    else:
        _build_objects(params, offsets, config, root, result)
    return result


def _shared_mesh(params):
    if params.geometry_type == "TORI":
        return geometry.new_torus_mesh(
            "Stellar Torus", params.major_radius, params.minor_radius,
            params.major_segments, params.minor_segments, smooth=params.smooth)
    return geometry.new_plane_mesh("Stellar Plane", params.plane_size, params.plane_subdivisions)


def _build_objects(params, offsets, config, root, result):
    mesh = _shared_mesh(params)
    for _family, layer, indices in selection(params):
        if params.organize == "GROUPED":
            home = bpy.data.collections.new(layer)
            config.children.link(home)
        else:
            home = config
        for index in indices:
            ob = bpy.data.objects.new(f"{index}t", mesh)
            ob.rotation_mode = "QUATERNION"
            ob.location = torus_position(index, offsets)
            ob.rotation_quaternion = torus_rotation(index)
            ob.parent = root
            home.objects.link(ob)
            result.objects.append(ob)


def _build_joined(params, offsets, config, root, result):
    local_verts, local_faces = _local_lattice(params)
    stride = len(local_verts)
    for _family, layer, indices in selection(params):
        verts, faces = [], []
        for k, index in enumerate(indices):
            q = torus_rotation(index)
            px, py, pz = torus_position(index, offsets)
            for v in local_verts:
                rx, ry, rz = rotate(q, v)
                verts.append((rx + px, ry + py, rz + pz))
            base = k * stride
            faces.extend(tuple(base + i for i in face) for face in local_faces)
        mesh = bpy.data.meshes.new(layer)
        mesh.from_pydata(verts, [], faces)
        if params.geometry_type == "TORI" and params.smooth:
            mesh.shade_smooth()
        ob = bpy.data.objects.new(layer, mesh)
        ob.rotation_mode = "QUATERNION"
        ob.parent = root
        config.objects.link(ob)
        result.objects.append(ob)
