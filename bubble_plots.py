"""
Bubble plot for speaker-count distributions.


bubbles are drawn as matplotlib Circle patches in data coordinates, and
row positions are computed from bubble diameters. This avoids overlap.

Input:
    speaker_counts: list[int]
        One speaker-count value per chunk/session.
"""

from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patheffects as pe


def plot_speaker_count_bubbles(
    speaker_counts,
    title="Distribution of Speakers",
    xlabel="",
    ylabel="Number of Total Speakers in FD and CAPCOM channels",
    color="per_row",
    label_bubbles=True,
):
    """
    Plot a horizontal bubble-stack distribution of speaker counts.

    Args:
        speaker_counts:
            List of integer speaker counts, one per chunk/session.
        title:
            Plot title.
        xlabel:
            X-axis label. The original figure often hides x ticks/labels.
        ylabel:
            Y-axis label.
        color:
            "per_row" for colormap by speaker count, or a matplotlib color.
        label_bubbles:
            Whether to write the speaker count inside each bubble.

    Returns:
        fig, ax
    """
    if not speaker_counts:
        raise ValueError("speaker_counts cannot be empty.")

    counts = Counter(int(value) for value in speaker_counts)
    ks = np.array(sorted(counts.keys()), dtype=int)
    ns = np.array([counts[k] for k in ks], dtype=int)


    colormap_name = "turbo"
    diam_min = 0.7
    diam_max = 2.2
    size_gamma = 1.15
    row_gap = 0.06
    bubble_gap = 0.02
    label_fs_min = 8
    label_fs_max = 20

    if color == "per_row":
        cmap = plt.colormaps.get_cmap(colormap_name)
        t = (ks - ks.min()) / max(1e-12, (ks.max() - ks.min()))
        row_colors = [cmap(value) for value in t]
    else:
        row_colors = [color] * len(ks)

    if ks.min() == ks.max():
        diams = np.full_like(ks, (diam_min + diam_max) / 2.0, dtype=float)
    else:
        t = (ks - ks.min()) / (ks.max() - ks.min())
        t = np.power(t, size_gamma)
        diams = diam_min + t * (diam_max - diam_min)

    radii = diams / 2.0

    denom = max(1e-12, diams.max() - diams.min())
    row_fontsizes = label_fs_min + (diams - diams.min()) * (label_fs_max - label_fs_min) / denom

    # Compute row centers based on actual bubble diameters.
    y_centers = np.zeros_like(diams, dtype=float)
    y_centers[0] = 0.0
    for index in range(1, len(diams)):
        y_centers[index] = (
            y_centers[index - 1]
            + 0.5 * diams[index - 1]
            + 0.5 * diams[index]
            + row_gap
        )

    x_list = []
    y_list = []
    k_list = []
    color_list = []
    radius_list = []
    fontsize_list = []
    row_widths = []

    for y0, k, n, radius, row_color, fontsize in zip(
        y_centers, ks, ns, radii, row_colors, row_fontsizes
    ):
        centers_x = radius + np.arange(n) * (2 * radius + bubble_gap)

        x_list.extend(centers_x.tolist())
        y_list.extend([y0] * n)
        k_list.extend([k] * n)
        color_list.extend([row_color] * n)
        radius_list.extend([radius] * n)
        fontsize_list.extend([float(fontsize)] * n)

        row_widths.append(centers_x[-1] + radius)

    fig_width = max(16.0, max(row_widths) * 0.38)
    fig_height = max(6.5, y_centers[-1] * 0.22 + 1.5)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_aspect("equal")
    ax.set_facecolor("#f7f7f7")

    for x, y, k, row_color, radius, fontsize in zip(
        x_list, y_list, k_list, color_list, radius_list, fontsize_list
    ):
        circle = Circle(
            (x, y),
            radius,
            facecolor=row_color,
            edgecolor="black",
            linewidth=0.35,
            alpha=0.95,
        )
        ax.add_patch(circle)

        if label_bubbles:
            text_color = "black" if 7 <= int(k) <= 24 else "white"
            ax.text(
                x,
                y,
                str(k),
                ha="center",
                va="center",
                fontsize=fontsize,
                color=text_color,
                path_effects=[
                    pe.withStroke(
                        linewidth=1.0,
                        foreground="white" if text_color == "black" else "black",
                    )
                ],
            )

    tick_values_y = np.arange(int(ks.min()), int(ks.max()) + 1, 5)
    tick_positions_y = []
    tick_labels_y = []

    for tick_value in tick_values_y:
        match = np.where(ks == tick_value)[0]
        if len(match) > 0:
            tick_positions_y.append(y_centers[match[0]])
            tick_labels_y.append(str(tick_value))

    ax.set_yticks(tick_positions_y)
    ax.set_yticklabels(tick_labels_y)

    ax.set_xlim(-0.5, max(row_widths) + 0.5)
    ax.set_ylim(y_centers[0] - diams[0] / 2.0 - 0.25, y_centers[-1] + diams[-1] / 2.0 + 0.25)


    if xlabel:
        ax.set_xlabel(xlabel, fontsize=18)
    else:
        ax.set_xticks([])
        ax.set_xlabel("")

    ax.set_ylabel(ylabel, fontsize=18)
    ax.set_title(title, fontsize=20)
    ax.grid(axis="x", linestyle=":", alpha=0.25)
    ax.tick_params(axis="both", labelsize=12)

    fig.tight_layout()
    return fig, ax
