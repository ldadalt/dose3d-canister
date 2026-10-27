"""Slice, isodose and sweep figures.

Interactive files use Plotly. The GIF and PDF images use Matplotlib so a
README preview does not need a display.

The 3D view extracts Mesh3d shells with marching cubes on a downsampled
grid. That keeps the HTML small: Plotly Isosurface would embed the full
volume once per gray level and stall the browser.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.animation import PillowWriter
from plotly.subplots import make_subplots
from skimage.measure import marching_cubes

from dose3d_canister.criteria import (
    BCSH,
    DoseCriteria,
    FDA_AABB,
    JAPAN,
    PORTARIA_158,
)
from dose3d_canister.interpolate import DoseVolume

# Levels used on blood-irradiator isodose maps, in gray.
CLINICAL_ISODOSE_GY = (15, 20, 25, 30, 35, 40, 45, 50)
# Cool→warm clinical scale (brochure-like): outer low dose → inner hot.
_ISODOSE_COLOR = {
    15: "#1f6f8b",
    20: "#2a9d8f",
    25: "#e9c46a",
    30: "#f4a261",
    35: "#e76f51",
    40: "#d62828",
    45: "#9b2226",
    50: "#6a040f",
}
# Display grid for WebGL: denser grid + no face-stride keeps shells intact.
_DEFAULT_VIEW_MAX_SIDE = 32
_PLOTLY_CONFIG = {"responsive": True, "displaylogo": False}
_SCENE_BG = "#eef2f5"
_AXIS_GRID = "#c5ced6"
_CANISTER_LINE = "#5c6b7a"
# Compare-ready criteria overlays (key, preset, fail-low color, fail-high color).
_COMPARE_CRITERIA: tuple[tuple[str, DoseCriteria, str, str], ...] = (
    ("japan", JAPAN, "#2563eb", "#b91c1c"),
    ("fda", FDA_AABB, "#0f766e", "#c2410c"),
    ("bcsh", BCSH, "#7c3aed", "#b45309"),
    ("portaria", PORTARIA_158, "#15803d", "#9f1239"),
)
_MESH_LIGHTING = dict(
    ambient=0.38,
    diffuse=0.9,
    fresnel=0.22,
    specular=0.65,
    roughness=0.28,
)
_CLINICAL_COLORSCALE = [
    [0.00, "#1f6f8b"],
    [0.25, "#2a9d8f"],
    [0.45, "#e9c46a"],
    [0.60, "#f4a261"],
    [0.75, "#e76f51"],
    [0.90, "#d62828"],
    [1.00, "#6a040f"],
]


def _finite_limits(dose_gy: np.ndarray) -> tuple[float, float]:
    finite = np.asarray(dose_gy, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return 0.0, 1.0
    return float(finite.min()), float(finite.max())


def clinical_isodose_levels(dose_gy: np.ndarray) -> list[float]:
    """Standard gray contours that fall strictly inside the reconstructed range."""

    finite = np.asarray(dose_gy, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return []
    low = float(finite.min())
    high = float(finite.max())
    return [float(level) for level in CLINICAL_ISODOSE_GY if low < level < high]


def write_html(
    volume: DoseVolume,
    path: str | Path,
    title: str,
    *,
    criteria: DoseCriteria | None = None,
    view_max_side: int = _DEFAULT_VIEW_MAX_SIDE,
) -> None:
    """Write a light page: 2D isodose plus a full Mesh3d 3D model with filters.

    The 3D block is deferred with ``requestIdleCallback`` so the axial /
    coronal maps paint first on slow machines. Toolbar filters only toggle
    precomputed traces (min Gy, percentile, optional norm overlays).
    """

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    isodose = _isodose_figure(volume, title)
    model, filter_meta = _isosurface_figure(
        volume,
        title,
        criteria=criteria,
        max_side=view_max_side,
    )
    isodose_div = isodose.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config=_PLOTLY_CONFIG,
        div_id="isodose-plot",
    )
    model_json = model.to_json().replace("</", "<\\/")
    filters_json = json.dumps(filter_meta).replace("</", "<\\/")
    plotly_config = json.dumps(_PLOTLY_CONFIG)
    gy_options = "".join(
        f'<option value="{level}">≥ {level:.0f} Gy</option>'
        for level in filter_meta.get("shell_levels_gy", [])
    )
    pct_options = "".join(
        f'<option value="{p["gy"]}">P{p["percentile"]} (≥ {p["gy"]:.1f} Gy)</option>'
        for p in filter_meta.get("percentiles", [])
    )
    compare_items = filter_meta.get("compare", [])
    criteria_cards = []
    compare_checks = []
    for item in compare_items:
        hint = str(item.get("hint", "")).replace("'", "").replace('"', "")
        rules = str(item.get("rules", hint)).replace("'", "").replace('"', "")
        note = "" if item.get("has_overlay") else " · within bounds on this map"
        color = item.get("color", "#5c6b7a")
        compare_checks.append(
            "<label class='check'><input type='checkbox' class='flt-compare' data-criteria='"
            + item["key"]
            + "'> "
            + item["label"]
            + "</label>"
        )
        criteria_cards.append(
            "<article class='crit-card' data-criteria='"
            + item["key"]
            + "'>"
            + "<header><span class='swatch' style='background:"
            + color
            + "'></span><strong>"
            + item["label"]
            + "</strong></header>"
            + "<p>"
            + rules
            + note
            + "</p></article>"
        )
    compare_block = (
        "<div class='tool-group'><span class='tool-label'>Show criteria</span>"
        + "".join(compare_checks)
        + "</div>"
    )
    criteria_panel = "".join(criteria_cards)
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink: #1a2332;
    --muted: #5a6778;
    --line: #d5dde5;
    --paper: #f7f9fb;
    --accent: #c1121f;
    --side: 320px;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: "Source Sans 3", "Segoe UI", sans-serif;
    color: var(--ink);
    background:
      radial-gradient(1200px 500px at 10% -10%, #dde7ef 0%, transparent 55%),
      radial-gradient(900px 400px at 100% 0%, #f0e6e4 0%, transparent 45%),
      var(--paper);
  }}
  .wrap {{
    width: min(1860px, 100%);
    max-width: 1860px;
    margin: 0 auto;
    padding: 1.1rem 1.5rem 1.8rem;
  }}
  h1 {{
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0 0 0.4rem;
  }}
  h1 span.brand {{
    display: block;
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.3rem;
  }}
  .lede {{
    color: var(--muted);
    max-width: 92ch;
    line-height: 1.45;
    margin: 0 0 1.1rem;
    font-size: 1rem;
  }}
  h2 {{
    font-size: 1.1rem;
    font-weight: 600;
    margin: 1.35rem 0 0.5rem;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid var(--line);
  }}
  .toolbar {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem 1.25rem;
    align-items: center;
    padding: 0.8rem 1rem;
    margin: 0 0 0.55rem;
    border: 1px solid var(--line);
    border-radius: 10px;
    background: #fff;
  }}
  .tool-group {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem 0.85rem;
    align-items: center;
  }}
  .tool-label {{
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    margin-right: 0.15rem;
  }}
  .toolbar select {{
    font: inherit;
    font-size: 0.92rem;
    padding: 0.3rem 0.5rem;
    border: 1px solid var(--line);
    border-radius: 6px;
    background: #fff;
    color: var(--ink);
  }}
  .toolbar .check {{
    display: inline-flex;
    gap: 0.35rem;
    align-items: center;
    font-size: 0.9rem;
    color: var(--ink);
    cursor: pointer;
    user-select: none;
  }}
  .stage-3d {{
    display: grid;
    grid-template-columns: minmax(0, 1fr) var(--side);
    gap: 0.85rem;
    align-items: stretch;
  }}
  .stage-main {{
    min-width: 0;
  }}
  .stage-side {{
    border: 1px solid var(--line);
    border-radius: 10px;
    background: #fff;
    padding: 0.85rem 0.9rem 1rem;
    box-shadow: 0 8px 28px rgba(26, 35, 50, 0.06);
    overflow: auto;
    max-height: calc(820px + 4.5rem);
  }}
  .stage-side h3 {{
    margin: 0.85rem 0 0.45rem;
    font-size: 0.72rem;
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--muted);
  }}
  .stage-side h3:first-child {{ margin-top: 0; }}
  .crit-card {{
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 0.55rem 0.65rem;
    margin: 0 0 0.45rem;
    background: #fbfcfd;
  }}
  .crit-card header {{
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.25rem;
  }}
  .crit-card strong {{ font-size: 0.92rem; }}
  .crit-card p {{
    margin: 0;
    color: var(--muted);
    font-size: 0.82rem;
    line-height: 1.35;
  }}
  .swatch {{
    width: 0.7rem;
    height: 0.7rem;
    border-radius: 2px;
    flex: 0 0 auto;
  }}
  #layer-legend {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}
  #layer-legend li {{
    display: flex;
    align-items: flex-start;
    gap: 0.45rem;
    padding: 0.28rem 0;
    font-size: 0.86rem;
    line-height: 1.3;
    border-bottom: 1px solid #eef2f5;
  }}
  #layer-legend li:last-child {{ border-bottom: 0; }}
  #layer-legend .swatch {{ margin-top: 0.2rem; }}
  #volume3d-host {{
    min-height: 820px;
    height: 820px;
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
    background: {_SCENE_BG};
    box-shadow: 0 12px 40px rgba(26, 35, 50, 0.08);
  }}
  #volume3d-host .js-plotly-plot,
  #volume3d-host .plot-container {{
    width: 100% !important;
    height: 100% !important;
  }}
  #volume3d-status {{
    color: var(--muted);
    font-size: 0.92rem;
    margin: 0.3rem 0 0.55rem;
  }}
  #isodose-plot {{
    width: 100%;
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 8px 28px rgba(26, 35, 50, 0.06);
  }}
  @media (max-width: 1400px) {{
    .stage-3d {{ grid-template-columns: 1fr; }}
    .stage-side {{ max-height: none; }}
    #volume3d-host {{ min-height: 640px; height: 640px; }}
  }}
</style>
</head><body>
<div class="wrap">
<h1><span class="brand">dose3d-canister</span>{title}</h1>
<p class="lede">3D Mesh3d isodose inside the canister. Use <b>View</b> to show
isodose shells, criteria overlays only, or both. Criteria cards on the right
list the regulatory bounds in full — neither curve nor surface is a measurement.</p>
<h2>Isodose planes</h2>
{isodose_div}
<h2>3D isodose</h2>
<div class="stage-3d">
  <div class="stage-main">
    <div class="toolbar" id="volume3d-toolbar">
      <div class="tool-group">
        <span class="tool-label">View</span>
        <select id="flt-view">
          <option value="both" selected>Isodose + criteria</option>
          <option value="isodose">Isodose only</option>
          <option value="criteria">Criteria only</option>
        </select>
      </div>
      <div class="tool-group">
        <span class="tool-label">Min shell</span>
        <select id="flt-min-gy">
          <option value="0" selected>All shells</option>
          {gy_options}
        </select>
      </div>
      <div class="tool-group">
        <span class="tool-label">Percentile</span>
        <select id="flt-percentile">
          <option value="0" selected>Off</option>
          {pct_options}
        </select>
      </div>
      {compare_block}
    </div>
    <p id="volume3d-status">Loading 3D isodose…</p>
    <div id="volume3d-host"></div>
  </div>
  <aside class="stage-side">
    <h3>Criteria (full text)</h3>
    {criteria_panel}
    <h3>Active layers</h3>
    <ul id="layer-legend"><li style="color:var(--muted)">Waiting for plot…</li></ul>
  </aside>
</div>
</div>
<script type="application/json" id="volume3d-data">{model_json}</script>
<script type="application/json" id="volume3d-filters">{filters_json}</script>
<script>
(function () {{
  const status = document.getElementById("volume3d-status");
  const host = document.getElementById("volume3d-host");
  const legend = document.getElementById("layer-legend");
  const raw = document.getElementById("volume3d-data");
  const minGy = document.getElementById("flt-min-gy");
  const pct = document.getElementById("flt-percentile");
  const viewMode = document.getElementById("flt-view");
  const compareBoxes = () => Array.from(document.querySelectorAll(".flt-compare"));

  function metaOf(trace) {{
    const m = trace.meta;
    if (!m) return {{}};
    return Array.isArray(m) ? (m[0] || {{}}) : m;
  }}

  function criteriaOn(key) {{
    const el = document.querySelector(".flt-compare[data-criteria='" + key + "']");
    return !!(el && el.checked);
  }}

  function layerLabel(m, trace) {{
    if (m.label) return m.label;
    if (trace && trace.name) return trace.name;
    return m.kind || "layer";
  }}

  function refreshLegend(visible) {{
    const items = [];
    const seen = new Set();
    host.data.forEach((trace, i) => {{
      if (!visible[i]) return;
      const m = metaOf(trace);
      const label = layerLabel(m, trace);
      const key = (m.criteria || m.kind || "") + "|" + label;
      if (seen.has(key)) return;
      seen.add(key);
      const color = m.color || (trace.line && trace.line.color) || trace.color || "#5c6b7a";
      items.push(
        "<li><span class='swatch' style='background:" + color +
        "'></span><span>" + label + "</span></li>"
      );
    }});
    legend.innerHTML = items.length
      ? items.join("")
      : "<li style='color:var(--muted)'>No layers visible.</li>";
  }}

  function applyFilters() {{
    if (!host.data) return;
    const mode = viewMode.value;
    const floorGy = Math.max(Number(minGy.value) || 0, Number(pct.value) || 0);
    const visible = host.data.map((trace) => {{
      const m = metaOf(trace);
      const kind = m.kind || "";
      if (kind === "canister") return true;
      if (kind === "isodose") {{
        if (mode === "criteria") return false;
        return (Number(m.gy) || 0) >= floorGy;
      }}
      if (m.criteria) {{
        if (mode === "isodose") return false;
        return criteriaOn(m.criteria);
      }}
      return true;
    }});
    Plotly.restyle(host, {{ visible: visible }}, visible.map((_, i) => i));
    refreshLegend(visible);
    const activeShells = visible.filter((v, i) => metaOf(host.data[i]).kind === "isodose" && v).length;
    const overlayDrawn = visible.filter((v, i) => metaOf(host.data[i]).criteria && v).length;
    const checked = compareBoxes().filter((el) => el.checked).length;
    let msg = "View: " + mode + " · " + activeShells + " shell(s) · " +
      checked + " criteria selected · drag to rotate.";
    if (mode !== "isodose" && checked && overlayDrawn === 0) {{
      msg += " Selected criteria within bounds (nothing to paint).";
    }} else if (overlayDrawn) {{
      msg += " " + overlayDrawn + " criteria layer(s) on.";
    }}
    status.textContent = msg;
  }}

  function mount() {{
    try {{
      const fig = JSON.parse(raw.textContent);
      if (fig.layout) fig.layout.showlegend = false;
      Plotly.newPlot(host, fig.data, fig.layout, {plotly_config}).then(() => {{
        applyFilters();
        Plotly.Plots.resize(host);
      }});
      window.addEventListener("resize", () => Plotly.Plots.resize(host));
      [minGy, pct, viewMode].forEach((el) => el.addEventListener("change", applyFilters));
      compareBoxes().forEach((el) => el.addEventListener("change", applyFilters));
    }} catch (err) {{
      status.textContent = "Could not draw the 3D view: " + err;
    }}
  }}
  if (window.requestIdleCallback) {{
    requestIdleCallback(mount, {{ timeout: 1200 }});
  }} else {{
    setTimeout(mount, 50);
  }}
}})();
</script>
</body></html>
"""
    file_path.write_text(html, encoding="utf-8")


def save_slice_png(volume: DoseVolume, path: str | Path) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    figure = _matplotlib_slices(volume)
    figure.savefig(file_path, dpi=120, bbox_inches="tight")
    plt.close(figure)


def save_axial_gif(volume: DoseVolume, path: str | Path, frames: int = 24) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    indices = np.linspace(0, len(volume.z_mm) - 1, min(frames, len(volume.z_mm)), dtype=int)
    figure, axis = plt.subplots(figsize=(4.6, 4.4))
    writer = PillowWriter(fps=6)
    with writer.saving(figure, str(file_path), dpi=80):
        for index in indices:
            axis.clear()
            _draw_axial(axis, volume, int(index))
            writer.grab_frame()
    plt.close(figure)


def pyvista_cloud(volume: DoseVolume):
    """Measured-grid point cloud. Imports PyVista only when called."""

    import pyvista as pv

    mask = np.isfinite(volume.dose_gy)
    xx, yy, zz = np.meshgrid(volume.x_mm, volume.y_mm, volume.z_mm, indexing="ij")
    step = max(1, int(np.ceil(mask.sum() / 20000)))
    chosen = np.flatnonzero(mask.ravel())[::step]
    points = np.column_stack([xx.ravel()[chosen], yy.ravel()[chosen], zz.ravel()[chosen]])
    cloud = pv.PolyData(points)
    cloud["dose_gy"] = volume.dose_gy.ravel()[chosen]
    return cloud


def _isodose_figure(volume: DoseVolume, title: str) -> go.Figure:
    iz = _mid_index(volume.z_mm)
    iy = int(np.argmin(np.abs(volume.y_mm)))
    figure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            f"Axial z = {volume.z_mm[iz]:.1f} mm",
            "Coronal y = 0",
        ),
    )
    low, high = _finite_limits(volume.dose_gy)
    figure.add_trace(
        _contour_trace(
            volume.x_mm,
            volume.y_mm,
            volume.dose_gy[:, :, iz].T,
            showscale=True,
            zmin=low,
            zmax=high,
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        _contour_trace(
            volume.x_mm,
            volume.z_mm,
            volume.dose_gy[:, iy, :].T,
            showscale=False,
            zmin=low,
            zmax=high,
        ),
        row=1,
        col=2,
    )
    figure.update_layout(
        title=f"{title} — isodose",
        height=560,
        autosize=True,
        margin=dict(l=40, r=40, t=56, b=40),
    )
    figure.update_xaxes(title_text="x (mm)", scaleanchor="y", row=1, col=1)
    figure.update_yaxes(title_text="y (mm)", row=1, col=1)
    figure.update_xaxes(title_text="x (mm)", row=1, col=2)
    figure.update_yaxes(title_text="z (mm)", row=1, col=2)
    return figure


def _contour_trace(
    x_mm: np.ndarray,
    y_mm: np.ndarray,
    grid: np.ndarray,
    *,
    showscale: bool,
    zmin: float,
    zmax: float,
) -> go.Contour:
    return go.Contour(
        x=x_mm,
        y=y_mm,
        z=grid,
        zmin=zmin,
        zmax=zmax,
        contours=dict(
            start=CLINICAL_ISODOSE_GY[0],
            end=CLINICAL_ISODOSE_GY[-1],
            size=5,
            coloring="heatmap",
            showlabels=True,
            labelfont=dict(size=11, color="black"),
        ),
        line=dict(width=2, color="#1a2332"),
        colorscale=_CLINICAL_COLORSCALE,
        showscale=showscale,
        colorbar=dict(title="Gy"),
        hovertemplate="%{x:.1f} mm, %{y:.1f} mm<br>%{z:.2f} Gy<extra></extra>",
    )


def _isosurface_figure(
    volume: DoseVolume,
    title: str,
    *,
    criteria: DoseCriteria | None = None,
    max_side: int = _DEFAULT_VIEW_MAX_SIDE,
) -> tuple[go.Figure, dict]:
    xs, ys, zs, values, inside, spacing = _display_grid(volume, max_side=max_side)
    levels = clinical_isodose_levels(values)
    figure = go.Figure()
    radius_mm, z0, z1 = _canister_extents(volume)
    for trace in _canister_wireframe(radius_mm, z0, z1):
        figure.add_trace(trace)

    finite = values[np.isfinite(values)]
    filter_meta: dict = {
        "shell_levels_gy": [float(level) for level in levels],
        "percentiles": [],
        "criteria_name": criteria.name if criteria else None,
        "dmin_gy": criteria.dmin_gy if criteria else None,
        "dmax_gy": criteria.dmax_gy if criteria else None,
        "dose_min_gy": float(finite.min()) if finite.size else None,
        "dose_max_gy": float(finite.max()) if finite.size else None,
        "compare": [],
    }
    if finite.size:
        for percentile in (50, 75, 90):
            gy = float(np.percentile(finite, percentile))
            filter_meta["percentiles"].append({"percentile": percentile, "gy": round(gy, 2)})

    origin = (float(xs[0]), float(ys[0]), float(zs[0]))
    if levels and finite.size:
        filled = _continuous_dose_field(values, inside)
        volume_zyx = np.transpose(filled, (2, 1, 0))
        spacing_zyx = (spacing[2], spacing[1], spacing[0])
        mesh_ctx = (volume_zyx, spacing_zyx, origin)
        span = max(levels[-1] - levels[0], 1.0)
        for level in reversed(levels):
            mesh = _marching_mesh(*mesh_ctx, level=level)
            if mesh is None:
                continue
            x, y, z, faces = mesh
            t = (level - levels[0]) / span
            opacity = 0.22 + 0.38 * t
            color = _ISODOSE_COLOR.get(int(level), "#888888")
            figure.add_trace(
                _mesh3d_trace(
                    x,
                    y,
                    z,
                    faces,
                    color=color,
                    opacity=opacity,
                    name=f"{level:.0f} Gy",
                    legendgroup=f"iso-{level:.0f}",
                    hover=f"<b>{level:.0f} Gy</b> isodose shell",
                    meta={
                        "kind": "isodose",
                        "gy": float(level),
                        "color": color,
                        "label": f"Isodose {level:.0f} Gy",
                    },
                    visible=True,
                )
            )

    _add_compare_overlays(
        figure,
        volume,
        filter_meta,
        active=criteria,
        max_side=max_side,
        origin=origin,
        spacing=spacing,
    )

    figure.update_layout(**_scene_layout(f"{title} — 3D isodose", radius_mm, z0, z1))
    return figure, filter_meta


def _continuous_dose_field(values: np.ndarray, inside: np.ndarray) -> np.ndarray:
    """Fill hull holes inside the canister, then smooth — avoids shredded shells."""

    from scipy.ndimage import distance_transform_edt, gaussian_filter

    finite = values[np.isfinite(values)]
    sentinel = float(finite.min()) - 100.0 if finite.size else -100.0
    known = np.isfinite(values)
    filled = np.array(values, dtype=np.float64, copy=True)
    fillable = inside & ~known
    if fillable.any() and known.any():
        _, indices = distance_transform_edt(~known, return_distances=True, return_indices=True)
        filled[fillable] = values[tuple(indices[:, fillable])]
    support = inside & np.isfinite(filled)
    blurred = gaussian_filter(np.where(support, filled, 0.0), sigma=1.15)
    weight = gaussian_filter(support.astype(np.float64), sigma=1.15)
    smoothed = np.full_like(blurred, sentinel, dtype=np.float64)
    np.divide(blurred, weight, out=smoothed, where=weight > 1e-6)
    return np.where(inside, smoothed, sentinel)


def _add_compare_overlays(
    figure: go.Figure,
    volume: DoseVolume,
    filter_meta: dict,
    *,
    active: DoseCriteria | None,
    max_side: int,
    origin: tuple[float, float, float],
    spacing: tuple[float, float, float],
) -> None:
    """Precompute fail/limit meshes for each regulatory preset (toggled in UI)."""

    sx, sy, sz = _display_strides(volume, max_side=max_side)
    spacing_zyx = (spacing[2], spacing[1], spacing[0])
    dose = volume.dose_gy
    if not np.isfinite(dose).any():
        return

    dose_min = _pool_nan_reduce(dose, sx, sy, sz, mode="min")
    dose_max = _pool_nan_reduce(dose, sx, sy, sz, mode="max")
    filter_meta["dose_min_gy"] = float(np.nanmin(dose_min))
    filter_meta["dose_max_gy"] = float(np.nanmax(dose_max))
    xs = volume.x_mm[::sx]
    ys = volume.y_mm[::sy]
    zs = volume.z_mm[::sz]
    active_name = active.name if active else None

    for key, preset, low_color, high_color in _COMPARE_CRITERIA:
        short = {
            "japan": "Japan",
            "fda": "FDA/AABB",
            "bcsh": "BCSH",
            "portaria": "Portaria 158",
        }[key]
        dmin = preset.dmin_gy
        dmax = preset.dmax_gy
        rule_lines = [preset.name + "."]
        if dmin is not None:
            rule_lines.append(f"Minimum ≥ {dmin:.0f} Gy everywhere.")
        if dmax is not None:
            rule_lines.append(f"Maximum ≤ {dmax:.0f} Gy everywhere.")
        if preset.central_point_min_gy is not None:
            rule_lines.append(f"Centre point ≥ {preset.central_point_min_gy:.0f} Gy.")
        if preset.central_plane_min_gy is not None and preset.central_point_min_gy is None:
            rule_lines.append(
                f"Central plane mean ≥ {preset.central_plane_min_gy:.0f} Gy."
            )
        if preset.note:
            rule_lines.append(preset.note)
        rules = " ".join(rule_lines)
        entry = {
            "key": key,
            "label": short + (" ★" if active_name == preset.name else ""),
            "hint": rules,
            "rules": rules,
            "color": low_color,
            "has_overlay": False,
        }

        if dmin is not None and np.nanmin(dose_min) < dmin < np.nanmax(dose_max):
            mesh = _mesh_from_dose_field(dose_min, spacing, origin, level=dmin)
            if mesh is not None:
                x, y, z, faces = mesh
                figure.add_trace(
                    _mesh3d_trace(
                        x,
                        y,
                        z,
                        faces,
                        color=low_color,
                        opacity=0.3,
                        name=f"{short} limit {dmin:.0f}",
                        legendgroup=f"cmp-{key}-limit-low",
                        hover=f"<b>{preset.name}</b> dmin {dmin:.0f} Gy",
                        meta={
                            "kind": "limit_low",
                            "criteria": key,
                            "gy": float(dmin),
                            "color": low_color,
                            "label": f"{short}: limit {dmin:.0f} Gy (dmin)",
                        },
                        visible=False,
                    )
                )
                entry["has_overlay"] = True

        if dmax is not None and np.nanmin(dose_min) < dmax < np.nanmax(dose_max):
            mesh = _mesh_from_dose_field(dose_max, spacing, origin, level=dmax)
            if mesh is not None:
                x, y, z, faces = mesh
                figure.add_trace(
                    _mesh3d_trace(
                        x,
                        y,
                        z,
                        faces,
                        color=high_color,
                        opacity=0.3,
                        name=f"{short} limit {dmax:.0f}",
                        legendgroup=f"cmp-{key}-limit-high",
                        hover=f"<b>{preset.name}</b> dmax {dmax:.0f} Gy",
                        meta={
                            "kind": "limit_high",
                            "criteria": key,
                            "gy": float(dmax),
                            "color": high_color,
                            "label": f"{short}: limit {dmax:.0f} Gy (dmax)",
                        },
                        visible=False,
                    )
                )
                entry["has_overlay"] = True

        if dmin is not None:
            fail_full = np.isfinite(dose) & (dose < dmin)
            if np.any(fail_full):
                fail = _or_pool(fail_full, sx, sy, sz)
                added = _add_fail_trace(
                    figure,
                    fail,
                    xs,
                    ys,
                    zs,
                    spacing_zyx,
                    origin,
                    color=low_color,
                    name=f"{short} below {dmin:.0f} Gy",
                    legendgroup=f"cmp-{key}-fail-low",
                    hover=f"<b>{preset.name} fail</b> dose &lt; {dmin:.0f} Gy",
                    meta={
                        "kind": "fail_low",
                        "criteria": key,
                        "gy": float(dmin),
                        "color": low_color,
                        "label": f"{short}: below {dmin:.0f} Gy (fail dmin)",
                    },
                )
                entry["has_overlay"] = entry["has_overlay"] or added

        if dmax is not None:
            fail_full = np.isfinite(dose) & (dose > dmax)
            if np.any(fail_full):
                fail = _or_pool(fail_full, sx, sy, sz)
                added = _add_fail_trace(
                    figure,
                    fail,
                    xs,
                    ys,
                    zs,
                    spacing_zyx,
                    origin,
                    color=high_color,
                    name=f"{short} above {dmax:.0f} Gy",
                    legendgroup=f"cmp-{key}-fail-high",
                    hover=f"<b>{preset.name} fail</b> dose &gt; {dmax:.0f} Gy",
                    meta={
                        "kind": "fail_high",
                        "criteria": key,
                        "gy": float(dmax),
                        "color": high_color,
                        "label": f"{short}: above {dmax:.0f} Gy (fail dmax)",
                    },
                )
                entry["has_overlay"] = entry["has_overlay"] or added

        # Centre / central-plane rules (FDA, Portaria): highlight dose below the target.
        centre = preset.central_point_min_gy
        if centre is None:
            centre = preset.central_plane_min_gy
        if centre is not None and np.any(np.isfinite(dose) & (dose < centre)):
            if np.nanmin(dose_min) < centre < np.nanmax(dose_max):
                mesh = _mesh_from_dose_field(dose_min, spacing, origin, level=centre)
                if mesh is not None:
                    x, y, z, faces = mesh
                    figure.add_trace(
                        _mesh3d_trace(
                            x,
                            y,
                            z,
                            faces,
                            color=low_color,
                            opacity=0.28,
                            name=f"{short} centre {centre:.0f}",
                            legendgroup=f"cmp-{key}-centre",
                            hover=f"<b>{preset.name}</b> centre/plane {centre:.0f} Gy",
                            meta={
                                "kind": "centre_limit",
                                "criteria": key,
                                "gy": float(centre),
                                "color": low_color,
                                "label": f"{short}: centre/plane limit {centre:.0f} Gy",
                            },
                            visible=False,
                        )
                    )
                    entry["has_overlay"] = True
            fail = _or_pool(np.isfinite(dose) & (dose < centre), sx, sy, sz)
            added = _add_fail_trace(
                figure,
                fail,
                xs,
                ys,
                zs,
                spacing_zyx,
                origin,
                color=low_color,
                name=f"{short} below centre {centre:.0f}",
                legendgroup=f"cmp-{key}-centre-fail",
                hover=f"<b>{preset.name}</b> dose &lt; {centre:.0f} Gy (centre rule)",
                meta={
                    "kind": "centre_low",
                    "criteria": key,
                    "gy": float(centre),
                    "color": low_color,
                    "label": f"{short}: below {centre:.0f} Gy (centre rule)",
                },
            )
            entry["has_overlay"] = entry["has_overlay"] or added

        filter_meta["compare"].append(entry)


def _marching_mesh(
    volume_zyx: np.ndarray,
    spacing_zyx: tuple[float, float, float],
    origin: tuple[float, float, float],
    *,
    level: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
    try:
        verts_zyx, faces, *_ = marching_cubes(
            volume_zyx,
            level=level,
            spacing=spacing_zyx,
            allow_degenerate=False,
        )
    except ValueError:
        return None
    if verts_zyx.size == 0 or faces.size == 0:
        return None
    x = verts_zyx[:, 2] + origin[0]
    y = verts_zyx[:, 1] + origin[1]
    z = verts_zyx[:, 0] + origin[2]
    return x, y, z, faces


def _mask_surface(
    fail_mask: np.ndarray,
    spacing_zyx: tuple[float, float, float],
    origin: tuple[float, float, float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
    """Outer surface of a boolean fail region (dose outside criteria)."""

    from scipy.ndimage import binary_dilation, gaussian_filter

    if not np.any(fail_mask):
        return None
    dilated = binary_dilation(fail_mask, iterations=1)
    field = gaussian_filter(dilated.astype(np.float64), sigma=0.55)
    field_zyx = np.transpose(field, (2, 1, 0))
    peak = float(field_zyx.max())
    if peak < 0.2:
        return None
    level = min(0.35, 0.45 * peak)
    return _marching_mesh(field_zyx, spacing_zyx, origin, level=level)


def _add_fail_trace(
    figure: go.Figure,
    fail: np.ndarray,
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    spacing_zyx: tuple[float, float, float],
    origin: tuple[float, float, float],
    *,
    color: str,
    name: str,
    legendgroup: str,
    hover: str,
    meta: dict,
) -> bool:
    """Prefer a fail Mesh3d; fall back to markers when the region is sparse."""

    surface = _mask_surface(fail, spacing_zyx, origin)
    if surface is not None:
        x, y, z, faces = surface
        figure.add_trace(
            _mesh3d_trace(
                x,
                y,
                z,
                faces,
                color=color,
                opacity=0.55,
                name=name,
                legendgroup=legendgroup,
                hover=hover,
                meta=meta,
                visible=False,
            )
        )
        return True
    ii, jj, kk = np.where(fail)
    if ii.size == 0:
        return False
    figure.add_trace(
        go.Scatter3d(
            x=xs[ii],
            y=ys[jj],
            z=zs[kk],
            mode="markers",
            marker=dict(size=5, color=color, opacity=0.9),
            name=name,
            legendgroup=legendgroup,
            hovertemplate=hover + "<extra></extra>",
            meta={**meta, "color": color, "label": meta.get("label") or name},
            visible=False,
            showlegend=False,
        )
    )
    return True


def _mesh3d_trace(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    faces: np.ndarray,
    *,
    color: str,
    opacity: float,
    name: str,
    legendgroup: str,
    hover: str,
    meta: dict,
    visible: bool,
) -> go.Mesh3d:
    return go.Mesh3d(
        x=x,
        y=y,
        z=z,
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        color=color,
        opacity=float(opacity),
        flatshading=False,
        name=name,
        legendgroup=legendgroup,
        hovertemplate=hover + "<extra></extra>",
        lighting=_MESH_LIGHTING,
        lightposition=dict(x=140, y=60, z=240),
        meta=meta,
        visible=visible,
        showlegend=False,
    )


def _canister_extents(volume: DoseVolume) -> tuple[float, float, float]:
    radius = min(
        abs(float(volume.x_mm[0])),
        abs(float(volume.x_mm[-1])),
        abs(float(volume.y_mm[0])),
        abs(float(volume.y_mm[-1])),
    )
    return radius, float(volume.z_mm[0]), float(volume.z_mm[-1])


def _canister_wireframe(radius_mm: float, z0: float, z1: float) -> list[go.Scatter3d]:
    """Thin steel-gray cage so nested shells read against the canister wall."""

    theta = np.linspace(0.0, 2.0 * np.pi, 65)
    cx = radius_mm * np.cos(theta)
    cy = radius_mm * np.sin(theta)
    traces: list[go.Scatter3d] = []
    meta = {"kind": "canister"}
    common = dict(
        mode="lines",
        line=dict(color=_CANISTER_LINE, width=2.5),
        opacity=0.85,
        hoverinfo="skip",
        showlegend=False,
        legendgroup="canister",
        meta=meta,
    )
    for z in (z0, 0.5 * (z0 + z1), z1):
        traces.append(go.Scatter3d(x=cx, y=cy, z=np.full_like(cx, z), **common))
    for angle in np.linspace(0.0, 2.0 * np.pi, 8, endpoint=False):
        x = [radius_mm * np.cos(angle)] * 2
        y = [radius_mm * np.sin(angle)] * 2
        traces.append(go.Scatter3d(x=x, y=y, z=[z0, z1], **common))
    for angle in np.linspace(0.0, 2.0 * np.pi, 4, endpoint=False):
        traces.append(
            go.Scatter3d(
                x=[0.0, radius_mm * np.cos(angle)],
                y=[0.0, radius_mm * np.sin(angle)],
                z=[z0, z0],
                mode="lines",
                line=dict(color=_CANISTER_LINE, width=1.5),
                opacity=0.45,
                hoverinfo="skip",
                showlegend=False,
                legendgroup="canister",
                meta=meta,
            )
        )
    traces[0].meta = {"kind": "canister", "color": _CANISTER_LINE, "label": "Canister wall"}
    traces[0].name = "Canister wall"
    return traces


def _scene_layout(title: str, radius_mm: float, z0: float, z1: float) -> dict:
    pad = radius_mm * 0.08
    axis = dict(
        backgroundcolor=_SCENE_BG,
        gridcolor=_AXIS_GRID,
        zerolinecolor="#9aa8b5",
        showbackground=True,
        showspikes=False,
        title_font=dict(size=12, color="#3d4a5c"),
        tickfont=dict(size=10, color="#5a6778"),
    )
    return dict(
        title=dict(text=title, font=dict(size=16, color="#1a2332"), x=0.01, xanchor="left"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=_SCENE_BG,
        font=dict(family="Source Sans 3, Segoe UI, sans-serif", color="#1a2332"),
        autosize=True,
        showlegend=False,
        scene=dict(
            bgcolor=_SCENE_BG,
            xaxis=dict(**axis, title="x (mm)", range=[-radius_mm - pad, radius_mm + pad]),
            yaxis=dict(**axis, title="y (mm)", range=[-radius_mm - pad, radius_mm + pad]),
            zaxis=dict(**axis, title="z (mm)", range=[z0 - pad, z1 + pad]),
            aspectmode="data",
            camera=dict(
                eye=dict(x=1.55, y=1.35, z=0.85),
                up=dict(x=0.0, y=0.0, z=1.0),
                center=dict(x=0.0, y=0.0, z=-0.05),
            ),
        ),
        height=820,
        margin=dict(l=10, r=10, t=48, b=10),
        uirevision="dose3d",
    )


def _display_strides(volume: DoseVolume, *, max_side: int) -> tuple[int, int, int]:
    if max_side < 8:
        raise ValueError("max_side must be at least 8.")

    def stride_for(length: int) -> int:
        return max(1, int(np.ceil(length / max_side)))

    return (
        stride_for(len(volume.x_mm)),
        stride_for(len(volume.y_mm)),
        stride_for(len(volume.z_mm)),
    )


def _display_grid(
    volume: DoseVolume,
    *,
    max_side: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, tuple[float, float, float]]:
    """Downsample the reconstructed volume for interactive 3D display.

    Each axis is strided on its own so a tall canister does not starve x/y.
    Returns ``inside`` so hull holes can be filled before marching cubes.
    """

    sx, sy, sz = _display_strides(volume, max_side=max_side)
    xs = volume.x_mm[::sx]
    ys = volume.y_mm[::sy]
    zs = volume.z_mm[::sz]
    values = volume.dose_gy[::sx, ::sy, ::sz]
    inside = volume.inside[::sx, ::sy, ::sz]
    spacing = (
        float(xs[1] - xs[0]) if len(xs) > 1 else float(volume.spacing_mm[0]),
        float(ys[1] - ys[0]) if len(ys) > 1 else float(volume.spacing_mm[1]),
        float(zs[1] - zs[0]) if len(zs) > 1 else float(volume.spacing_mm[2]),
    )
    return xs, ys, zs, values, inside, spacing


def _pool_nan_reduce(
    dose: np.ndarray,
    sx: int,
    sy: int,
    sz: int,
    *,
    mode: str,
) -> np.ndarray:
    """Block-reduce dose so cold/hot extrema survive display downsampling."""

    reduce = np.nanmin if mode == "min" else np.nanmax
    nx, ny, nz = dose.shape
    out = np.full(
        ((nx + sx - 1) // sx, (ny + sy - 1) // sy, (nz + sz - 1) // sz),
        np.nan,
        dtype=float,
    )
    for ix in range(out.shape[0]):
        for iy in range(out.shape[1]):
            for iz in range(out.shape[2]):
                block = dose[
                    ix * sx : min((ix + 1) * sx, nx),
                    iy * sy : min((iy + 1) * sy, ny),
                    iz * sz : min((iz + 1) * sz, nz),
                ]
                if np.isfinite(block).any():
                    out[ix, iy, iz] = float(reduce(block))
    return out


def _or_pool(mask: np.ndarray, sx: int, sy: int, sz: int) -> np.ndarray:
    nx, ny, nz = mask.shape
    out = np.zeros(
        ((nx + sx - 1) // sx, (ny + sy - 1) // sy, (nz + sz - 1) // sz),
        dtype=bool,
    )
    for ix in range(out.shape[0]):
        for iy in range(out.shape[1]):
            for iz in range(out.shape[2]):
                block = mask[
                    ix * sx : min((ix + 1) * sx, nx),
                    iy * sy : min((iy + 1) * sy, ny),
                    iz * sz : min((iz + 1) * sz, nz),
                ]
                out[ix, iy, iz] = bool(np.any(block))
    return out


def _mesh_from_dose_field(
    dose_xyz: np.ndarray,
    spacing: tuple[float, float, float],
    origin: tuple[float, float, float],
    *,
    level: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
    finite = np.isfinite(dose_xyz)
    if not finite.any():
        return None
    # Treat finite voxels as the support region for limit surfaces.
    filled = _continuous_dose_field(dose_xyz, finite)
    volume_zyx = np.transpose(filled, (2, 1, 0))
    spacing_zyx = (spacing[2], spacing[1], spacing[0])
    return _marching_mesh(volume_zyx, spacing_zyx, origin, level=level)


def _matplotlib_slices(volume: DoseVolume):
    iz = int(np.argmin(np.abs(volume.z_mm - 0.5 * (volume.z_mm[0] + volume.z_mm[-1]))))
    iy = int(np.argmin(np.abs(volume.y_mm)))
    figure, axes = plt.subplots(1, 2, figsize=(9.2, 4.2))
    _draw_axial(axes[0], volume, iz)
    coronal = np.ma.masked_invalid(volume.dose_gy[:, iy, :].T)
    image = axes[1].imshow(
        coronal,
        origin="lower",
        extent=[volume.x_mm[0], volume.x_mm[-1], volume.z_mm[0], volume.z_mm[-1]],
        aspect="auto",
        cmap="viridis",
    )
    axes[1].set_title("Coronal y = 0")
    axes[1].set_xlabel("x (mm)")
    axes[1].set_ylabel("z (mm)")
    figure.colorbar(image, ax=axes, fraction=0.046, pad=0.04, label="Dose (Gy)")
    _draw_contours(axes[1], volume.x_mm, volume.z_mm, coronal)
    figure.suptitle("Isodose inside the canister")
    return figure


def _draw_axial(axis, volume: DoseVolume, index: int) -> None:
    axial = np.ma.masked_invalid(volume.dose_gy[:, :, index].T)
    image = axis.imshow(
        axial,
        origin="lower",
        extent=[volume.x_mm[0], volume.x_mm[-1], volume.y_mm[0], volume.y_mm[-1]],
        cmap="viridis",
    )
    radius = min(abs(volume.x_mm[0]), abs(volume.x_mm[-1]))
    circle = plt.Circle((0, 0), radius, fill=False, color="black", linewidth=0.8)
    axis.add_patch(circle)
    axis.set_aspect("equal")
    axis.set_title(f"Axial z = {volume.z_mm[index]:.1f} mm")
    axis.set_xlabel("x (mm)")
    axis.set_ylabel("y (mm)")
    image.set_clim(np.nanmin(volume.dose_gy), np.nanmax(volume.dose_gy))
    _draw_contours(axis, volume.x_mm, volume.y_mm, axial)


def _draw_contours(axis, x_mm: np.ndarray, y_mm: np.ndarray, grid: np.ndarray) -> None:
    levels = clinical_isodose_levels(grid)
    if not levels or not np.isfinite(grid).any():
        return
    curves = axis.contour(
        x_mm,
        y_mm,
        np.ma.masked_invalid(grid),
        levels=levels,
        colors="black",
        linewidths=0.8,
    )
    axis.clabel(curves, inline=True, fontsize=7, fmt=lambda value: f"{value:.0f} Gy")


def _mid_index(axis: np.ndarray) -> int:
    middle = 0.5 * (float(axis[0]) + float(axis[-1]))
    return int(np.argmin(np.abs(axis - middle)))
