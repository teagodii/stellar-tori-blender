# Stellar-Tori Blender

A Blender extension that generates **Stellar-Tori**: 45 symmetrically placed tori (or planes) that combine into 63 configurations. For more information, check out the interactive web viewer at [StellarTori.com](https://stellartori.com).

> **Status: v0.1, in development.** Base generation works: tori and planes at the canonical positions and rotations, with configurable dimensions and positions that stay editable.

## Install

1. Download `stellar_tori-<version>.zip` from the [Releases](https://github.com/teagodii/stellar-tori-blender/releases) page (not the "Source code" archives).
2. In Blender, open **Edit > Preferences > Add-ons**, click the **⌄** menu at the top right, choose **Install from Disk…** and pick that `.zip`.

Pick the **.zip** itself, not the unzipped folder.

## Use

- **Add > Mesh > Stellar-Tori** (3D Viewport, Object Mode) adds the full 45-tori figure at the 3D cursor.
- Change the settings right after adding in the **Adjust Last Operation** panel, or at any time later in the sidebar (**N**) under the **Stellar-Tori** tab. Select the figure's root empty or any of its tori to edit it there.
- Pick a configuration from the **Vt / Wt / Mt** grid. Each column takes one of its layers or none.
- Choose **Tori** or **Planes** and adjust them: major and minor radius and segments, or plane size and subdivisions; the four shell offsets; how the result is organized (one object per torus, grouped by layer, or one joined mesh per family); whether the figure stands as in the web viewer; smooth shading.
- Every change rebuilds the figure in place. The root empty keeps its location, rotation and scale, so you can move the whole figure freely.
- A rebuild replaces the tori, so changes made to a single torus are lost. When the figure is set, click **Detach** to turn it into plain objects that you can edit by hand.

## Requirements

Blender 4.2 or newer.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
