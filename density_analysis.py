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
		df = pd.DataFrame(data, columns=['BSSID', 'Transmitter MAC', 'PHY Type', 'Channel', 'Frequency', 'Signal Strength (dBm)', 'Signal/Noise Ratio']).set_index(['Transmitter MAC'])
		print(df)

