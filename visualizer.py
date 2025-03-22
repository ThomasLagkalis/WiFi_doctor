import matplotlib.pyplot as plt
import numpy as np

class Visualizer:

    def __init__(self):
        """
        Data to visualize (e.g. metrics).
        """

    def plot_density_metrics(self, metrics_dict):
        """Plots all metrics in a single figure with multiple subplots."""
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle("Network Density Analysis Metrics", fontsize=16)
        
        metric_titles = [
            ("Unique Transmitter MACs per BSSID", "BSSID Index", "Tx MAC addresses/sec"),
            ("Total Packets Transmitted per BSSID", "BSSID Index", "Packets/sec"),
            ("Total Packets Transmitted per PHY Type", "PHY Type", "Packets/sec"),
            ("Total Packets Transmitted per Channel", "Channel", "Packets/sec"),
            ("Total Packets Transmitted per Frequency Band", "Frequency Band", "Packets/sec"),
            ("Mean RSSI per BSSID", "BSSID Index", "RSSI (dBm)")
        ]
        
        metric_keys = [
            'tx_per_bssid', 'packets_per_bssid', 'packets_per_phy', 'packets_per_channel', 'packets_per_band', 'mean_rssi_per_bssid'
        ]
        
        for ax, key, (title, xlabel, ylabel) in zip(axes.flatten(), metric_keys, metric_titles):
            data = metrics_dict[key]
            ax.bar(data.keys(), data.values())
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_xticks(np.arange(len(data)))  # Ensure integer ticks
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

    def display_density_cli_metrics(self, density_data):
        print("Unique Transmitter MACs per BSSID:")
        print(density_data['tx_per_bssid'])
        print("\nTotal Packets Transmitted per BSSID:")
        print(density_data['packets_per_bssid'])
        print("\nTotal Packets Transmitted per PHY Type:")
        print(density_data['packets_per_phy'])
        print("\nTotal Packets Transmitted per Channel:")
        print(density_data['packets_per_channel'])
        print("\nTotal Packets Transmitted per Frequency Band:")
        print(density_data['packets_per_band'])
        print("\nRSSID:")
        print(density_data['rssid'])
