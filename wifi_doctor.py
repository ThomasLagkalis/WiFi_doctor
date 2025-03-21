from parser import Parser
from density_analysis import Analyzer

FILE_PATH = "./home_capture.pcapng"
#FILE_PATH = "./trace 801_11.pcapng"
#FILE_PATH = './HowIWiFi_PCAP.pcap'
#FILE_PATH = './spiti_mike.pcapng'

if __name__ == "__main__":
    pcap_file = FILE_PATH
    parser = Parser(pcap_file)
    results = parser.parse_pcap()
    analyzer = Analyzer(results)
    density_data = analyzer.get_density_data()
    print(density_data)
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
    print("\nTotal SSIDs:")
    print(density_data['total_ssids'])
