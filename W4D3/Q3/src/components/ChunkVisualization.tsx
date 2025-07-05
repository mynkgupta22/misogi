import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Divider,
} from '@mui/material';

interface ChunkVisualizationProps {
  chunks: string[];
  metadata: {
    total_chunks: number;
    average_chunk_size: number;
    strategy: string;
  };
}

const ChunkVisualization: React.FC<ChunkVisualizationProps> = ({ chunks, metadata }) => {
  return (
    <Grid container spacing={3}>
      {/* Metadata Display */}
      <Grid item xs={12}>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Chunking Results
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <Typography variant="body2" color="text.secondary">
                Total Chunks:
              </Typography>
              <Typography variant="h6">
                {metadata.total_chunks}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="body2" color="text.secondary">
                Average Chunk Size:
              </Typography>
              <Typography variant="h6">
                {Math.round(metadata.average_chunk_size)} characters
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="body2" color="text.secondary">
                Strategy:
              </Typography>
              <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
                {metadata.strategy}
              </Typography>
            </Grid>
          </Grid>
        </Paper>
      </Grid>

      {/* Chunks Display */}
      <Grid item xs={12}>
        <Box sx={{ maxHeight: '600px', overflow: 'auto' }}>
          {chunks.map((chunk, index) => (
            <Card key={index} sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                  Chunk {index + 1} ({chunk.length} characters)
                </Typography>
                <Divider sx={{ my: 1 }} />
                <Typography
                  variant="body2"
                  sx={{
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    fontFamily: 'monospace'
                  }}
                >
                  {chunk}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Grid>
    </Grid>
  );
};

export default ChunkVisualization; 