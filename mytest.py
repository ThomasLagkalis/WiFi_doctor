# from parser import Parser

# #FILE_PATH = "./home_capture.pcapng"
# FILE_PATH = "./trace 801_11.pcapng"
import pyshark

if __name__ == "__main__":
    cap = pyshark.FileCapture('./HowIWiFi_PCAP.pcap')
    print(cap[202])
    # pcap_file = FILE_PATH
    # parser = Parser(pcap_file)
    # results = parser.parse_pcap()
    # for entry in results:
    #     print(entry)
    #     print()
