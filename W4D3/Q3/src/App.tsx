import { useState } from 'react';
import { Container, Typography, Box, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import PdfUploader from './components/PdfUploader';
import ChunkingStrategy from './components/ChunkingStrategy';
import ChunkVisualization from './components/ChunkVisualization';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  const [extractedText, setExtractedText] = useState<string>('');
  const [strategy, setStrategy] = useState<string>('fixed');
  const [chunkSize, setChunkSize] = useState<number>(500);
  const [overlap, setOverlap] = useState<number>(50);
  const [chunks, setChunks] = useState<string[]>([]);
  const [metadata, setMetadata] = useState<any>(null);

  const handlePdfUpload = (text: string) => {
    setExtractedText(text);
    processChunks(text, strategy, chunkSize, overlap);
  };

  const processChunks = async (text: string, strategy: string, chunkSize: number, overlap: number) => {
    try {
      const response = await fetch('http://localhost:8000/chunk', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          strategy,
          chunk_size: chunkSize,
          overlap,
        }),
      });

      const data = await response.json();
      if (data.error) {
        alert(data.error);
        return;
      }

      setChunks(data.chunks);
      setMetadata(data.metadata);
    } catch (error) {
      console.error('Error processing chunks:', error);
      alert('Error processing text chunks. Please try again.');
    }
  };

  const handleStrategyChange = (newStrategy: string) => {
    setStrategy(newStrategy);
    if (extractedText) {
      processChunks(extractedText, newStrategy, chunkSize, overlap);
    }
  };

  const handleChunkSizeChange = (newSize: number) => {
    setChunkSize(newSize);
    if (extractedText) {
      processChunks(extractedText, strategy, newSize, overlap);
    }
  };

  const handleOverlapChange = (newOverlap: number) => {
    setOverlap(newOverlap);
    if (extractedText) {
      processChunks(extractedText, strategy, chunkSize, newOverlap);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            RAG Chunking Strategy Visualizer
          </Typography>
          
          <PdfUploader onPdfUpload={handlePdfUpload} />
          
          {extractedText && (
            <>
              <ChunkingStrategy
                strategy={strategy}
                chunkSize={chunkSize}
                overlap={overlap}
                onStrategyChange={handleStrategyChange}
                onChunkSizeChange={handleChunkSizeChange}
                onOverlapChange={handleOverlapChange}
              />
              
              {chunks.length > 0 && metadata && (
                <ChunkVisualization chunks={chunks} metadata={metadata} />
              )}
            </>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 