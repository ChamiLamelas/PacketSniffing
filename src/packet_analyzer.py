"""
Packet level analyzer

Chami Lamelas
"""

import pandas as pd
import misc
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import packet_monitor


def _get_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=str, help="subfolder of results/process")
    return parser.parse_args().run


def load_df(run):
    values = misc.read_object(os.path.join(packet_monitor.get_full_run_path(run), "log.pkl"))
    df = pd.DataFrame(data=values[1:], columns=values[0])
    df["total_transfer_size_megabits"] = (df["transfer_size_bytes"] * 8) / 1e6
    return df


def _system_time_series(df, run):
    system_totals = df.groupby("log_timestamp_sec")["total_transfer_size_megabits"].sum()
    timestamps = np.array(system_totals.index.tolist())[1:]
    values = system_totals.values
    transfers = [e - values[i - 1] for i, e in enumerate(values[1:], start=1)]
    _, ax = plt.subplots()
    ax.plot(timestamps, transfers)
    misc.save_plot(os.path.join(packet_monitor.get_full_run_path(run), "system_time_series.pdf"))


def main():
    run = _get_run()
    df = load_df(run)
    _system_time_series(df, run)


if __name__ == '__main__':
    main()
