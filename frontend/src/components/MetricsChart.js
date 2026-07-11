import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

function MetricsChart() {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await axios.get('/metrics/trends');
        const { timestamps, values } = response.data;
        setChartData({
          labels: timestamps,
          datasets: [
            {
              label: 'Performance Over Time',
              data: values,
              fill: false,
              backgroundColor: '#1976d2',
              borderColor: '#1976d2',
              tension: 0.4,
            },
          ],
        });
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    };

    fetchChartData();
  }, []);

  if (!chartData) {
    return <p>Loading chart...</p>;
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <Line
        data={chartData}
        options={{
          responsive: true,
          plugins: {
            legend: {
              display: true,
              position: 'top',
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Time',
              },
            },
            y: {
              title: {
                display: true,
                text: 'Value',
              },
            },
          },
        }}
      />
    </div>
  );
}

export default MetricsChart;