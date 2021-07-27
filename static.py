"""
matplotlib charts go here
"""

import pandas as pd

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


def get_label(col):
    if "_roll" in col:
        col = col.split("_roll")[0]

    labels = {
        "Full": "Fully infectious\n(Glady's number)",
        "Part": "Partly infections WTF",
        "Unkn": "Unknown, or we don't know",
        "Total": "Infectious in the community\n(real number)",
        "Local_cases": "All cases\nisolating + infectious",
        "Isolating": "iso All cases, isolating + infectious",
    }

    return labels[col]


def make_plot(df):

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle("NSW")
    ax.set_title(
        f"Covid cases in NSW {df.Date.min():%b-%d} to {df.Date.max():%b-%d}",
        fontsize=14,
    )

    ax.set_ylabel("Infectious Cases")
    ax.set_xlabel("Date")

    X = df.Date
    colors = {}

    # draw smoothed lines
    cols = ["Local_cases", "Total", "Full"]
    for i, col in enumerate(cols[::-1]):
        Y = df[col]
        Y_roll = df[f"{col}_roll"]
        bottom = None if (i - 1) < 0 else df[cols[i - 1]]

        # draw line
        line = ax.plot(
            X,
            Y_roll,
            lw=1.8,
            linestyle="--",
            alpha=0.88,
            color="red" if col == "Total" else None,
        )

        color = line[0].get_color()
        colors[col] = color

        # label line at its end
        xy = X.iloc[-1] + pd.DateOffset(days=1), Y_roll.values[-1]
        ax.annotate(get_label(col), xy=xy, fontsize=15, color=color)

    # step
    # ax.step(df.Date, df.Total, "o--", alpha=0.35, color=colors["Total"])

    # stacked bar chart
    alpha = 0.05
    full = ax.bar(df.Date, df.Full, label="Fully Infectious", alpha=alpha)
    part = ax.bar(
        df.Date, df.Part, bottom=df.Full, label="Partially Infectious", alpha=alpha
    )
    unkn = ax.bar(
        df.Date, df.Unkn, bottom=df.Full + df.Part, label="Not telling us", alpha=0.1
    )
    isolating = ax.bar(
        df.Date,
        df.Isolating,
        bottom=df.Total,
        label="Isolating",
        color=colors["Local_cases"],
        alpha=alpha,
    )  # only drawing for labels

    for rect in [full, part, unkn, isolating]:  # label the bars in the center
        ax.bar_label(rect, label_type="center", alpha=0.4)

    # label totals by making a invisible total bar
    r = ax.bar(df.Date, df.Total, alpha=0)  # only drawing for labels
    ax.bar_label(r, alpha=0.8, padding=5, fontsize=14, color=colors["Total"])

    ax.bar_label(
        isolating, alpha=0.8, padding=5, fontsize=12, color=colors["Local_cases"]
    )

    # final plot tweaks
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    date_form = mdates.DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date_form)
    ax.legend(loc="upper left", fontsize=13)

    return fig