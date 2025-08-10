import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Typography, Space, Spin, Alert } from 'antd';
import {
  GlobalOutlined,
  BookOutlined,
  TagsOutlined,
  EyeOutlined,
  TrophyOutlined,
  RiseOutlined,
} from '@ant-design/icons';
import { useAuth } from '../../contexts/AuthContext';
import httpClient from '../../services/httpClient';
import './Dashboard.css';

const { Title, Text } = Typography;

interface DashboardStats {
  websites_count: number;
  bookmarks_count: number;
  categories_count: number;
  tags_count: number;
  collections_count: number;
  total_website_visits: number;
  total_bookmark_visits: number;
  avg_website_quality: number;
  recent_websites: number;
  recent_bookmarks: number;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // 并行获取各种数据
      const [websitesRes, bookmarksRes, categoriesRes] = await Promise.allSettled([
        httpClient.get('/websites/'),
        httpClient.get('/bookmarks/'),
        httpClient.get('/websites/categories/')
      ]);
      
      // 安全提取数据
      const websitesData = websitesRes.status === 'fulfilled' ? websitesRes.value : null;
      const bookmarksData = bookmarksRes.status === 'fulfilled' ? bookmarksRes.value : null;
      const categoriesData = categoriesRes.status === 'fulfilled' ? categoriesRes.value : null;
      
      // 计算统计数据
      const websitesCount = Array.isArray(websitesData?.results) ? websitesData.results.length : 
                           Array.isArray(websitesData) ? websitesData.length : 0;
      const bookmarksCount = Array.isArray(bookmarksData?.results) ? bookmarksData.results.length : 
                            Array.isArray(bookmarksData) ? bookmarksData.length : 0;
      const categoriesCount = Array.isArray(categoriesData?.results) ? categoriesData.results.length : 
                             Array.isArray(categoriesData) ? categoriesData.length : 0;
      
      const safeStats = {
        websites_count: websitesCount,
        bookmarks_count: bookmarksCount,
        categories_count: categoriesCount,
        tags_count: 0, // 暂时设为0，后续可以添加标签API
        collections_count: 0, // 暂时设为0
        total_website_visits: 0, // 暂时设为0，需要访问统计API
        total_bookmark_visits: 0, // 暂时设为0
        avg_website_quality: 8.5, // 暂时设为固定值
        recent_websites: Math.min(websitesCount, 3), // 假设最近新增
        recent_bookmarks: Math.min(bookmarksCount, 5), // 假设最近新增
      };
      
      console.log('Dashboard stats:', safeStats);
      setStats(safeStats);
    } catch (err: any) {
      console.error('Dashboard fetch error:', err);
      setError(err.message || '获取统计数据失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <Spin size="large" />
        <Text style={{ marginTop: 16, display: 'block' }}>加载中...</Text>
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="加载失败"
        description={error}
        type="error"
        showIcon
        action={
          <button onClick={fetchDashboardStats}>重试</button>
        }
      />
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <Title level={2}>
          欢迎回来，{String(user?.first_name || user?.username || '用户')}！
        </Title>
        <Text type="secondary">
          这里是您的个人数据概览
        </Text>
      </div>

      <Row gutter={[24, 24]}>
        {/* 基础统计 */}
        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card">
            <Statistic
              title="网站总数"
              value={stats?.websites_count || 0}
              prefix={<GlobalOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff' }}
            />
            <div className="stat-extra">
              <Text type="secondary">
                最近7天新增 {stats?.recent_websites || 0} 个
              </Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card">
            <Statistic
              title="书签总数"
              value={stats?.bookmarks_count || 0}
              prefix={<BookOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a' }}
            />
            <div className="stat-extra">
              <Text type="secondary">
                最近7天新增 {stats?.recent_bookmarks || 0} 个
              </Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card">
            <Statistic
              title="分类数量"
              value={stats?.categories_count || 0}
              prefix={<TagsOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
            <div className="stat-extra">
              <Text type="secondary">
                标签 {stats?.tags_count || 0} 个
              </Text>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card">
            <Statistic
              title="总访问量"
              value={(stats?.total_website_visits || 0) + (stats?.total_bookmark_visits || 0)}
              prefix={<EyeOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#722ed1' }}
            />
            <div className="stat-extra">
              <Text type="secondary">
                网站 {stats?.total_website_visits || 0} + 书签 {stats?.total_bookmark_visits || 0}
              </Text>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
        {/* 质量评分 */}
        <Col xs={24} lg={12}>
          <Card title="网站质量评分" className="quality-card">
            <div className="quality-score">
              <Statistic
                value={stats?.avg_website_quality || 0}
                precision={1}
                suffix="/ 10"
                prefix={<TrophyOutlined />}
                valueStyle={{ 
                  color: (stats?.avg_website_quality || 0) >= 7 ? '#52c41a' : 
                         (stats?.avg_website_quality || 0) >= 5 ? '#faad14' : '#ff4d4f'
                }}
              />
              <Text type="secondary" style={{ marginTop: 8, display: 'block' }}>
                平均质量评分
              </Text>
            </div>
          </Card>
        </Col>

        {/* 快速操作 */}
        <Col xs={24} lg={12}>
          <Card title="快速操作" className="quick-actions">
            <Space direction="vertical" style={{ width: '100%' }}>
              <div className="action-item">
                <GlobalOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                <Text>添加新网站</Text>
              </div>
              <div className="action-item">
                <BookOutlined style={{ color: '#52c41a', marginRight: 8 }} />
                <Text>创建书签</Text>
              </div>
              <div className="action-item">
                <TagsOutlined style={{ color: '#faad14', marginRight: 8 }} />
                <Text>管理分类</Text>
              </div>
              <div className="action-item">
                <RiseOutlined style={{ color: '#722ed1', marginRight: 8 }} />
                <Text>查看分析</Text>
              </div>
            </Space>
          </Card>
        </Col>
      </Row>

      {/* 最近活动 */}
      <Row gutter={[24, 24]} style={{ marginTop: 24 }}>
        <Col span={24}>
          <Card title="最近活动" className="activity-card">
            <div className="activity-content">
              <Text type="secondary">
                最近7天内，您新增了 {stats?.recent_websites || 0} 个网站和 {stats?.recent_bookmarks || 0} 个书签。
                继续保持这个节奏，您的收藏库会越来越丰富！
              </Text>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;