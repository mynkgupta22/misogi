import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';

const Header: React.FC = () => {
  return (
    <AppBar position="static" sx={{ mb: 4 }}>
      <Toolbar>
        <Box display="flex" alignItems="center">
          <Typography variant="h6" component="div">
            SaaS Support System
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 