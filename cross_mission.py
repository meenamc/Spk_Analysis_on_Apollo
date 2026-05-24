"""
Cross-mission speech activity plot.

This module expects binned activity values.

Input format:
    mission_activity = {
        "Apollo 11": [(day, speech_seconds), ...],
        "Apollo 16": [(day, speech_seconds), ...],
        "Apollo 17": [(day, speech_seconds), ...],
    }
"""

import matplotlib.pyplot as plt


def plot_cross_mission_activity(
    mission_activity,
    title="Cross Mission Analysis",
    xlabel="Day across multiple Missions",
    ylabel="Speech in Seconds",
    y_max=None,
):
    """
    Plot speech activity across multiple missions.

    Args:
        mission_activity:
            Dictionary mapping mission label to ordered (x, y) points.
        title:
            Plot title.
        xlabel:
            X-axis label.
        ylabel:
            Y-axis label.
        y_max:
            Optional upper y-axis limit.

    Returns:
        fig, ax
    """
    if not mission_activity:
        raise ValueError("mission_activity cannot be empty.")

    line_styles = ["-.", "--", "-"]

    fig, ax = plt.subplots(figsize=(13, 6))

    max_day = 0
    for index, (mission, points) in enumerate(mission_activity.items()):
        if not points:
            continue

        x_values, y_values = zip(*points)
        max_day = max(max_day, max(x_values))

        ax.plot(
            x_values,
            y_values,
            linestyle=line_styles[index % len(line_styles)],
            linewidth=2,
            label=mission,
        )

    ax.set_title(title, fontsize=18)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)

    if y_max is not None:
        ax.set_ylim(0, y_max)

    day_ticks = list(range(1, int(max_day) + 2))
    ax.set_xticks(day_ticks)
    ax.set_xticklabels([f"Day {day}" for day in day_ticks])

    ax.grid(alpha=0.25)
    ax.legend(loc="upper left", frameon=True, fontsize=11)

    fig.tight_layout()
    return fig, ax
