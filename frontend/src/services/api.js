const API_BASE_URL = 'http://localhost:5000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth endpoints
  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // Profile endpoints
  async getProfile() {
    return this.request('/profile/profile');
  }

  async updateProfile(profileData) {
    return this.request('/profile/profile', {
      method: 'POST',
      body: JSON.stringify(profileData),
    });
  }

  // Pairing endpoints
  async getCurrentPairing() {
    return this.request('/pairing/my-pairing');
  }

  async getPairingHistory(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/pairing/history${queryString ? `?${queryString}` : ''}`);
  }

  // Quiz endpoints
  async getQuizResult() {
    return this.request('/quiz/my-quiz');
  }

  async submitQuiz(quizData) {
    return this.request('/quiz/submit', {
      method: 'POST',
      body: JSON.stringify(quizData),
    });
  }

  // Admin endpoints
  async getUsers(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/admin/users${queryString ? `?${queryString}` : ''}`);
  }

  async createNewWeekPairings(data = {}) {
    return this.request('/pairing/new-week', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export default new ApiService();