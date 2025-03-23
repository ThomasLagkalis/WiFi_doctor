from parser import Parser
from data_monitor import DataMonitor
from visualizer import Visualizer

#FILE_PATH = "./captures/home_capture.pcapng"
#FILE_PATH = "./captures/trace 801_11.pcapng"
#FILE_PATH = './captures/HowIWiFi_PCAP.pcap'
FILE_PATH = './captures/spiti_mike.pcapng'



if __name__ == "__main__":
    pcap_file = FILE_PATH
    parser = Parser(pcap_file)
    results = parser.parse_pcap()
    monitor = DataMonitor(results)
    density_data = monitor.get_density_data()

    # generate combined plot
    visualizer = Visualizer()
    visualizer.display_density_cli_metrics(density_data)
    visualizer.plot_density_metrics(density_data)
