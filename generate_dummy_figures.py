"""
Generate dummy data and demo figures for the speaker analysis plotting scripts.

This script imports the plotting functions from:
    bubble_plots.py
    cross_mission.py
    cross_mission_speaker_specific.py
    donut_plots.py

It creates synthetic data shaped to resemble the original analysis figures:
    - horizontal bubble speaker distributions
    - cross-mission sparse/spiky activity trajectories
    - speaker-specific cross-mission trajectories
    - dense speaker-turn donut plots
"""

from pathlib import Path
import random
import json

from bubble_plots import plot_speaker_count_bubbles
from cross_mission import plot_cross_mission_activity
from cross_mission_speaker_specific import plot_speaker_cross_mission_activity
from donut_plots import plot_speaker_turn_donut


def make_dummy_speaker_counts(seed=7):
    """
    Create speaker-count values that resemble a dense horizontal bubble plot.
    """
    rng = random.Random(seed)
    counts = []

    for speaker_count in range(3, 36):
        center = 13
        spread = 10
        base = int(42 * max(0.08, 1 - abs(speaker_count - center) / spread))

        if speaker_count > 22:
            base = int(base * 0.45)
        if speaker_count > 28:
            base = int(base * 0.25)

        n = max(1, base + rng.randint(-4, 5))
        counts.extend([speaker_count] * n)

    return counts


def make_dummy_cross_mission_activity(seed=11):
    """
    Create sparse cross-mission activity curves with occasional spikes.
    """
    rng = random.Random(seed)
    days = [1 + i * 0.25 for i in range(56)]

    activity = {
        "Apollo 11": [],
        "Apollo 16": [],
        "Apollo 17": [],
    }

    for mission in activity:
        for day in days:
            base = rng.choice([0, 20, 40, 60, 80, 120])
            if rng.random() < 0.18:
                base += rng.randint(250, 650)

            if mission == "Apollo 17" and day > 9 and rng.random() < 0.25:
                base += rng.randint(300, 900)

            if mission == "Apollo 17" and 13.0 < day < 14.0:
                base += rng.randint(1800, 3000)

            activity[mission].append((day, base))

    return activity


def make_dummy_speaker_activity(seed=17):
    """
    Create speaker-specific activity curves with larger sparse spikes.
    """
    rng = random.Random(seed)
    days = [1 + i * 0.25 for i in range(56)]

    activity = {
        "Apollo 11": [],
        "Apollo 16": [],
        "Apollo 17": [],
    }

    for mission in activity:
        for day in days:
            value = rng.choice([0, 10, 30, 50, 70])

            if rng.random() < 0.15:
                value += rng.randint(120, 500)

            if mission == "Apollo 17" and day > 9:
                value += rng.choice([0, 40, 90, 150])

            if mission == "Apollo 17" and 13.0 < day < 14.0:
                value += rng.randint(1800, 3000)

            activity[mission].append((day, value))

    return activity


def make_dummy_turns(seed=23, n_turns=220):
    """
    Create dense sequential speaker-turn data for donut plots.
    """
    rng = random.Random(seed)
    turns = []

    for _ in range(n_turns):
        role = rng.choices(
            ["primary", "secondary", "silence"],
            weights=[0.22, 0.33, 0.45],
            k=1,
        )[0]

        if role == "primary":
            duration = rng.uniform(2.0, 9.0)
        elif role == "secondary":
            duration = rng.uniform(1.0, 6.5)
        else:
            duration = rng.uniform(2.0, 12.0)

        turns.append({"role": role, "duration": round(duration, 2)})

    return turns


def main():
    output_dir = Path("figures")
    output_dir.mkdir(exist_ok=True)

    speaker_counts = make_dummy_speaker_counts()
    cross_mission_activity = make_dummy_cross_mission_activity()
    speaker_activity = make_dummy_speaker_activity()
    turns = make_dummy_turns()

    fig, _ = plot_speaker_count_bubbles(
        speaker_counts,
        title="Distribution of Speakers: Demo Mission",
        xlabel="Chunks / Sessions",
        ylabel="Total Speakers in FD and CAPCOM Channels",
    )
    fig.savefig(output_dir / "bubble_speaker_distribution.png", dpi=300)

    fig, _ = plot_cross_mission_activity(
        cross_mission_activity,
        title="Cross Mission Analysis: Speaker Activity across Apollo 11, Apollo 16, and Apollo 17",
        y_max=3300,
    )
    fig.savefig(output_dir / "cross_mission_activity.png", dpi=300)

    fig, _ = plot_speaker_cross_mission_activity(
        speaker_activity,
        speaker_name="Charles Duke",
        title="Cross Mission Analysis: Speaker Charles Duke across Apollo 11, Apollo 16, and Apollo 17",
        y_max=3300,
    )
    fig.savefig(output_dir / "cross_mission_speaker_specific.png", dpi=300)

    fig, _ = plot_speaker_turn_donut(
        turns,
        title="Speaker-Turn Composition Demo",
    )
    fig.savefig(output_dir / "speaker_turn_donut.png", dpi=300)

    with open("dummy_data.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "speaker_counts": speaker_counts,
                "cross_mission_activity": cross_mission_activity,
                "speaker_activity": speaker_activity,
                "turns": turns,
            },
            file,
            indent=2,
        )


if __name__ == "__main__":
    main()
