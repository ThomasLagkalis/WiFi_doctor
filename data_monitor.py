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
    def _Re_mapping(self, RSSI):
        """
        Return expected PHY rate in Mbps
        """
        if RSSI <= -88: return 6.5
        elif -87 <= RSSI <= -86: return 13
        elif -85 <= RSSI <= -83: return 19.5
        elif -82 <= RSSI <= -81: return 26
        elif -80 <= RSSI <= -75: return 39
        elif -74 <= RSSI <= -73: return 52
        elif -72 <= RSSI <= -71: return 58.5
        elif -70 <= RSSI: return 65
        else: return 0 


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
        - Rate Gap (as defined in I.Pefkianakis et al. Characterizing Home Wireless Performance: The Gateway View)
        
        verbose : - 0 -> silent mode
                  - 1 -> print in stdout the calculated throughputw
        """
        df = pd.DataFrame(self.data, columns=['Transmitter MAC', 'Receiver MAC', 'PHY Type',  'Signal Strength (dBm)', 'Bandwidth', 'Data Rate', 'Short Gi', 'MCS Index', 'Retry'])

        # Filter packets from AP (2C:F8:9B:DD:06:A0) to device (00:20:A6:FC:B0:36)
        df = df[(df['Transmitter MAC'] == '2c:f8:9b:dd:06:a0') & (df['Receiver MAC'] == '00:20:a6:fc:b0:36')]

        df['Signal Strength (dBm)'] = pd.to_numeric(df['Signal Strength (dBm)'], errors='coerce')
        
        # Calculate retry (loss) rate.
        retries = df.groupby('Retry').size()
        retries = retries.to_dict()
        df['Data Rate'] = pd.to_numeric(df['Data Rate'], errors='coerce')
        mean_data_rate = df['Data Rate'].mean()
        loss_rate = retries[8]/(retries[8] + retries[0])  
        throughput = mean_data_rate * (1- loss_rate)
        df['Rate Gap'] = df['Signal Strength (dBm)'].apply(lambda x: self._Re_mapping(x)) - df['Data Rate']

        if (verbose == 1):
            print(df)
            print('Loss Rate: ', loss_rate)
            print('Mean data rate: ', mean_data_rate)
            print('Downlink Throughput: ', throughput)
            
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
