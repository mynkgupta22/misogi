import React from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Grid,
  Paper,
  Typography,
} from '@mui/material';

interface ChunkingStrategyProps {
  strategy: string;
  chunkSize: number;
  overlap: number;
  onStrategyChange: (strategy: string) => void;
  onChunkSizeChange: (size: number) => void;
  onOverlapChange: (overlap: number) => void;
}

const strategies = [
  {
    value: 'fixed',
    label: 'Fixed Size',
    description: 'Splits text into chunks of fixed size with specified overlap'
  },
  {
    value: 'sentence',
    label: 'Sentence-based',
    description: 'Splits text by sentences while maintaining chunk size constraints'
  },
  {
    value: 'paragraph',
    label: 'Paragraph-based',
    description: 'Splits by paragraphs, combining small ones and splitting large ones'
  },
  {
    value: 'sliding',
    label: 'Sliding Window',
    description: 'Uses a sliding window approach with fixed overlap'
  }
];

const ChunkingStrategy: React.FC<ChunkingStrategyProps> = ({
  strategy,
  chunkSize,
  overlap,
  onStrategyChange,
  onChunkSizeChange,
  onOverlapChange
}) => {
  const selectedStrategy = strategies.find(s => s.value === strategy);

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Chunking Strategy</InputLabel>
            <Select
              value={strategy}
              label="Chunking Strategy"
              onChange={(e) => onStrategyChange(e.target.value)}
            >
              {strategies.map((s) => (
                <MenuItem key={s.value} value={s.value}>
                  {s.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        {selectedStrategy && (
          <Grid item xs={12}>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              {selectedStrategy.description}
            </Typography>
          </Grid>
        )}

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            type="number"
            label="Chunk Size"
            value={chunkSize}
            onChange={(e) => onChunkSizeChange(Number(e.target.value))}
            InputProps={{ inputProps: { min: 100, max: 2000 } }}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            type="number"
            label="Overlap Size"
            value={overlap}
            onChange={(e) => onOverlapChange(Number(e.target.value))}
            InputProps={{ inputProps: { min: 0, max: chunkSize - 50 } }}
          />
        </Grid>
      </Grid>
    </Paper>
  );
};

export default ChunkingStrategy; 