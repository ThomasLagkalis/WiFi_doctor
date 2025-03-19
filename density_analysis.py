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
        df = pd.DataFrame(data, columns=['BSSID', 'Transmitter MAC', 'PHY Type', 'Channel', 'Frequency', 
                                         'Signal Strength (dBm)', 'Signal/Noise Ratio']).apply(pd.to_numeric, errors='ignore') \
            .groupby(by='Transmitter MAC') \
            .agg({'BSSID': 'size', 'Signal Strength (dBm)': ['min', 'max', 'mean'], 'Frequency':['min', 'max', 'mean'], 'Signal/Noise Ratio': ['min', 'max', 'mean']})
        
        print(df)
        total_ssid = df['BSSID'].sum()
        df['BSSID'] = df['BSSID']/total_ssid
        print(df['BSSID'])
        print(df.shape)
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
        print('hey')
