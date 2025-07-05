import React from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, Paper } from '@mui/material';

interface PdfUploaderProps {
  onPdfUpload: (text: string) => void;
}

const PdfUploader: React.FC<PdfUploaderProps> = ({ onPdfUpload }) => {
  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      if (data.error) {
        alert(data.error);
        return;
      }
      
      onPdfUpload(data.text);
    } catch (error) {
      console.error('Error uploading PDF:', error);
      alert('Error uploading PDF. Please try again.');
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  });

  return (
    <Paper
      elevation={3}
      sx={{
        p: 3,
        mb: 3,
        backgroundColor: '#f5f5f5'
      }}
    >
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed #999',
          borderRadius: 2,
          p: 3,
          textAlign: 'center',
          cursor: 'pointer',
          '&:hover': {
            borderColor: 'primary.main',
            backgroundColor: 'rgba(0, 0, 0, 0.04)'
          }
        }}
      >
        <input {...getInputProps()} />
        <Typography variant="h6" color="primary" gutterBottom>
          {isDragActive ? 'Drop the PDF here' : 'Drag & drop a PDF file here'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          or click to select a file
        </Typography>
      </Box>
    </Paper>
  );
};

export default PdfUploader; 