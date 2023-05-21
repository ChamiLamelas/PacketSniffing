"""
System-wide network usage analyzer

Chami Lamelas
"""

import pickle
import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import math
from collections import Counter
import misc
import monitor


def _get_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=str, help="subfolder of results/system")
    return parser.parse_args().run


def _make_cdf(run, log):
    _, ax = plt.subplots()
    hist = sorted([(k, v) for k, v in Counter(log).items()], key=lambda e: e[0])
    x = [e[0] for e in hist]
    counts = [e[1] for e in hist]
    factor = sum(counts)
    pdf = [e / factor for e in counts]
    cdf = np.cumsum(pdf)
    ax.plot(x, cdf)
    ax.set_xlabel("Total System Network Usage (Mbps)")
    ax.set_ylabel("CDF")
    ax.spines[['right', 'top']].set_visible(False)
    misc.save_plot(os.path.join(monitor.get_full_run_path(run), "cdf.pdf"))


def _make_time_series(run, log):
    _, ax = plt.subplots()
    x = np.arange(len(log))
    mins = np.arange(math.ceil(len(log) / 60)) + 1
    mins_ticks = [60 * m - 1 for m in mins]
    ax.set_xticks(mins_ticks[9::10])
    ax.set_xticklabels(mins[9::10])
    ax.plot(x, log)
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Total System Network Usage (Mbps)")
    ax.spines[['right', 'top']].set_visible(False)
    misc.save_plot(os.path.join(monitor.get_full_run_path(run), "time_series.pdf"))


def main():
    run = _get_run()
    with open(os.path.join(monitor.get_full_run_path(run), "log.pkl"), "rb") as f:
        log = pickle.load(f)
    _make_cdf(run, log)
    _make_time_series(run, log)


if __name__ == '__main__':
    main()
