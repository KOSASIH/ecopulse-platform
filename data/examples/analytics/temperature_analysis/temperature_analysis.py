import pandas as pd

def analyze_temperature(data):
	# Calculate average temperature
	avg_temp = data['temperature_celsius'].mean()
	return avg_temp

if __name__ == '__main__':
	data = pd.read_csv('temperature_data.csv')
	avg_temp = analyze_temperature(data)
	print(f'Average temperature: {avg_temp:.2f}°C')
