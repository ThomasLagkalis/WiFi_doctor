import matplotlib
matplotlib.use('Qt5Agg')
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



    def plot_throughput_stats(self, performance_data):
        """
        Plots throughput per packet index along with min, max, median, 75th, and 90th percentiles.

        Parameters:
            performance_data (dict): Output from `get_performance_data()` containing the DataFrame.
        """
        df = performance_data['data frame']  # Extract the full DataFrame
        throughput = df['Throughput'].dropna().reset_index(drop=True)  # Drop NaN & reset index as packet number

        # Compute Statistics
        min_val = throughput.min()
        max_val = throughput.max()
        median_val = throughput.median()
        mean_val = throughput.mean()
        p75_val = throughput.quantile(0.75)
        p90_val = throughput.quantile(0.90)

        # Packet index as x-axis
        packet_index = np.arange(len(throughput))

        # Plot
        plt.figure(figsize=(12, 6))

        rolling_avg = throughput.rolling(window=300, min_periods=1).mean()

        plt.plot(packet_index, throughput, label='Throughput', color='blue', linestyle='-', linewidth=2, alpha=0.3)
        plt.plot(packet_index, rolling_avg, label='Rolling Average', color='purple', linestyle='-', linewidth=2)

        # Plot Total Statistics as Horizontal Lines
        plt.axhline(min_val, color='gray', linestyle='--', label=f'Min: {min_val:.2f} Mbps')
        plt.axhline(max_val, color='black', linestyle='--', label=f'Max: {max_val:.2f} Mbps')
        plt.axhline(median_val, color='green', linestyle='-', label=f'Median: {median_val:.2f} Mbps')
        plt.axhline(p75_val, color='orange', linestyle='-.', label=f'75th Percentile: {p75_val:.2f} Mbps')
        plt.axhline(p90_val, color='red', linestyle=':', label=f'90th Percentile: {p90_val:.2f} Mbps')
        plt.axhline(mean_val, color='cyan', linestyle='-', label=f'Mean: {mean_val:.2f} Mbps')
    
        plt.xlabel('Packet Index')
        plt.ylabel('Throughput (Mbps)')
        plt.title('Throughput per Packet with Statistical Percentiles')
        plt.legend()
        plt.grid(True)
        plt.show()

        # --- Plot 2: Histogram of Throughput ---
        plt.figure(figsize=(10, 5))
        plt.hist(throughput, bins=20, color='skyblue', edgecolor='black', alpha=0.7, density=False)

        # Plot mean & median as vertical lines
        plt.axvline(mean_val, color='cyan', linestyle='-', linewidth=2, label=f'Mean: {mean_val:.2f} Mbps')
        plt.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f} Mbps')

        # Labels & Formatting
        plt.xlabel('Throughput (Mbps)')
        plt.ylabel('Throughput Density')
        plt.title('Histogram of Throughput Distribution')
        plt.legend()
        plt.grid(True)
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
