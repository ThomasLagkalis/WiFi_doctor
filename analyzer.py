


class Analyzer:

    def __init__(self):

        """
        Analyzer provides insights about the throughput performance. Why is throughput good or bad?

        """

    def performance_analysis(self, data):
        """
        data: a dictionary with the data frame and the throughput metrics from the data monitor.

        returns a dictionary with grouped by performance metrics
        """

        df = data['data frame']

        phy_count = df.groupby(['PHY Type']).size()
        mcs_indexes_count = df.groupby(['MCS Index']).size()
        bandwidth_count = df.groupby(['Bandwidth']).size()
        shortgi_count = df.groupby(['Short Gi']).size()
        rssi_count = df.groupby(['Signal Strength (dBm)']).size()
        streams_count = df.groupby(['Spatial Streams']).size()
        rate_gap_count = df.groupby(['Rate Gap']).size()

        result = {
            'Data Frame': df,
            'PHY count': phy_count.to_dict(),
            'mcs cound': mcs_indexes_count.to_dict(),
            'bandwidth count': bandwidth_count.to_dict(),
            'short_gi count': shortgi_count.to_dict(),
            'rssi count': rssi_count.to_dict(),
            'streams count': streams_count.to_dict(),
            'rate gap count': rate_gap_count.to_dict()
                }

        print("\nPHY Type count: ")
        print(phy_count.to_dict())
        print("\nBandwidth count: ")
        print(bandwidth_count.to_dict())
        print("\nShort GI count: ")
        print(shortgi_count.to_dict())
        print("\nMCS index count: ")
        print(mcs_indexes_count.to_dict())
        print("\nRSSI count: ")
        print(rssi_count.to_dict())
        print("\nSpatial Streams count: ")
        print(streams_count.to_dict())
        print("\nRate Gap count: ")
        print(rate_gap_count.to_dict())
        print()

        return result
