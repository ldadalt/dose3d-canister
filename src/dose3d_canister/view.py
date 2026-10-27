"""Slice, isodose and sweep figures.

Interactive files use Plotly. The GIF and PDF images use Matplotlib so a
README preview does not need a display.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.animation import PillowWriter
from plotly.subplots import make_subplots

from dose3d_canister.interpolate import DoseVolume


def write_html(volume: DoseVolume, path: str | Path, title: str) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    slices = _slice_figure(volume, title)
    iso = _isosurface_figure(volume, title)
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title></head><body>"
        f"<h1>{title}</h1>"
        "<p>Interpolated nodes only. Empty regions were outside the sample hull "
        "or outside the canister. The surface is not a measurement.</p>"
        + slices.to_html(full_html=False, include_plotlyjs="cdn")
        + iso.to_html(full_html=False, include_plotlyjs=False)
        + "</body></html>"
    )
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


def _slice_figure(volume: DoseVolume, title: str) -> go.Figure:
    iz = int(np.argmin(np.abs(volume.z_mm - 0.5 * (volume.z_mm[0] + volume.z_mm[-1]))))
    iy = int(np.argmin(np.abs(volume.y_mm)))
    axial = volume.dose_gy[:, :, iz].T
    coronal = volume.dose_gy[:, iy, :].T
    figure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            f"Axial z = {volume.z_mm[iz]:.1f} mm",
            "Coronal y = 0",
        ),
    )
    color = dict(colorscale="Viridis", colorbar=dict(title="Gy", x=1.02))
    figure.add_trace(
        go.Heatmap(
            x=volume.x_mm,
            y=volume.y_mm,
            z=axial,
            **color,
            hovertemplate="x=%{x:.1f} mm<br>y=%{y:.1f} mm<br>%{z:.2f} Gy<extra></extra>",
        ),
        row=1,
        col=1,
    )
    figure.add_trace(
        go.Heatmap(
            x=volume.x_mm,
            y=volume.z_mm,
            z=coronal,
            colorscale="Viridis",
            showscale=False,
            hovertemplate="x=%{x:.1f} mm<br>z=%{y:.1f} mm<br>%{z:.2f} Gy<extra></extra>",
        ),
        row=1,
        col=2,
    )
    figure.update_layout(title=title, height=520, width=980)
    figure.update_xaxes(title_text="x (mm)", scaleanchor="y", row=1, col=1)
    figure.update_yaxes(title_text="y (mm)", row=1, col=1)
    figure.update_xaxes(title_text="x (mm)", row=1, col=2)
    figure.update_yaxes(title_text="z (mm)", row=1, col=2)
    return figure


def _isosurface_figure(volume: DoseVolume, title: str) -> go.Figure:
    stride = max(1, int(np.ceil(max(volume.dose_gy.shape) / 40)))
    xs = volume.x_mm[::stride]
    ys = volume.y_mm[::stride]
    zs = volume.z_mm[::stride]
    values = volume.dose_gy[::stride, ::stride, ::stride]
    finite = values[np.isfinite(values)]
    if finite.size == 0:
        return go.Figure()
    low = float(np.nanmin(finite))
    high = float(np.nanmax(finite))
    filled = np.where(np.isfinite(values), values, low)
    xx, yy, zz = np.meshgrid(xs, ys, zs, indexing="ij")
    levels = _isodose_levels(low, high)
    figure = go.Figure(
        data=go.Isosurface(
            x=xx.ravel(),
            y=yy.ravel(),
            z=zz.ravel(),
            value=filled.ravel(),
            isomin=levels[0],
            isomax=levels[-1],
            surface_count=len(levels),
            colorscale="Viridis",
            caps=dict(x_show=False, y_show=False, z_show=False),
            colorbar=dict(title="Gy"),
        )
    )
    figure.update_layout(
        title=f"{title} — isodose surfaces",
        scene=dict(
            xaxis_title="x (mm)",
            yaxis_title="y (mm)",
            zaxis_title="z (mm)",
            aspectmode="data",
        ),
        height=640,
    )
    return figure


def _isodose_levels(low: float, high: float) -> list[float]:
    if high <= low:
        return [low]
    span = high - low
    raw = [low + 0.2 * span, low + 0.5 * span, low + 0.8 * span]
    return raw


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
    figure.suptitle("Interpolated dose inside the canister")
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
