import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { message } from 'antd';
import { authService } from '../services/authService';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  avatar?: string;
  bio?: string;
  theme: string;
  language: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  register: (userData: RegisterData) => Promise<boolean>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => Promise<boolean>;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const isAuthenticated = !!user;

  // 初始化时检查用户登录状态
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        }
      } catch (error) {
        console.error('初始化认证失败:', error);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      setLoading(true);
      const response = await authService.login(username, password);
      
      // 保存令牌
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      
      // 设置用户信息，添加默认的theme和language属性
      setUser({
        ...response.user,
        theme: 'light',
        language: 'zh-CN'
      });
      
      message.success('登录成功');
      return true;
    } catch (error: any) {
      console.error('登录失败:', error);
      message.error(error.response?.data?.error || '登录失败');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: RegisterData): Promise<boolean> => {
    try {
      setLoading(true);
      const response = await authService.register(userData);
      
      // 保存令牌
      localStorage.setItem('access_token', response.tokens.access);
      localStorage.setItem('refresh_token', response.tokens.refresh);
      
      // 设置用户信息，添加默认的theme和language属性
      setUser({
        ...response.user,
        theme: 'light',
        language: 'zh-CN'
      });
      
      message.success('注册成功');
      return true;
    } catch (error: any) {
      console.error('注册失败:', error);
      message.error(error.response?.data?.error || '注册失败');
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    try {
      // 清除本地存储
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      // 清除用户状态
      setUser(null);
      
      message.success('已退出登录');
    } catch (error) {
      console.error('退出登录失败:', error);
    }
  };

  const updateUser = async (userData: Partial<User>): Promise<boolean> => {
    try {
      const updatedUser = await authService.updateProfile(userData);
      setUser(updatedUser);
      message.success('更新成功');
      return true;
    } catch (error: any) {
      console.error('更新用户信息失败:', error);
      message.error(error.response?.data?.error || '更新失败');
      return false;
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};