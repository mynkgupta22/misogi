import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { Login } from './pages/Login';
import { DocumentList } from './components/DocumentList';
import { DocumentViewer } from './components/DocumentViewer';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return token ? <>{children}</> : <Navigate to="/login" />;
};

const App: React.FC = () => {
  return (
    <ChakraProvider>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/documents"
              element={
                <PrivateRoute>
                  <DocumentList />
                </PrivateRoute>
              }
            />
            <Route
              path="/viewer/:id"
              element={
                <PrivateRoute>
                  <DocumentViewer />
                </PrivateRoute>
              }
            />
            <Route path="/" element={<Navigate to="/documents" />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ChakraProvider>
  );
};

export default App; 