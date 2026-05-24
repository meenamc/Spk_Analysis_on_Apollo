# Speaker Activity Analysis

This repository contains plotting utilities for visualizing speaker-role activity. This makes the figures reusable for any dataset that provides speaker counts, mission/session activity curves, speaker-specific activity curves, or ordered speaker-turns.

## Repository Structure

```text
.
├── bubble_plots.py
├── cross_mission.py
├── cross_mission_speaker_specific.py
├── donut_plots.py
├── generate_dummy_figures.py
├── dummy_data.json
└── figures/
```

## Plot Descriptions

### 1. Speaker-count bubble plot

`bubble_plots.py` visualizes how many distinct speakers appear in each chunk or session. Each bubble represents one chunk/session (30 minutes), and the y-axis corresponds to the number of speakers detected in that chunk. Rows with many bubbles indicate that many chunks have that speaker count.

This plot is useful for understanding speaker-density patterns across a corpus. For example, it can show whether most chunks contain only a few active speakers or whether many chunks involve dense multi-speaker interaction. In mission-control audio, this helps summarize how crowded or sparse the communication environment is across processed segments.

Input format:

```python
speaker_counts = [4, 6, 6, 8, 12, 15, 15, 18]
```

Usage:

```python
from bubble_plots import plot_speaker_count_bubbles

fig, ax = plot_speaker_count_bubbles(speaker_counts)
```

Generated demo figure:

```text
figures/bubble_speaker_distribution.png
```

### 2. Cross-mission activity plot

`cross_mission.py` compares total speech activity across multiple missions. Each line represents one mission/session, and each point represents the amount of speech activity within a time bin.

This plot is useful for comparing communication intensity over time. Peaks indicate periods of increased speech activity, while low regions indicate quieter intervals. In Apollo-style mission analysis, this type of figure can highlight mission phases where communication becomes more active, such as operational events, coordination periods, or high-workload intervals.

Input format:

```python
mission_activity = {
    "Apollo 11": [(1.0, 120), (1.25, 180), (1.5, 90)],
    "Apollo 16": [(1.0, 100), (1.25, 160), (1.5, 130)],
}
```

Usage:

```python
from cross_mission import plot_cross_mission_activity

fig, ax = plot_cross_mission_activity(mission_activity)
```

Generated demo figure:

```text
figures/cross_mission_activity.png
```

### 3. Speaker-specific cross-mission activity plot

`cross_mission_speaker_specific.py` tracks the activity of one selected speaker across multiple missions or sessions. Each line represents a mission/session, and each point represents the selected speaker's duration within a time bin.

This plot is useful for analyzing how the role or participation of a particular speaker changes over time. It can be used to compare whether a speaker is consistently active, concentrated around specific mission phases, or unusually active in one mission compared with another. In speaker-role analysis, this is helpful for studying primary communicators, mission specialists, or recurring roles across sessions.

Input format:

```python
speaker_activity = {
    "Apollo 11": [(1.0, 40), (1.25, 65), (1.5, 20)],
    "Apollo 16": [(1.0, 30), (1.25, 70), (1.5, 45)],
}
```

Usage:

```python
from cross_mission_speaker_specific import plot_speaker_cross_mission_activity

fig, ax = plot_speaker_cross_mission_activity(
    speaker_activity,
    speaker_name="Charles Duke",
)
```

Generated demo figure:

```text
figures/cross_mission_speaker_specific.png
```

### 4. Speaker-turn donut plot

`donut_plots.py` visualizes the sequence and relative duration of speaker turns within a chunk/session. Each wedge corresponds to one turn. The angular size of the wedge is proportional to the turn duration. Wedge color represents the role label, such as `primary`, `secondary`, or `silence`.

This plot is useful for summarizing turn-taking structure. It shows how often the primary speaker appears, how frequently secondary speakers interrupt or contribute, and how much silence occurs between speech regions. Unlike a simple duration summary, the donut preserves the turn sequence by drawing each turn as a separate wedge.

Input format:

```python
turns = [
    {"role": "primary", "duration": 12.0},
    {"role": "secondary", "duration": 5.0},
    {"role": "silence", "duration": 20.0},
]
```

Usage:

```python
from donut_plots import plot_speaker_turn_donut

fig, ax = plot_speaker_turn_donut(turns)
```

Generated demo figure:

```text
figures/speaker_turn_donut.png
```

## Dummy Data and Demo Figures

The repository includes `generate_dummy_figures.py`, which creates synthetic data shaped to resemble speaker-analysis outputs and saves example figures to the `figures/` directory.

Run:

```bash
python generate_dummy_figures.py
```

This generates:

```text
figures/bubble_speaker_distribution.png
figures/cross_mission_activity.png
figures/cross_mission_speaker_specific.png
figures/speaker_turn_donut.png
```

The generated data is also saved in:

```text
dummy_data.json
```



## Dependencies

```bash
pip install matplotlib numpy
```


