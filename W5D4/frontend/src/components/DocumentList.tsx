import React, { useState, useEffect } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  IconButton,
  useToast,
  Text,
  Flex,
  Input,
  Button,
} from '@chakra-ui/react';
import { DeleteIcon, DownloadIcon, ViewIcon } from '@chakra-ui/icons';
import { format } from 'date-fns';
import { useAuth } from '../hooks/useAuth';

interface Document {
  id: number;
  title: string;
  file_type: string;
  created_at: string;
  updated_at: string;
}

export const DocumentList: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const { token } = useAuth();
  const toast = useToast();

  const fetchDocuments = async () => {
    try {
      const response = await fetch('/api/v1/my-documents', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      }
    } catch (error) {
      toast({
        title: 'Error fetching documents',
        status: 'error',
        duration: 3000,
      });
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [token]);

  const handleDelete = async (id: number) => {
    try {
      const response = await fetch(`/api/v1/documents/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        setDocuments(docs => docs.filter(doc => doc.id !== id));
        toast({
          title: 'Document deleted successfully',
          status: 'success',
          duration: 3000,
        });
      }
    } catch (error) {
      toast({
        title: 'Error deleting document',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const filteredDocuments = documents.filter(doc =>
    doc.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box>
      <Flex mb={4} gap={4}>
        <Input
          placeholder="Search documents..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button colorScheme="blue" onClick={() => window.location.href = '/upload'}>
          Upload New
        </Button>
      </Flex>

      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Title</Th>
            <Th>Type</Th>
            <Th>Created</Th>
            <Th>Updated</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {filteredDocuments.map((doc) => (
            <Tr key={doc.id}>
              <Td>{doc.title}</Td>
              <Td>{doc.file_type}</Td>
              <Td>{format(new Date(doc.created_at), 'MMM d, yyyy')}</Td>
              <Td>{format(new Date(doc.updated_at), 'MMM d, yyyy')}</Td>
              <Td>
                <IconButton
                  aria-label="View document"
                  icon={<ViewIcon />}
                  mr={2}
                  onClick={() => window.location.href = `/viewer/${doc.id}`}
                />
                <IconButton
                  aria-label="Download document"
                  icon={<DownloadIcon />}
                  mr={2}
                  onClick={() => window.location.href = `/api/v1/documents/${doc.id}/download`}
                />
                <IconButton
                  aria-label="Delete document"
                  icon={<DeleteIcon />}
                  colorScheme="red"
                  onClick={() => handleDelete(doc.id)}
                />
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      {filteredDocuments.length === 0 && (
        <Text mt={4} textAlign="center">No documents found</Text>
      )}
    </Box>
  );
}; 