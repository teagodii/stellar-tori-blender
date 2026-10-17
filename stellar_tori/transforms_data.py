# SPDX-License-Identifier: GPL-3.0-or-later
#
# GENERATED FILE — DO NOT EDIT.
# Generated from the Stellar-Tori app at commit e86a9fb894519b6e72636626f2465aaac6297146 (2026-10-16).
# Regenerate it from the app instead of editing it by hand.

"""Canonical Stellar-Tori transform data: 45 tori, 9 rotations, 63 configurations.

Positions are stored as signed references to four offset constants, so the
constants can be exposed as settings; the defaults below reproduce the canonical
figure exactly. Quaternions are (w, x, y, z), the order Blender's
``rotation_quaternion`` uses. The transforms are in the app's frame (Y-up).
"""

# Offset constants in world units. The diagonal values are canonical, not
# axial / sqrt(2) (0.7, not 0.7071...): never "correct" them.
OFFSET_DEFAULTS = {
    "WT_AXIAL": 1.0,
    "WT_DIAGONAL": 0.7,
    "MT_AXIAL": 2.4,
    "MT_DIAGONAL": 1.7,
}

# The nine distinct rotations, (w, x, y, z), at full double precision, in
# order of first use.
QUATERNIONS = {
    "IDENTITY": (1.0, 0.0, 0.0, 0.0),
    "Y90": (0.7071067811865476, 0.0, 0.7071067811865475, 0.0),
    "X90": (0.7071067811865476, 0.7071067811865475, 0.0, 0.0),
    "X45": (0.9238795325112867, 0.3826834323650898, 0.0, 0.0),
    "X45_NEG": (0.9238795325112867, -0.3826834323650898, 0.0, 0.0),
    "Y45": (0.9238795325112867, 0.0, 0.3826834323650898, 0.0),
    "Y45_NEG": (0.9238795325112867, 0.0, -0.3826834323650898, 0.0),
    "XY_DIAG_POS": (0.6532814824381883, 0.2705980500730985, 0.6532814824381882, -0.27059805007309845),
    "XY_DIAG_NEG": (0.6532814824381883, -0.2705980500730985, 0.6532814824381882, 0.27059805007309845),
}

# Torus index -> position as one entry per axis (x, y, z). Each entry is None
# for 0, or (sign, constant name), meaning sign * OFFSET_DEFAULTS[name].
POSITIONS = {
    1: (None, None, None),
    2: (None, None, None),
    3: (None, None, None),
    4: (None, None, (1, "WT_AXIAL")),
    5: (None, None, (-1, "WT_AXIAL")),
    6: (None, (-1, "WT_AXIAL"), None),
    7: (None, (1, "WT_AXIAL"), None),
    8: ((1, "WT_AXIAL"), None, None),
    9: ((-1, "WT_AXIAL"), None, None),
    10: (None, None, (1, "MT_AXIAL")),
    11: (None, None, (-1, "MT_AXIAL")),
    12: (None, (-1, "MT_AXIAL"), None),
    13: (None, (1, "MT_AXIAL"), None),
    14: ((1, "MT_AXIAL"), None, None),
    15: ((-1, "MT_AXIAL"), None, None),
    16: (None, None, None),
    17: (None, None, None),
    18: (None, None, None),
    19: (None, None, None),
    20: (None, None, None),
    21: (None, None, None),
    22: (None, (-1, "WT_DIAGONAL"), (1, "WT_DIAGONAL")),
    23: (None, (1, "WT_DIAGONAL"), (1, "WT_DIAGONAL")),
    24: (None, (-1, "WT_DIAGONAL"), (-1, "WT_DIAGONAL")),
    25: (None, (1, "WT_DIAGONAL"), (-1, "WT_DIAGONAL")),
    26: ((1, "WT_DIAGONAL"), None, (1, "WT_DIAGONAL")),
    27: ((-1, "WT_DIAGONAL"), None, (1, "WT_DIAGONAL")),
    28: ((1, "WT_DIAGONAL"), None, (-1, "WT_DIAGONAL")),
    29: ((-1, "WT_DIAGONAL"), None, (-1, "WT_DIAGONAL")),
    30: ((1, "WT_DIAGONAL"), (-1, "WT_DIAGONAL"), None),
    31: ((-1, "WT_DIAGONAL"), (-1, "WT_DIAGONAL"), None),
    32: ((1, "WT_DIAGONAL"), (1, "WT_DIAGONAL"), None),
    33: ((-1, "WT_DIAGONAL"), (1, "WT_DIAGONAL"), None),
    34: (None, (-1, "MT_DIAGONAL"), (1, "MT_DIAGONAL")),
    35: (None, (1, "MT_DIAGONAL"), (1, "MT_DIAGONAL")),
    36: (None, (-1, "MT_DIAGONAL"), (-1, "MT_DIAGONAL")),
    37: (None, (1, "MT_DIAGONAL"), (-1, "MT_DIAGONAL")),
    38: ((1, "MT_DIAGONAL"), None, (1, "MT_DIAGONAL")),
    39: ((-1, "MT_DIAGONAL"), None, (1, "MT_DIAGONAL")),
    40: ((1, "MT_DIAGONAL"), None, (-1, "MT_DIAGONAL")),
    41: ((-1, "MT_DIAGONAL"), None, (-1, "MT_DIAGONAL")),
    42: ((1, "MT_DIAGONAL"), (-1, "MT_DIAGONAL"), None),
    43: ((-1, "MT_DIAGONAL"), (-1, "MT_DIAGONAL"), None),
    44: ((1, "MT_DIAGONAL"), (1, "MT_DIAGONAL"), None),
    45: ((-1, "MT_DIAGONAL"), (1, "MT_DIAGONAL"), None),
}

# Torus index -> key into QUATERNIONS.
ROTATIONS = {
    1: "IDENTITY",
    2: "Y90",
    3: "X90",
    4: "IDENTITY",
    5: "IDENTITY",
    6: "X90",
    7: "X90",
    8: "Y90",
    9: "Y90",
    10: "IDENTITY",
    11: "IDENTITY",
    12: "X90",
    13: "X90",
    14: "Y90",
    15: "Y90",
    16: "X45",
    17: "X45_NEG",
    18: "Y45",
    19: "Y45_NEG",
    20: "XY_DIAG_POS",
    21: "XY_DIAG_NEG",
    22: "X45",
    23: "X45_NEG",
    24: "X45_NEG",
    25: "X45",
    26: "Y45",
    27: "Y45_NEG",
    28: "Y45_NEG",
    29: "Y45",
    30: "XY_DIAG_POS",
    31: "XY_DIAG_NEG",
    32: "XY_DIAG_NEG",
    33: "XY_DIAG_POS",
    34: "X45",
    35: "X45_NEG",
    36: "X45_NEG",
    37: "X45",
    38: "Y45",
    39: "Y45_NEG",
    40: "Y45_NEG",
    41: "Y45",
    42: "XY_DIAG_POS",
    43: "XY_DIAG_NEG",
    44: "XY_DIAG_NEG",
    45: "XY_DIAG_POS",
}

# Layer -> torus indices. Composites: 9Vt = 3Vt + 6Vt, 18Wt = 6Wt + 12Wt,
# 18Mt = 6Mt + 12Mt. The full families are 9Vt, 18Wt and 18Mt.
LAYERS = {
    "3Vt": (1, 2, 3),
    "6Vt": (16, 17, 18, 19, 20, 21),
    "9Vt": (1, 2, 3, 16, 17, 18, 19, 20, 21),
    "6Wt": (4, 5, 6, 7, 8, 9),
    "12Wt": (22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33),
    "18Wt": (4, 5, 6, 7, 8, 9, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33),
    "6Mt": (10, 11, 12, 13, 14, 15),
    "12Mt": (34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45),
    "18Mt": (10, 11, 12, 13, 14, 15, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45),
}

# The 3 x 3 configuration grid: each column takes none or one of its options.
VT_OPTIONS = ("3Vt", "6Vt", "9Vt")
WT_OPTIONS = ("6Wt", "12Wt", "18Wt")
MT_OPTIONS = ("6Mt", "12Mt", "18Mt")
DEFAULT_SELECTION = ("9Vt", "18Wt", "18Mt")

# Formal name by torus count.
FORMAL_NAMES = {
    3: "Tri-tori",
    6: "Hex-tori",
    9: "Ennea-tori",
    12: "Dodeka-tori",
    15: "Pentadeka-tori",
    18: "Octadeka-tori",
    21: "Icosikaihena-tori",
    24: "Icosikaitetra-tori",
    27: "Icosikaihepta-tori",
    30: "Triakonta-tori",
    33: "Triakontakaitri-tori",
    36: "Hexatriakonta-tori",
    39: "Triakontakaiennea-tori",
    42: "Tessarakontakaidi-tori",
    45: "Tessarakontakaipenta-tori",
}

# All 63 configurations in the app's order: (id, (vt, wt, mt), torus count).
CONFIGURATIONS = (
    ("3Vt", ("3Vt", None, None), 3),
    ("6Wt", (None, "6Wt", None), 6),
    ("6Mt", (None, None, "6Mt"), 6),
    ("6Vt", ("6Vt", None, None), 6),
    ("3Vt_6Wt", ("3Vt", "6Wt", None), 9),
    ("3Vt_6Mt", ("3Vt", None, "6Mt"), 9),
    ("9Vt", ("9Vt", None, None), 9),
    ("12Wt", (None, "12Wt", None), 12),
    ("6Wt_6Mt", (None, "6Wt", "6Mt"), 12),
    ("12Mt", (None, None, "12Mt"), 12),
    ("6Vt_6Wt", ("6Vt", "6Wt", None), 12),
    ("6Vt_6Mt", ("6Vt", None, "6Mt"), 12),
    ("3Vt_12Wt", ("3Vt", "12Wt", None), 15),
    ("3Vt_6Wt_6Mt", ("3Vt", "6Wt", "6Mt"), 15),
    ("3Vt_12Mt", ("3Vt", None, "12Mt"), 15),
    ("9Vt_6Wt", ("9Vt", "6Wt", None), 15),
    ("9Vt_6Mt", ("9Vt", None, "6Mt"), 15),
    ("18Wt", (None, "18Wt", None), 18),
    ("12Wt_6Mt", (None, "12Wt", "6Mt"), 18),
    ("6Wt_12Mt", (None, "6Wt", "12Mt"), 18),
    ("18Mt", (None, None, "18Mt"), 18),
    ("6Vt_12Wt", ("6Vt", "12Wt", None), 18),
    ("6Vt_6Wt_6Mt", ("6Vt", "6Wt", "6Mt"), 18),
    ("6Vt_12Mt", ("6Vt", None, "12Mt"), 18),
    ("3Vt_18Wt", ("3Vt", "18Wt", None), 21),
    ("3Vt_12Wt_6Mt", ("3Vt", "12Wt", "6Mt"), 21),
    ("3Vt_6Wt_12Mt", ("3Vt", "6Wt", "12Mt"), 21),
    ("3Vt_18Mt", ("3Vt", None, "18Mt"), 21),
    ("9Vt_12Wt", ("9Vt", "12Wt", None), 21),
    ("9Vt_6Wt_6Mt", ("9Vt", "6Wt", "6Mt"), 21),
    ("9Vt_12Mt", ("9Vt", None, "12Mt"), 21),
    ("18Wt_6Mt", (None, "18Wt", "6Mt"), 24),
    ("12Wt_12Mt", (None, "12Wt", "12Mt"), 24),
    ("6Wt_18Mt", (None, "6Wt", "18Mt"), 24),
    ("6Vt_18Wt", ("6Vt", "18Wt", None), 24),
    ("6Vt_12Wt_6Mt", ("6Vt", "12Wt", "6Mt"), 24),
    ("6Vt_6Wt_12Mt", ("6Vt", "6Wt", "12Mt"), 24),
    ("6Vt_18Mt", ("6Vt", None, "18Mt"), 24),
    ("3Vt_18Wt_6Mt", ("3Vt", "18Wt", "6Mt"), 27),
    ("3Vt_12Wt_12Mt", ("3Vt", "12Wt", "12Mt"), 27),
    ("3Vt_6Wt_18Mt", ("3Vt", "6Wt", "18Mt"), 27),
    ("9Vt_18Wt", ("9Vt", "18Wt", None), 27),
    ("9Vt_12Wt_6Mt", ("9Vt", "12Wt", "6Mt"), 27),
    ("9Vt_6Wt_12Mt", ("9Vt", "6Wt", "12Mt"), 27),
    ("9Vt_18Mt", ("9Vt", None, "18Mt"), 27),
    ("18Wt_12Mt", (None, "18Wt", "12Mt"), 30),
    ("12Wt_18Mt", (None, "12Wt", "18Mt"), 30),
    ("6Vt_18Wt_6Mt", ("6Vt", "18Wt", "6Mt"), 30),
    ("6Vt_12Wt_12Mt", ("6Vt", "12Wt", "12Mt"), 30),
    ("6Vt_6Wt_18Mt", ("6Vt", "6Wt", "18Mt"), 30),
    ("3Vt_18Wt_12Mt", ("3Vt", "18Wt", "12Mt"), 33),
    ("3Vt_12Wt_18Mt", ("3Vt", "12Wt", "18Mt"), 33),
    ("9Vt_18Wt_6Mt", ("9Vt", "18Wt", "6Mt"), 33),
    ("9Vt_12Wt_12Mt", ("9Vt", "12Wt", "12Mt"), 33),
    ("9Vt_6Wt_18Mt", ("9Vt", "6Wt", "18Mt"), 33),
    ("18Wt_18Mt", (None, "18Wt", "18Mt"), 36),
    ("6Vt_18Wt_12Mt", ("6Vt", "18Wt", "12Mt"), 36),
    ("6Vt_12Wt_18Mt", ("6Vt", "12Wt", "18Mt"), 36),
    ("3Vt_18Wt_18Mt", ("3Vt", "18Wt", "18Mt"), 39),
    ("9Vt_18Wt_12Mt", ("9Vt", "18Wt", "12Mt"), 39),
    ("9Vt_12Wt_18Mt", ("9Vt", "12Wt", "18Mt"), 39),
    ("6Vt_18Wt_18Mt", ("6Vt", "18Wt", "18Mt"), 42),
    ("9Vt_18Wt_18Mt", ("9Vt", "18Wt", "18Mt"), 45),
)
