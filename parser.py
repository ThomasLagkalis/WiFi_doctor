import pyshark

class Parser:
    '''
    A class that parses a pcap file and extracts relavant WI-FI parameters
    '''
    def __init__(self, file_path):
        self.file_path = file_path
        self.parsed_data = []

    def parse_pcap(self):
        """
        Parses a pcap file and extracts relevant Wi-Fi parameters.
        i.e.
            - BSSID
            - Transmitter MAC
            - Receiver MAC
            - Type/Subtype
            - PHY Type
            - MCS Index
            - Bandwidth
            - Spatial Streams
            - Short Gi
            - Channel
            - Frequency
            - Signal strength (dBm)
            - SNR
            - Data Rate
            - TSF timestamp
            - Retry flag
        """
        capture = pyshark.FileCapture(self.file_path, display_filter="wlan")
        parsed_data = []
        
        for index, packet in enumerate(capture):
            if index > 500:
               break
            try:
                wlan_layer = packet.wlan
                wlan_radio_layer = packet.wlan_radio if hasattr(packet, 'wlan_radio') else None
                radio_layer = packet.radiotap if hasattr(packet, 'radiotap') else None
                data = {
                    "BSSID": wlan_layer.bssid if hasattr(wlan_layer, 'bssid') else None,
                    "Transmitter MAC": wlan_layer.ta if hasattr(wlan_layer, 'ta') else None,
                    "Receiver MAC": wlan_layer.ra if hasattr(wlan_layer, 'ra') else None,
                    "Type/Subtype": wlan_layer.fc_type_subtype if hasattr(wlan_layer, 'fc_type_subtype') else None,
                    "PHY Type": wlan_radio_layer.phy if wlan_radio_layer and  hasattr(wlan_radio_layer, 'phy') else None,
                    "MCS Index": radio_layer.mcs_index if radio_layer and  hasattr(radio_layer, 'mcs_index') else None,
                    "Bandwidth": radio_layer.mcs_bw if radio_layer and  hasattr(radio_layer, 'mcs_bw') else None,
                    "Spatial Streams": radio_layer.mcs_stbc if wlan_radio_layer and  hasattr(radio_layer, 'mcs_stbc') else None,
                    "Short Gi": (int(radio_layer.flags, 16) & 128) == 128 if radio_layer and  hasattr(radio_layer, 'flags') else None,
                    "Channel": wlan_radio_layer.channel if wlan_radio_layer and hasattr(wlan_radio_layer, 'channel') else None,
                    "Frequency": radio_layer.channel_freq if radio_layer and hasattr(radio_layer, 'channel_freq') else None,
                    "Signal Strength (dBm)": wlan_radio_layer.signal_dbm if wlan_radio_layer and hasattr(wlan_radio_layer, 'signal_dbm') else None,
                    "Signal/Noise Ratio": wlan_radio_layer.snr if wlan_radio_layer and hasattr(wlan_radio_layer, 'snr') else None,
                    "Data Rate": wlan_radio_layer.data_rate if wlan_radio_layer and hasattr(wlan_radio_layer, 'data_rate') else None,
                    "TSF Timestamp": float(wlan_radio_layer.timestamp) if wlan_radio_layer and hasattr(wlan_radio_layer, 'timestamp') else None,
                    "Retry": int(wlan_layer.flags, 16) & 8 if wlan_layer and hasattr(wlan_layer, 'flags') else None
                }



                parsed_data.append(data)
            except Exception as e:
                print(f"Error parsing packet: {e}")

        capture.close()
        return parsed_data

