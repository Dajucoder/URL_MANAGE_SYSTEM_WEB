import axios from 'axios';
import { API_BASE_URL } from '../config/constants';

const API_URL = `${API_BASE_URL}/users`;

export interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    avatar?: string;
    bio?: string;
    theme: string;
    language: string;
  };
}

export interface RegisterResponse {
  message: string;
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
  };
  tokens: {
    access: string;
    refresh: string;
  };
}

class AuthService {
  async login(username: string, password: string): Promise<LoginResponse> {
    const response = await axios.post(`${API_URL}/login/`, {
      username,
      password,
    });
    return response.data;
  }

  async register(userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name?: string;
    last_name?: string;
  }): Promise<RegisterResponse> {
    const response = await axios.post(`${API_URL}/register/`, userData);
    return response.data;
  }

  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await axios.post(`${API_URL}/logout/`, {
          refresh_token: refreshToken,
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
      } catch (error) {
        console.error('服务器退出登录失败:', error);
      }
    }
  }

  async getCurrentUser() {
    const response = await axios.get(`${API_URL}/info/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
    return response.data;
  }

  async updateProfile(userData: any) {
    const response = await axios.patch(`${API_URL}/profile/`, userData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
    return response.data;
  }

  async changePassword(oldPassword: string, newPassword: string) {
    const response = await axios.post(`${API_URL}/change-password/`, {
      old_password: oldPassword,
      new_password: newPassword,
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    });
    return response.data;
  }

  async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await axios.post(`${API_URL}/token/refresh/`, {
      refresh: refreshToken,
    });

    const newAccessToken = response.data.access;
    localStorage.setItem('access_token', newAccessToken);
    
    return newAccessToken;
  }
}

export const authService = new AuthService();