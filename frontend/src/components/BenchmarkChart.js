import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Card, CardContent, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

function BenchmarkChart() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBenchmarkData = async () => {
      try {
        const response = await axios.get('/metrics/benchmark');
        const { timestamps, avgResponseTimes, p95ResponseTimes } = response.data;
        setChartData({
          labels: timestamps,
          datasets: [
            {
              label: 'Average Response Time (s)',
              data: avgResponseTimes,
              fill: false,
              backgroundColor: '#4caf50',
              borderColor: '#4caf50',
              tension: 0.4,
            },
            {
              label: '95th Percentile Response Time (s)',
              data: p95ResponseTimes,
              fill: false,
              backgroundColor: '#f44336',
              borderColor: '#f44336',
              tension: 0.4,
            },
          ],
        });
      } catch (error) {
        console.error('Error fetching benchmark data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBenchmarkData();
  }, []);

  return (
    <Card elevation={3} style={{ borderRadius: '12px', marginTop: '20px' }}>
      <CardContent>
        <Typography variant="h6" align="center" gutterBottom>
          Benchmark Performance
        </Typography>
        {loading ? (
          <CircularProgress style={{ display: 'block', margin: '20px auto' }} />
        ) : (
          <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
        )}
      </CardContent>
    </Card>
  );
}

export default BenchmarkChart;