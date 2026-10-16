# SPDX-License-Identifier: GPL-3.0-or-later
"""Live figures: settings stored on the root empty, regenerated in place whenever they change.

Every object carries ``Object.stellar_tori`` (a ``StellarToriSettings``). Its
``role`` marks what the add-on built:

- ``ROOT``: a figure's root empty. Its settings are the figure's ``build.Params``.
  Changing any of them (from the sidebar or from Python) regenerates the figure.
- ``PART``: a torus, plane or family object built under a root. A regenerate
  deletes and rebuilds every part, so edits made to a single part are lost.
- ``NONE``: everything else, including detached figures.

A regenerate keeps the root itself: its name (unless the configuration changes
and the name is still the generated one), location, rotation, scale, parent
and collection. Toggling "Match Viewer Orientation" adds or removes the +90° X
turn on top of whatever rotation the root has. Nothing here uses ``bpy.ops``.
"""

import re

import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty
from mathutils import Quaternion

from . import build
from . import settings

ROLES = (("NONE", "None", "Not part of a live figure"),
         ("ROOT", "Root", "The root empty of a live figure"),
         ("PART", "Part", "An object built under a live figure's root"))

_SUFFIX = re.compile(r"\.\d{3,}$")  # Blender's ".001" name suffix


def _on_update(self, context):
    if self.role != "ROOT" or context.mode != "OBJECT":
        return
    try:
        regenerate(self.id_data, context.view_layer)
    except ValueError as exc:  # the figure is left as it was
        print(f"Stellar Tori: can't regenerate {self.id_data.name!r}: {exc}")


class StellarToriSettings(bpy.types.PropertyGroup):
    __annotations__ = {
        **settings.properties(update=_on_update),
        "role": EnumProperty(name="Role", items=ROLES, default="NONE", options=set()),
        # What the last build applied, so a regenerate knows what changed.
        "generated_name": StringProperty(name="Generated Name", options=set()),
        "view_applied": BoolProperty(name="View Turn Applied", options=set()),
    }


# ============================================
# FINDING FIGURES
# ============================================

def figure_root(ob):
    """The root of the live figure ``ob`` belongs to (``ob`` itself for a root), or None."""
    if ob is None:
        return None
    role = ob.stellar_tori.role
    if role == "ROOT":
        return ob
    if role == "PART" and ob.parent is not None and ob.parent.stellar_tori.role == "ROOT":
        return ob.parent
    return None


def parts(root):
    """The objects the add-on built under ``root``."""
    return [ob for ob in root.children if ob.stellar_tori.role == "PART"]


# ============================================
# ADOPT / REGENERATE / DETACH
# ============================================

def adopt(result, params):
    """Make a fresh ``build.build`` result a live figure: store ``params`` on its root."""
    data = result.root.stellar_tori
    settings.from_params(data, params)  # role is still NONE, so this doesn't regenerate
    data.generated_name = build.configuration_name(params)
    data.view_applied = params.match_app_view
    data.role = "ROOT"
    for ob in result.objects:
        ob.stellar_tori.role = "PART"


def regenerate(root, view_layer=None):
    """Rebuild ``root``'s figure from its stored settings, in place. Returns the new parts.

    Raises ValueError, with nothing changed, if the settings can't be built.
    """
    data = root.stellar_tori
    params = settings.to_params(data)
    build.validate(params)
    view_layer = view_layer or bpy.context.view_layer
    home = root.users_collection[0] if root.users_collection else bpy.context.scene.collection

    old = parts(root)
    active_was_part = view_layer.objects.active in old
    meshes = {ob.data for ob in old if ob.data is not None}
    groups = {c for ob in old for c in ob.users_collection if c in home.children.values()}
    bpy.data.batch_remove(old)
    bpy.data.batch_remove([m for m in meshes if m.users == 0]
                          + [c for c in groups if not c.objects and not c.children])

    new = build.build_parts(params, home, root)
    for ob in new:
        ob.stellar_tori.role = "PART"
    _rename(root, home, build.configuration_name(params))
    _apply_view(root, params.match_app_view)

    if active_was_part:
        root.select_set(True, view_layer=view_layer)
        view_layer.objects.active = root
    return new


def detach(root):
    """Turn ``root``'s figure into plain objects: the settings are dropped and nothing regenerates."""
    for ob in parts(root):
        ob.property_unset("stellar_tori")
    root.property_unset("stellar_tori")


def _rename(root, home, name):
    """Follow a configuration change, unless the root or collection was renamed by hand."""
    data = root.stellar_tori
    old = data.generated_name
    if name == old:
        return
    if _SUFFIX.sub("", root.name) == old:
        root.name = name
    roots_in_home = [ob for ob in home.objects if ob.stellar_tori.role == "ROOT"]
    if not home.is_embedded_data and _SUFFIX.sub("", home.name) == old and roots_in_home == [root]:
        home.name = name
    data.generated_name = name


def _apply_view(root, match_app_view):
    """Add or remove the +90° X turn, keeping any rotation the root was given by hand."""
    data = root.stellar_tori
    if data.view_applied == match_app_view:
        return
    turn = Quaternion(build.APP_VIEW_ROTATION)
    if not match_app_view:
        turn.invert()
    q = _rotation(root) @ turn
    for exact in (build.APP_VIEW_ROTATION, build.IDENTITY_ROTATION):
        if max(abs(a - b) for a, b in zip(q, exact)) < 1e-6:
            q = Quaternion(exact)  # an untouched root lands exactly where build() puts it
    _set_rotation(root, q)
    data.view_applied = match_app_view


def _rotation(ob):
    if ob.rotation_mode == "QUATERNION":
        return ob.rotation_quaternion.copy()
    if ob.rotation_mode == "AXIS_ANGLE":
        angle, *axis = ob.rotation_axis_angle
        return Quaternion(axis, angle)
    return ob.rotation_euler.to_quaternion()


def _set_rotation(ob, q):
    if ob.rotation_mode == "QUATERNION":
        ob.rotation_quaternion = q
    elif ob.rotation_mode == "AXIS_ANGLE":
        axis, angle = q.to_axis_angle()
        ob.rotation_axis_angle = (angle, *axis)
    else:
        ob.rotation_euler = q.to_euler(ob.rotation_mode, ob.rotation_euler)


# ============================================
# REGISTRATION
# ============================================

def register():
    bpy.utils.register_class(StellarToriSettings)
    bpy.types.Object.stellar_tori = bpy.props.PointerProperty(type=StellarToriSettings)


def unregister():
    del bpy.types.Object.stellar_tori
    bpy.utils.unregister_class(StellarToriSettings)
