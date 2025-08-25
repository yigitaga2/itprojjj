// Enhanced API client for the School Feedback Platform

class ApiClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };
    }

    /**
     * Get authorization headers
     */
    getAuthHeaders() {
        const token = AuthHelpers.getToken();
        if (token) {
            return {
                ...this.defaultHeaders,
                'Authorization': `Bearer ${token}`
            };
        }
        return this.defaultHeaders;
    }

    /**
     * Make HTTP request with error handling
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: this.getAuthHeaders(),
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            // Handle authentication errors
            if (response.status === 401 || response.status === 403) {
                AuthHelpers.handleAuthError({ status: response.status });
                throw new Error('Authentication failed');
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || `HTTP error! status: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error(`API request failed: ${endpoint}`, error);
            throw error;
        }
    }

    /**
     * GET request
     */
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    /**
     * POST request
     */
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * PUT request
     */
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }

    // Specific API methods
    
    /**
     * Login user
     */
    async login(username, password) {
        const response = await this.post('/auth/login', { username, password });
        if (response.access_token) {
            AuthHelpers.setToken(response.access_token);
        }
        return response;
    }

    /**
     * Get current user info
     */
    async getCurrentUser() {
        return this.get('/auth/me');
    }

    /**
     * Submit feedback
     */
    async submitFeedback(feedbackData) {
        return this.post('/feedback', feedbackData);
    }

    /**
     * Get feedback list
     */
    async getFeedback(filters = {}) {
        const params = new URLSearchParams(filters);
        return this.get(`/feedback?${params}`);
    }

    /**
     * Get analytics data
     */
    async getAnalytics() {
        return this.get('/analytics');
    }

    /**
     * Get categories
     */
    async getCategories() {
        return this.get('/categories');
    }

    /**
     * Get subjects
     */
    async getSubjects() {
        return this.get('/subjects');
    }

    /**
     * Test sentiment analysis
     */
    async testSentiment(text) {
        return this.get(`/test-sentiment?text=${encodeURIComponent(text)}`);
    }
}

// Create global API client instance
const apiClient = new ApiClient();
