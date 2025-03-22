from parser import Parser
from density_analysis import Analyzer
from visualizer import Visualizer

#FILE_PATH = "./home_capture.pcapng"
#FILE_PATH = "./trace 801_11.pcapng"
#FILE_PATH = './HowIWiFi_PCAP.pcap'
FILE_PATH = './spiti_mike.pcapng'



if __name__ == "__main__":
    pcap_file = FILE_PATH
    parser = Parser(pcap_file)
    results = parser.parse_pcap()
    analyzer = Analyzer(results)
    density_data = analyzer.get_density_data()

    # generate combined plot
    visualizer = Visualizer()
    visualizer.plot_density_metrics(density_data)
    visualizer.display_density_cli_metrics(density_data)
