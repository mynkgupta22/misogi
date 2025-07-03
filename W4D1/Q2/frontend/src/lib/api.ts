import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const auth = {
  register: (data: { email: string; username: string; password: string }) =>
    api.post('/auth/register', data),
  login: (data: { username: string; password: string }) =>
    api.post('/auth/token', new URLSearchParams(data)),
};

// Products endpoints
export const products = {
  getAll: (params?: {
    category?: string;
    subcategory?: string;
    min_price?: number;
    max_price?: number;
    min_rating?: number;
  }) => api.get('/products', { params }),
  getCategories: () => api.get('/products/categories'),
  trackInteraction: (productId: string, interactionType: string) =>
    api.post(`/products/interaction/${productId}`, { interaction_type: interactionType }),
};

// Recommendations endpoints
export const recommendations = {
  getSimilar: (productId: string, n?: number) =>
    api.get(`/recommendations/similar/${productId}`, { params: { n } }),
  getPersonalized: (n?: number) =>
    api.get('/recommendations/personalized', { params: { n } }),
  getPopular: (n?: number) =>
    api.get('/recommendations/popular', { params: { n } }),
};

export default api; 