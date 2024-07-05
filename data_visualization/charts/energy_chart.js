// Import libraries
import Chart from 'chart.js';
import * as d3 from 'd3-array';
import Highcharts from 'highcharts';

// Create energy consumption chart using Chart.js
function createChartJsChart(data) {
  const ctx = document.getElementById('chart-js-chart').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(d => d.date),
      datasets: [{
        label: 'Energy Consumption',
        data: data.map(d => d.energy_consumption),
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Energy Consumption Chart'
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// Create energy consumption chart using D3.js
function createD3Chart(data) {
  const margin = { top: 20, right: 20, bottom: 30, left: 40 };
  const width = 500 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;

  const xScale = d3.scaleTime()
   .domain(d3.extent(data, d => d.date))
   .range([0, width]);

  const yScale = d3.scaleLinear()
   .domain([0, d3.max(data, d => d.energy_consumption)])
   .range([height, 0]);

  const line = d3.line()
   .x(d => xScale(d.date))
   .y(d => yScale(d.energy_consumption));

  const svg = d3.select('#d3-chart')
   .append('svg')
   .attr('width', width + margin.left + margin.right)
   .attr('height', height + margin.top + margin.bottom)
   .append('g')
   .attr('transform', `translate(${margin.left}, ${margin.top})`);

  svg.append('path')
   .datum(data)
   .attr('class', 'line')
   .attr('d', line);

  svg.append('g')
   .attr('class', 'axis')
   .attr('transform', `translate(0, ${height})`)
   .call(d3.axisBottom(xScale));

  svg.append('g')
   .attr('class', 'axis')
   .call(d3.axisLeft(yScale));
}

// Create energy consumption chart using Highcharts
function createHighchartsChart(data) {
  Highcharts.chart('highcharts-chart', {
    chart: {
      type: 'line'
    },
    title: {
      text: 'Energy Consumption Chart'
    },
    xAxis: {
      type: 'datetime',
      labels: {
        format: '{value:%Y-%m-%d}'
      }
    },
    yAxis: {
      title: {
        text: 'Energy Consumption (kWh)'
      }
    },
    series: [{
      data: data.map(d => [d.date, d.energy_consumption]),
      name: 'Energy Consumption'
    }]
  });
}

// Example usage
const data = [
  { date: '2022-01-01', energy_consumption: 100 },
  { date: '2022-01-02', energy_consumption: 120 },
  { date: '2022-01-03', energy_consumption: 110 },
  //...
];

createChartJsChart(data);
createD3Chart(data);
createHighchartsChart(data);
