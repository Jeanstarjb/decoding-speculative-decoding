import React from 'react';
import { CssBaseline, Container, Typography, Grid } from '@mui/material';
import MetricsCard from './components/MetricsCard';
import MetricsChart from './components/MetricsChart';

function App() {
  return (
    <>
      <CssBaseline />
      <Container maxWidth="lg">
        <Typography variant="h3" align="center" gutterBottom style={{ marginTop: '20px', fontWeight: 'bold', color: '#1976d2' }}>
          System Performance Dashboard
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} sm={6} md={4}>
            <MetricsCard title="CPU Usage" metricEndpoint="/metrics/cpu" />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <MetricsCard title="Memory Usage" metricEndpoint="/metrics/memory" />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <MetricsCard title="Request Rate" metricEndpoint="/metrics/requests" />
          </Grid>
        </Grid>
        <Typography variant="h5" align="center" style={{ marginTop: '40px', fontWeight: 'bold', color: '#1976d2' }}>
          Performance Trends
        </Typography>
        <MetricsChart />
      </Container>
    </>
  );
}

export default App;