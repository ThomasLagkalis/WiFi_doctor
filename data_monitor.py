import pandas as pd
import math

class DataMonitor:

    def __init__(self, data):
        self.data = data
        """
        Data Columns For Density Analysis
        i.e.
            - BSSID
            - Transmitter MAC
            - PHY Type
            - Channel
            - Frequency
            - Signal strength (dBm)
            - SNR
        """
        
        """
        Signal strength Expected Quality
        -90dBm  Chances of connecting are very low at this level
        -80dBm  Unreliable signal strength
        -67dBm  Reliable signal strength– the edge of what Cisco considers to be adequate to support Voice over WLAN
        -55dBm  Anything down to this level can be considered excellent signal strength.
        -30dBm  Maximum signal strength, you are probably standing right next to the access point.
        -90_-67 : bad / low
        -67_-55 : medium
        -55_-30 : good / high
        """
        """
        https://www.netspotapp.com/wifi-troubleshooting/snr.html
        SNR Range (dB)  Connection Quality  Best Use Cases
        Less than 10    Unusable  Barely functional Wi-Fi, emergency use only
        10 - 15 Poor  Limited browsing, non-critical tasks
        15 - 25 Fair  Basic web usage, standard video calls
        25 - 40 Very Good  HD streaming, video calls, web browsing
        40 +    Excellent  4K streaming, online gaming, large file transfers

        """

    def _Re_mapping(self, mcs_index, phy_type, bandwidth, spatial_streams, short_gi):
        """
        Return expected PHY rate in Mbps
        """
        if math.isnan(mcs_index): return None
        bw = 20 * 2**int(bandwidth)
        #dictionary element = mcs_index: {bandwidth: [data rate/800ns, data rate/400ns]}
        table_80211n = {
            0: {20: [6.5, 7.2],   40: [13.5, 14.4], 80: [29.3, 32.5],     160: [58.5, 65]},
            1: {20: [13, 14.4],   40: [27, 30],     80: [58.5, 65],       160: [117, 130]},
            2: {20: [19.5, 21.7], 40: [40.5, 45],   80: [87.8, 97.5],     160: [175.5, 195]},
            3: {20: [26, 28.9],   40: [54, 60],     80: [117, 130],       160: [234, 260]},
            4: {20: [39, 43.3],   40: [81, 90],     80: [175.5, 195],     160: [351, 390]},
            5: {20: [52, 57.8],   40: [108, 120],   80: [234, 260],       160: [468, 520]},
            6: {20: [58.5, 65],   40: [121.5, 135], 80: [263.3, 292.5],   160: [526.5, 585]},
            7: {20: [65, 72.2],   40: [135, 150],   80: [292.5, 325],     160: [585, 650]},
        }

        table_80211ac = {
            8: {20: [78, 86.7],   40: [162, 180],   80: [351, 390],       160: [702, 780]},
            9: {40: [180, 200],   80: [292.5, 325], 160: [585, 650]}
        }

        use_table = table_80211ac.get(mcs_index) if phy_type == 8 else table_80211n.get(mcs_index) if mcs_index < 8 else table_80211n.get(mcs_index % 8)

        data_rate = use_table.get(bw)[short_gi] * (int(spatial_streams) +1)
        return data_rate


    def get_performance_data(self, verbose=0):
        """
        Calculates the theoretical downlink throughput (Throughput = Data_Rate * (1-Frame_Loss_Rate))
        and returns the throughput and the following performace data:

        - PHY Type
        - Bandwidth
        - Short Gi
        - Data Rate
        - MCS Index
        - Signal Strength (dBm)
        - Spatial Streams
        - Rate Gap (as defined in I.Pefkianakis et al. Characterizing Home Wireless Performance: The Gateway View)
        
        verbose : - 0 -> silent mode
                  - 1 -> print in stdout the calculated throughputw
        """
        df = pd.DataFrame(self.data, columns=['Transmitter MAC', 'Receiver MAC', 'PHY Type',  'Signal Strength (dBm)', 'Bandwidth', 'Data Rate', 'Short Gi', 'MCS Index', 'Spatial Streams', 'Retry'])
       

        # Filter packets from AP (2C:F8:9B:DD:06:A0) to device (00:20:A6:FC:B0:36)
        df = df[(df['Transmitter MAC'] == '2c:f8:9b:dd:06:a0') & (df['Receiver MAC'] == '00:20:a6:fc:b0:36')]

        df['Signal Strength (dBm)'] = pd.to_numeric(df['Signal Strength (dBm)'], errors='coerce')
        df['MCS Index'] = pd.to_numeric(df['MCS Index'], errors='coerce')
        
        # Calculate retry (loss) rate.
        retries = df.groupby('Retry').size()
        retries = retries.to_dict()
        df['Data Rate'] = pd.to_numeric(df['Data Rate'], errors='coerce')
        mean_data_rate = df['Data Rate'].mean()
        loss_rate = retries[8]/(retries[8] + retries[0])  
        mean_throughput = mean_data_rate * (1- loss_rate)
        #df['Rate Gap'] = df['Signal Strength (dBm)'].apply(lambda x: self._Re_mapping(x)) - df['Data Rate']
        df['Re'] = df.apply(lambda x: self._Re_mapping(x['MCS Index'], x['PHY Type'], x['Bandwidth'], x['Spatial Streams'], x['Short Gi']), axis=1)
        df['Rate Gap'] = df['Re'] - df['Data Rate']

        # Make the time series of throughput
        df['Throughput'] = df['Data Rate'] * (1 - loss_rate)

        if (verbose == 1):
            print(df)
            print('Loss Rate: ', loss_rate)
            print('Mean data rate: ', mean_data_rate)
            print('Downlink Mean Throughput: ', mean_throughput)

        return {
            'mean throughput': mean_throughput,
            'data frame': df
            }

    def get_density_data(self):
        """
        Calculates and returns:
        - The number of unique transmitter MACs per BSSID
        - The total packets transmitted per BSSID
        - The total packets transmitted per PHY type
        - The total packets transmitted per channel
        - The total packets transmitted per frequency band (2.4 GHz or 5 GHz)
        - The RSSID (Received Signal Strength Inverse Density) for the entire dataset
        - The total number of SSIDs
        - The mean RSSI per BSSID
        """
        df = pd.DataFrame(self.data, columns=['SSID', 'BSSID', 'Transmitter MAC', 'PHY Type', 'Channel', 'Frequency', 'Signal Strength (dBm)', 'TSF Timestamp'])
       
        
        # Ensure 'TSF Timestamp', 'Frequency' and 'Signal Strength (dBm)' columns are numeric, coercing errors to NaN
        df['TSF Timestamp'] = pd.to_numeric(df['TSF Timestamp'], errors='coerce')
        df['Frequency'] = pd.to_numeric(df['Frequency'], errors='coerce')
        df['Signal Strength (dBm)'] = pd.to_numeric(df['Signal Strength (dBm)'], errors='coerce')
         
        # Calculate the total duration of capture in seconds
        total_duration = (df['TSF Timestamp'].iloc[-1] - df['TSF Timestamp'].iloc[0])/1000000
        if (math.isnan(total_duration)):
            total_duration = 1
        
        # Count unique Transmitter MACs per BSSID
        tx_macs_per_bssid = df.groupby('BSSID')['Transmitter MAC'].nunique()
        
        # Count total packets transmitted per BSSID
        packets_per_bssid = df.groupby('BSSID').size()
        
        # Compute mean RSSI per BSSID
        mean_rssi_per_bssid = df.groupby('BSSID')['Signal Strength (dBm)'].mean()
        
        # Assign index numbers to BSSIDs for plotting
        bssid_index = {bssid: idx for idx, bssid in enumerate(tx_macs_per_bssid.keys())}
        
        # Convert BSSID keys to integer index values
        tx_macs_per_bssid = {int(bssid_index[bssid]): float(count / total_duration) for bssid, count in tx_macs_per_bssid.items()}
        packets_per_bssid = {int(bssid_index[bssid]): float(count / total_duration) for bssid, count in packets_per_bssid.items()}
        mean_rssi_per_bssid = {int(bssid_index[bssid]): float(rssi) for bssid, rssi in mean_rssi_per_bssid.items()}
        
        # Count total packets transmitted per PHY type
        packets_per_phy = (df.groupby('PHY Type').size() / total_duration).to_dict()
        
        # Count total packets transmitted per channel
        packets_per_channel = (df.groupby('Channel').size() / total_duration).to_dict()
        
        # Categorize frequency into 2.4 GHz and 5 GHz bands, handling NaN values
        df['Frequency Band'] = df['Frequency'].apply(lambda x: '2.4 GHz' if pd.notna(x) and x < 3000 else ('5 GHz' if pd.notna(x) else 'Unknown'))
        packets_per_band = (df.groupby('Frequency Band').size() / total_duration).to_dict()
        
        # Compute overall RSSID using mean RSSI per SSID
        rssid = 0
        for m in mean_rssi_per_bssid.values():
            if m:
                rssid += 1/abs(m)
        
        return {
            'tx_per_bssid': tx_macs_per_bssid,
            'packets_per_bssid': packets_per_bssid,
            'packets_per_phy': packets_per_phy,
            'packets_per_channel': packets_per_channel,
            'packets_per_band': packets_per_band,
            'mean_rssi_per_bssid': mean_rssi_per_bssid,
            'rssid': rssid,
        }
