"""
Miscellaneous utility functions

Chami Lamelas
"""

from pathlib import Path
import os
import pickle
from datetime import datetime
import matplotlib.pyplot as plt


def formatted_now():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def prep_path(path):
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)


def save_object(obj, path):
    prep_path(path)
    with open(path, 'wb+') as f:
        pickle.dump(obj, f)


def read_object(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def save_plot(path):
    plt.savefig(path, bbox_inches='tight', format='pdf')
    plt.close()


def totals_to_transfers(totals):
    return [e - totals[i - 1] for i, e in enumerate(totals[1:], start=1)]
