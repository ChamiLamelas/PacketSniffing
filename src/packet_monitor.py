"""
Packet level monitor

Chami Lamelas
"""

import os

import scapy.all as sc
import psutil
from collections import Counter, namedtuple
import threading
import time
import argparse

import misc


def get_full_run_path(run):
    return os.path.join("..", "results", "process", run)


class PacketIdentifier(namedtuple("PacketIdentifier", ["src_ip", "dst_ip", "src_port", "dst_port"])):
    def flipped(self):
        return PacketIdentifier(self.src_ip, self.dst_ip, self.src_port, self.dst_port)


class ApplicationPacketSniffer:
    DOWNLOAD_DIRECTION = "download"
    UPLOAD_DIRECTION = "upload"

    def __init__(self, update_transfer_frequency_sec, update_sockets_frequency_sec, total_sniffing_time_min):
        self.__update_transfer_frequency_sec = update_transfer_frequency_sec
        self.__update_sockets_frequency_sec = update_sockets_frequency_sec
        self.__total_sniffing_time_sec = total_sniffing_time_min * 60 + 1
        self.__update_transfer_table = Counter()
        self.__detailed_log_table = [
            ["src_ip", "dst_ip", "src_port", "dst_port", "pid", "process_creation_time_sec", "process_name",
             "transfer_direction", "log_timestamp_sec", "total_transfer_size_bytes"]]
        self.__translation_table = dict()
        self.__network_interfaces = str(sc.ifaces)

    def __process_packet(self, packet):
        if "IP" in packet:
            src_ip = packet["IP"].src
            dst_ip = packet["IP"].dst
            transport = next((k for k in ["TCP", "UDP"] if k in packet), None)
            if transport is not None:
                src_port = packet[transport].sport
                dst_port = packet[transport].dport
                self.__update_transfer_table[PacketIdentifier(src_ip, dst_ip, src_port, dst_port)] += len(packet)

    def __collect_sockets(self):
        num_collections = int(self.__total_sniffing_time_sec / self.__update_sockets_frequency_sec)
        for i in range(num_collections):
            if i > 0:
                time.sleep(self.__update_sockets_frequency_sec)
            sockets = psutil.net_connections()
            for socket in sockets:
                if socket.laddr and socket.raddr:
                    src_ip, src_port = socket.laddr
                    dst_ip, dst_port = socket.raddr
                    self.__translation_table[PacketIdentifier(src_ip, dst_ip, src_port, dst_port)] = socket.pid

    def __start_collecting_sockets(self):
        thread = threading.Thread(target=self.__collect_sockets)
        thread.start()
        return thread

    def __log_transfers(self):
        num_collections = int(self.__total_sniffing_time_sec / self.__update_transfer_frequency_sec)
        for i in range(num_collections):
            if i > 0:
                time.sleep(self.__update_transfer_frequency_sec)

            for packet_id in list(self.__update_transfer_table.keys()):
                lookup, direction = None, None
                if packet_id in self.__translation_table:
                    lookup = packet_id
                    direction = ApplicationPacketSniffer.UPLOAD_DIRECTION
                elif packet_id.flipped() in self.__translation_table:
                    lookup = packet_id.flipped()
                    direction = ApplicationPacketSniffer.DOWNLOAD_DIRECTION

                if lookup is not None:
                    pid = self.__translation_table[lookup]
                    try:
                        process = psutil.Process(pid)
                        self.__detailed_log_table.append(
                            [packet_id.src_ip, packet_id.dst_ip, packet_id.src_port, packet_id.dst_port, pid,
                             process.create_time(), process.name(), direction, i,
                             self.__update_transfer_table[packet_id]])
                    except psutil.NoSuchProcess:
                        pass

    def __start_logging_transfers(self):
        thread = threading.Thread(target=self.__log_transfers)
        thread.start()
        return thread

    def start(self):
        socket_collector = self.__start_collecting_sockets()
        transfer_logger = self.__start_logging_transfers()
        sc.sniff(prn=self.__process_packet, timeout=self.__total_sniffing_time_sec, store=False)
        socket_collector.join()
        transfer_logger.join()
        misc.save_object(self.__detailed_log_table,
                         os.path.join(get_full_run_path(misc.formatted_now()), "log.pkl"))


def __get_cmdline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--t", "--update_transfer_frequency", type=int, help="Update Transfer Frequency (s)", default=1)
    parser.add_argument("--s", "--update_sockets_frequency", type=int, help="Update Sockets Frequency (s)", default=1)
    parser.add_argument("total_sniffing_time", type=int, help="Total Sniffing Time (min)")
    args = parser.parse_args()
    update_transfer_frequency = args.t
    update_sockets_frequency = args.s
    total_sniffing_time = args.total_sniffing_time
    return update_transfer_frequency, update_sockets_frequency, total_sniffing_time


def main():
    ApplicationPacketSniffer(*__get_cmdline_args()).start()


if __name__ == '__main__':
    main()
