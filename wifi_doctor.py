from parser import Parser
from data_monitor import DataMonitor
from visualizer import Visualizer

#FILE_PATH = "./captures/home_capture.pcapng"
#FILE_PATH = "./captures/trace 801_11.pcapng"
FILE_PATH = './captures/HowIWiFi_PCAP.pcap'
#FILE_PATH = './captures/spiti_mike.pcapng'



if __name__ == "__main__":
    pcap_file = FILE_PATH
    parser = Parser(pcap_file)
    results = parser.parse_pcap()
    monitor = DataMonitor(results)

    sel = int(input("1: density analysis\n2: performance analysis\n3: both\n"))
    if (sel == 1):
        density_data = monitor.get_density_data()
        # generate combined plot
        visualizer = Visualizer()
        visualizer.plot_density_metrics(density_data)
        visualizer.display_density_cli_metrics(density_data)
    elif (sel == 2):
        # performance analysis
        performance_data = monitor.get_performance_data(verbose=1)
    elif (sel == 3):
        density_data = monitor.get_density_data()
        # generate combined plot
        visualizer = Visualizer()
        visualizer.plot_density_metrics(density_data)
        visualizer.display_density_cli_metrics(density_data)
        
        # generate performacne analysis
        performance_data = monitor.get_performance_data(verbose=1)
    else:
        print("Wrong input")

