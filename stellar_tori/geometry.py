# SPDX-License-Identifier: GPL-3.0-or-later
"""Torus and plane mesh builders on the canonical Stellar Tori lattice.

Vertices sit exactly on the web viewer's wireframe lattice. The angles, the
expression order and the vertex order (theta outer, phi inner; plane x outer,
y inner) are the same, so a default mesh reproduces the viewer's points.

Torus, local frame: ring in the XY plane, axis along +Z.
    theta_i = (i / major_segments) * 2 pi, phi_j = (j / minor_segments) * 2 pi
    r = R + r_minor cos(phi);  P = (cos(theta) r, sin(theta) r, r_minor sin(phi))
Plane, local frame: square in XY facing +Z, half-extent ``size``.
    grid line i at -s + (2 s i) / n

The lattice functions are pure Python, so they can be tested without Blender.
The ``new_*_mesh`` functions wrap them in mesh datablocks. Blender stores
coordinates as float32.
"""

import math

import bpy

# The web viewer's defaults. A minor radius equal to the major radius makes a
# horn torus.
MAJOR_RADIUS = 1.0
MINOR_RADIUS = 1.0
MAJOR_SEGMENTS = 96
MINOR_SEGMENTS = 29
PLANE_SIZE = 1.0
PLANE_SUBDIVISIONS = 1

# Fewer than 3 segments around either circle can't close a mesh.
MIN_SEGMENTS = 3


def _segments(value, name):
    count = int(value)
    if count != value or count < MIN_SEGMENTS:
        raise ValueError(f"{name} must be a whole number >= {MIN_SEGMENTS}, got {value!r}")
    return count


def torus_vertices(major_radius, minor_radius, major_segments, minor_segments):
    """Torus lattice points, index ``i * minor_segments + j``."""
    n_theta = _segments(major_segments, "major_segments")
    n_phi = _segments(minor_segments, "minor_segments")
    verts = []
    for i in range(n_theta):
        theta = (i / n_theta) * math.pi * 2
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        for j in range(n_phi):
            phi = (j / n_phi) * math.pi * 2
            r = major_radius + minor_radius * math.cos(phi)
            verts.append((cos_theta * r, sin_theta * r, minor_radius * math.sin(phi)))
    return verts


def torus_faces(major_segments, minor_segments):
    """Quads wrapping both ways. Winding follows theta then phi, so normals face outward."""
    n_theta = _segments(major_segments, "major_segments")
    n_phi = _segments(minor_segments, "minor_segments")
    faces = []
    for i in range(n_theta):
        i_next = (i + 1) % n_theta
        for j in range(n_phi):
            j_next = (j + 1) % n_phi
            faces.append((
                i * n_phi + j,
                i_next * n_phi + j,
                i_next * n_phi + j_next,
                i * n_phi + j_next,
            ))
    return faces


def _subdivisions(value):
    count = int(value)
    if count != value or count < 1:
        raise ValueError(f"subdivisions must be a whole number >= 1, got {value!r}")
    return count


def plane_vertices(size, subdivisions):
    """Plane grid corners, index ``i * (n + 1) + j`` with x from i and y from j."""
    n = _subdivisions(subdivisions)
    s = size
    verts = []
    for i in range(n + 1):
        x = -s + (2 * s * i) / n
        for j in range(n + 1):
            y = -s + (2 * s * j) / n
            verts.append((x, y, 0.0))
    return verts


def plane_faces(subdivisions):
    """n x n quads, counter-clockwise seen from +Z, so normals face +Z."""
    n = _subdivisions(subdivisions)
    row = n + 1
    return [
        (i * row + j, (i + 1) * row + j, (i + 1) * row + j + 1, i * row + j + 1)
        for i in range(n)
        for j in range(n)
    ]


def _new_mesh(name, verts, faces, smooth):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)  # builds edges and shades flat
    if smooth:
        mesh.shade_smooth()
    return mesh


def new_torus_mesh(name, major_radius=MAJOR_RADIUS, minor_radius=MINOR_RADIUS,
                   major_segments=MAJOR_SEGMENTS, minor_segments=MINOR_SEGMENTS, smooth=True):
    """A new torus mesh datablock on the canonical lattice (smooth-shaded by default)."""
    verts = torus_vertices(major_radius, minor_radius, major_segments, minor_segments)
    return _new_mesh(name, verts, torus_faces(major_segments, minor_segments), smooth)


def new_plane_mesh(name, size=PLANE_SIZE, subdivisions=PLANE_SUBDIVISIONS):
    """A new plane mesh datablock on the canonical grid."""
    return _new_mesh(name, plane_vertices(size, subdivisions), plane_faces(subdivisions), smooth=False)
