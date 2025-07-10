import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Paper,
  Typography,
  CircularProgress,
  Chip,
} from '@mui/material';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

interface QueryResponse {
  intent: string;
  confidence: number;
  response: string;
  context: string;
  metrics: {
    response_relevance: number;
    context_utilization: number;
    intent_confidence: number;
    processing_time: number;
  };
}

const ChatInterface: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await axios.post<QueryResponse>('http://localhost:8000/api/query', {
        text: query,
      });

      setResponse(result.data);
    } catch (err) {
      setError('Error processing your request. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Ask a question"
            variant="outlined"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading || !query.trim()}
          >
            {loading ? <CircularProgress size={24} /> : 'Send'}
          </Button>
        </form>
      </Paper>

      {error && (
        <Paper elevation={3} sx={{ p: 3, mb: 3, bgcolor: '#ffebee' }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      )}

      {response && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Box sx={{ mb: 2 }}>
            <Chip
              label={`Intent: ${response.intent}`}
              color="primary"
              sx={{ mr: 1 }}
            />
            <Chip
              label={`Confidence: ${(response.confidence * 100).toFixed(1)}%`}
              color={response.confidence > 0.7 ? 'success' : 'warning'}
            />
          </Box>

          <Typography variant="h6" gutterBottom>
            Response:
          </Typography>
          <Box sx={{ mb: 3 }}>
            <ReactMarkdown>{response.response}</ReactMarkdown>
          </Box>

          <Typography variant="h6" gutterBottom>
            Metrics:
          </Typography>
          <Box>
            <Typography variant="body2">
              Response Relevance: {(response.metrics.response_relevance * 100).toFixed(1)}%
            </Typography>
            <Typography variant="body2">
              Context Utilization: {(response.metrics.context_utilization * 100).toFixed(1)}%
            </Typography>
            <Typography variant="body2">
              Processing Time: {response.metrics.processing_time.toFixed(2)}s
            </Typography>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default ChatInterface; 