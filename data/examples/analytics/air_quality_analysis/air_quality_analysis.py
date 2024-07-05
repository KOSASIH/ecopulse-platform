import pandas as pd

def analyze_air_quality(data):
	# Calculate average PM2.5 level
	avg_pm25 = data['pm25'].mean()
	return avg_pm25

if __name__ == '__main__':
	data = pd.read_csv('air_quality_data.csv')
	avg_pm25 = analyze_air_quality(data)
	print(f'Average PM2.5 level: {avg_pm25:.2f} μg/m³')
