# Stellar Tori for Blender

A Blender extension that generates the **Stellar Tori**: 45 mathematically placed tori (or planes) that combine into 63 configurations. It uses the same geometry truth as the interactive viewer at [stellartori.com](https://stellartori.com).

> **Status: v0.1, in development.** Base generation works: tori and planes at the canonical positions and rotations, with configurable dimensions and positions that stay editable. Wireframe styling, particles and glass render scenes come later.

## Install

1. Build the extension package from this repository (Blender 4.2 or newer):

   ```
   mkdir dist
   blender --command extension build --source-dir stellar_tori --output-dir dist
   ```

2. In Blender, open **Edit > Preferences > Add-ons**, click the **⌄** menu at the top right, choose **Install from Disk…** and pick `dist/stellar_tori-<version>.zip`.

Pick the **.zip** itself. Selecting the `.py` files inside it installs them as separate legacy add-ons that don't work.

## Use

- **Add > Mesh > Stellar Tori** (3D Viewport, Object Mode) adds the full 45-tori figure at the 3D cursor.
- Pick a configuration from the **Vt / Wt / Mt** grid. Each column takes one of its layers or none.
- Choose **Tori** or **Planes** and adjust them: major and minor radius and segments, or plane size and subdivisions; the four shell offsets; how the result is organized (one object per torus, grouped by layer, or one joined mesh per family); whether the figure stands as in the web viewer; smooth shading.
- Change the settings right after adding in the **Adjust Last Operation** panel, or at any time later in the sidebar (**N**) under the **Stellar Tori** tab. Select the figure's root empty or any of its tori to edit it there.
- Every change rebuilds the figure in place. The root empty keeps its location, rotation and scale, so you can move the whole figure freely.
- A rebuild replaces the tori, so changes made to a single torus are lost. When the figure is set, click **Detach** to turn it into plain objects that you can edit by hand.

## Requirements

Blender with extension support (4.2 or newer). Development and testing use Blender 5.1.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
