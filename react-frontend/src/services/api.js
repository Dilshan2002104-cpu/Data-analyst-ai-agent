import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

// Create axios instance
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Authentication API
export const authAPI = {
    register: async (email, password, displayName) => {
        const response = await apiClient.post('/api/auth/register', {
            email,
            password,
            displayName,
        });
        return response.data;
    },

    login: async (email, password) => {
        const response = await apiClient.post('/api/auth/login', {
            email,
            password,
        });
        return response.data;
    },

    getUser: async (uid) => {
        const response = await apiClient.get(`/api/auth/user/${uid}`);
        return response.data;
    },

    verifyToken: async (token) => {
        const response = await apiClient.post('/api/auth/verify', null, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data;
    },
};

// Dataset API
export const datasetAPI = {
    upload: async (file, userId) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('userId', userId);

        const response = await apiClient.post('/api/datasets/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    list: async (userId) => {
        const response = await apiClient.get(`/api/datasets?userId=${userId}`);
        return response.data;
    },

    get: async (id) => {
        const response = await apiClient.get(`/api/datasets/${id}`);
        return response.data;
    },

    delete: async (id) => {
        const response = await apiClient.delete(`/api/datasets/${id}`);
        return response.data;
    },
};

// Query API
export const queryAPI = {
    send: async (datasetId, query, userId) => {
        const response = await apiClient.post('/api/query', {
            datasetId,
            query,
            userId,
        });
        return response.data;
    },

    getHistory: async (datasetId) => {
        const response = await apiClient.get(`/api/query/history/${datasetId}`);
        return response.data;
    },

    health: async () => {
        const response = await apiClient.get('/api/query/health');
        return response.data;
    },
};

export default apiClient;
