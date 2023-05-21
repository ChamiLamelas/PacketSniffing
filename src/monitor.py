"""
System-wide network usage monitor

Chami Lamelas
"""

import psutil
import time
import os
import argparse

import misc


def get_full_run_path(run):
    return os.path.join("..", "results", "system", run)


def _get_time_and_freq():
    parser = argparse.ArgumentParser()
    parser.add_argument("time", type=int, help="total time (min)")
    parser.add_argument("-f", "--frequency", type=float, help="logging frequency (sec)", default=1)
    args = parser.parse_args()
    return args.time, args.frequency


def _bytes_to_mb(num_bytes):
    return (8 * num_bytes) / 1e6


def _monitor(total_time, frequency):
    secs = total_time * 60 + 1
    log = list()
    for i in range(secs):
        if i > 0:
            time.sleep(frequency)
        ti = time.time()
        wifi_use = psutil.net_io_counters(pernic=True)["Wi-Fi"]
        megabits_sent = _bytes_to_mb(wifi_use.bytes_sent)
        megabits_recv = _bytes_to_mb(wifi_use.bytes_recv)
        log.append(megabits_sent + megabits_recv)
        tf = time.time()
        print(tf - ti)
    return log


def _collect_stats(log):
    misc.save_object(misc.totals_to_transfers(log), os.path.join(get_full_run_path(misc.formatted_now()), "log.pkl"))


def main():
    total_time, freq = _get_time_and_freq()
    _collect_stats(_monitor(total_time, freq))


if __name__ == '__main__':
    main()
