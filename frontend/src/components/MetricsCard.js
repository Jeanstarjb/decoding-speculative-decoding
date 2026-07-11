import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

function MetricsCard({ title, metricEndpoint }) {
  const [value, setValue] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get(metricEndpoint);
        setValue(response.data.value);
      } catch (error) {
        console.error(`Error fetching ${title}:`, error);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, [metricEndpoint]);

  return (
    <Card elevation={3} style={{ borderRadius: '12px' }}>
      <CardContent>
        <Typography variant="h6" align="center" gutterBottom style={{ fontWeight: 'bold', color: '#424242' }}>
          {title}
        </Typography>
        {loading ? (
          <CircularProgress style={{ display: 'block', margin: '0 auto' }} />
        ) : (
          <Typography variant="h4" align="center" style={{ color: '#1976d2' }}>
            {value}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

export default MetricsCard;