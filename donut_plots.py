"""
Speaker-turn donut plots.

This module expects preprocessed speaker turns.

Each turn is represented as one wedge. Roles should already be assigned:
    primary
    secondary
    silence

Input format:
    turns = [
        {"role": "primary", "duration": 12.0},
        {"role": "secondary", "duration": 5.0},
        {"role": "silence", "duration": 20.0},
        ...
    ]
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


DEFAULT_COLORS = {
    "primary": "#2f7d32",
    "secondary": "#f39a1e",
    "silence": "#c979d0",
}


def _value(record, key, default=None):
    if isinstance(record, dict):
        return record.get(key, default)
    return getattr(record, key, default)


def plot_speaker_turn_donut(
    turns,
    title="Speaker-turn composition",
    role_key="role",
    duration_key="duration",
    role_colors=None,
    width=0.32,
):
    """
    Plot a donut where each wedge is a sequential speaker turn.

    Args:
        turns:
            List of turn records with role and duration.
        title:
            Plot title.
        role_key:
            Key for the role field.
        duration_key:
            Key for the duration field.
        role_colors:
            Optional dictionary mapping role to color.
        width:
            Donut ring width.

    Returns:
        fig, ax
    """
    if not turns:
        raise ValueError("turns cannot be empty.")

    role_colors = role_colors or DEFAULT_COLORS

    durations = []
    colors = []
    roles_in_plot = []

    for turn in turns:
        role = _value(turn, role_key)
        duration = _value(turn, duration_key)

        if role is None or duration is None:
            continue

        duration = float(duration)
        if duration <= 0:
            continue

        role = str(role)
        durations.append(duration)
        colors.append(role_colors.get(role, "gray"))
        roles_in_plot.append(role)

    if not durations:
        raise ValueError("No positive-duration turns were found.")

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.pie(
        durations,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={
            "width": width,
            "edgecolor": "white",
            "linewidth": 0.25,
        },
    )

    legend_roles = [role for role in ("silence", "secondary", "primary") if role in set(roles_in_plot)]
    legend_handles = [
        Patch(facecolor=role_colors.get(role, "gray"), label=role.title())
        for role in legend_roles
    ]

    ax.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=2,
        frameon=False,
    )

    ax.set_title(title, fontsize=14)
    ax.set_aspect("equal")

    fig.tight_layout()
    return fig, ax
