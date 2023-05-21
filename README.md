# Packet Sniffing

Repository where I experiment with `psutil` and `scapy` for bandwidth measurements in the interest of looking into network plans. `psutil` is used for system wide
network usage measurements. `scapy` is used to perform packet sniffing to get per process bandwidth measurements.

Setup: `pip install -r requirements.txt`

Running: `python <filename> -h` for all `src/` files besides `misc.py`.

You will see a `results` folder being created by `monitor` files.

Acknowledgements:
* [Network Usage Monitor Tutorial](https://www.thepythoncode.com/article/make-a-network-usage-monitor-in-python)
* [psutil documentation](https://psutil.readthedocs.io/en/latest/)
* [scapy documentation](https://scapy.readthedocs.io/en/latest/api/scapy.sendrecv.html)
* [stackoverflow scapy article 1](https://stackoverflow.com/questions/19311673/fetch-source-address-and-port-number-of-packet-scapy-script)
* [stackoverflow scapy article 2](https://stackoverflow.com/questions/10552067/get-packet-size-in-scapy-python)
* [stackoverflow python thread safety](https://stackoverflow.com/questions/6953351/thread-safety-in-pythons-dictionary)

Chami Lamelas

