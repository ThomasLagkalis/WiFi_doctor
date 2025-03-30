from parser import Parser
from data_monitor import DataMonitor
from visualizer import Visualizer
from analyzer import Analyzer

#FILE_PATH = "./captures/home_capture.pcapng"
#FILE_PATH = "./captures/trace 801_11.pcapng"
FILE_PATH = './captures/HowIWiFi_PCAP.pcap'
#FILE_PATH = './captures/spiti_mike.pcapng'



if __name__ == "__main__":
    pcap_file = FILE_PATH

    sel = int(input("1: density analysis\n2: performance analysis\n"))
    if (sel == 1):
        parser = Parser(pcap_file)
        results = parser.parse_pcap(density = True)
        monitor = DataMonitor(results)
        visualizer = Visualizer()
        analyzer = Analyzer()
        density_data = monitor.get_density_data()
        
        # generate combined plot
        visualizer.plot_density_metrics(density_data)
        visualizer.display_density_cli_metrics(density_data)
    elif (sel == 2):
        parser = Parser(pcap_file)
        results = parser.parse_pcap( density= False)
        monitor = DataMonitor(results)
        visualizer = Visualizer()
        analyzer = Analyzer()
        # performance analysis
        performance_data = monitor.get_performance_data(verbose=1)
        analyzed_data = analyzer.performance_analysis(performance_data)    
        visualizer.plot_throughput_stats(performance_data)
        visualizer.plot_dataframe_entries(analyzed_data['Data Frame'])
        visualizer.plot_rolling_average(analyzed_data['Data Frame'])
    else:
        print("Wrong input")

