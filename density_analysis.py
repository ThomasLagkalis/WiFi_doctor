import pandas as pd

class Analyzer:

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
        #df = pd.DataFrame(data, columns=['BSSID', 'Transmitter MAC', 'PHY Type', 'Channel', 'Frequency', 
           #                              'Signal Strength (dBm)', 'Signal/Noise Ratio']).apply(pd.to_numeric, errors='ignore') \
         #   .groupby(by='Transmitter MAC') \
          #  .agg({'BSSID': 'size', 'Signal Strength (dBm)': ['min', 'max', 'mean'], 'Frequency':['min', 'max', 'mean'], 'Signal/Noise Ratio': ['min', 'max', 'mean']})
        
        #print(df)
        #total_ssid = df['BSSID'].sum()
        #df['BSSID'] = df['BSSID']/total_ssid
        #print(df['BSSID'])
        #print(df.shape)
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
        #print('hey')

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
        """
        df = pd.DataFrame(self.data, columns=['SSID', 'BSSID', 'Transmitter MAC', 'PHY Type', 'Channel', 'Frequency', 'Signal Strength (dBm)'])
        
        # Ensure 'Frequency' and 'Signal Strength (dBm)' columns are numeric, coercing errors to NaN
        df['Frequency'] = pd.to_numeric(df['Frequency'], errors='coerce')
        df['Signal Strength (dBm)'] = pd.to_numeric(df['Signal Strength (dBm)'], errors='coerce')
        
        # Count unique Transmitter MACs per BSSID
        tx_macs_per_bssid = df.groupby('BSSID')['Transmitter MAC'].nunique()
        
        # Count total packets transmitted per BSSID
        packets_per_bssid = df.groupby('BSSID').size()
        
        # Count total packets transmitted per PHY type
        packets_per_phy = df.groupby('PHY Type').size()
        
        # Count total packets transmitted per channel
        packets_per_channel = df.groupby('Channel').size()
        
        # Categorize frequency into 2.4 GHz and 5 GHz bands, handling NaN values
        df['Frequency Band'] = df['Frequency'].apply(lambda x: '2.4 GHz' if pd.notna(x) and x < 3000 else ('5 GHz' if pd.notna(x) else 'Unknown'))
        packets_per_band = df.groupby('Frequency Band').size()
        
        # Compute mean RSSI per SSID
        mean_rssi_per_ssid = df.groupby('SSID')['Signal Strength (dBm)'].mean()
        
        # Compute overall RSSID using mean RSSI per SSID
        rssid = (1 / mean_rssi_per_ssid.abs()).sum() if not mean_rssi_per_ssid.isnull().all() else None
        
        # Compute total number of SSIDs
        total_ssids = df['SSID'].nunique()
        return {
            'tx_per_bssid': tx_macs_per_bssid.to_dict(),
            'packets_per_bssid': packets_per_bssid.to_dict(),
            'packets_per_phy': packets_per_phy.to_dict(),
            'packets_per_channel': packets_per_channel.to_dict(),
            'packets_per_band': packets_per_band.to_dict(),
            'rssid': rssid,
            'total_ssids': total_ssids
        }
