import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Heading,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  useToast,
  VStack,
  HStack,
} from '@chakra-ui/react';
import { ChevronDownIcon } from '@chakra-ui/icons';
import { useParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface DocumentMetadata {
  id: number;
  title: string;
  file_type: string;
  content?: string;
}

export const DocumentViewer: React.FC = () => {
  const [document, setDocument] = useState<DocumentMetadata | null>(null);
  const { id } = useParams<{ id: string }>();
  const { token } = useAuth();
  const toast = useToast();

  useEffect(() => {
    fetchDocument();
  }, [id, token]);

  const fetchDocument = async () => {
    try {
      const response = await fetch(`/api/v1/documents/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setDocument(data);
      }
    } catch (error) {
      toast({
        title: 'Error fetching document',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const handleExport = async (format: 'pdf' | 'docx' | 'md') => {
    try {
      const response = await fetch(`/api/v1/documents/${id}/export?format=${format}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${document?.title || 'document'}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      toast({
        title: 'Error exporting document',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const handleShare = async (platform: 'notion' | 'slack' | 'teams') => {
    try {
      const response = await fetch(`/api/v1/documents/${id}/share`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ platform }),
      });
      
      if (response.ok) {
        toast({
          title: `Shared to ${platform} successfully`,
          status: 'success',
          duration: 3000,
        });
      }
    } catch (error) {
      toast({
        title: 'Error sharing document',
        status: 'error',
        duration: 3000,
      });
    }
  };

  if (!document) {
    return <Box>Loading...</Box>;
  }

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={6} align="stretch">
        <HStack justify="space-between">
          <Heading size="lg">{document.title}</Heading>
          <HStack spacing={4}>
            <Menu>
              <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                Export As
              </MenuButton>
              <MenuList>
                <MenuItem onClick={() => handleExport('pdf')}>PDF</MenuItem>
                <MenuItem onClick={() => handleExport('docx')}>Word Document</MenuItem>
                <MenuItem onClick={() => handleExport('md')}>Markdown</MenuItem>
              </MenuList>
            </Menu>
            
            <Menu>
              <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                Share To
              </MenuButton>
              <MenuList>
                <MenuItem onClick={() => handleShare('notion')}>Notion</MenuItem>
                <MenuItem onClick={() => handleShare('slack')}>Slack</MenuItem>
                <MenuItem onClick={() => handleShare('teams')}>Microsoft Teams</MenuItem>
              </MenuList>
            </Menu>
          </HStack>
        </HStack>

        <Box
          p={6}
          borderWidth={1}
          borderRadius="lg"
          minH="500px"
          dangerouslySetInnerHTML={{ __html: document.content || '' }}
        />
      </VStack>
    </Container>
  );
}; 