import React, { useState, useEffect } from 'react';
import {
  Card,
  Form,
  Input,
  Button,
  Avatar,
  Upload,
  Select,
  DatePicker,
  Typography,
  Space,
  message,
  Row,
  Col,
  Statistic,
} from 'antd';
import {
  UserOutlined,
  CameraOutlined,
  SaveOutlined,
  LockOutlined,
} from '@ant-design/icons';
import { useAuth } from '../../contexts/AuthContext';
import httpClient from '../../services/httpClient';
import { THEMES, LANGUAGES } from '../../config/constants';
import dayjs from 'dayjs';
import './Profile.css';

const { Title, Text } = Typography;
const { Option } = Select;

interface UserStats {
  total_bookmarks: number;
  total_visits: number;
  categories_count: number;
  tags_count: number;
  websites_count: number;
  collections_count: number;
  join_date: string;
}

const Profile: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [stats, setStats] = useState<UserStats | null>(null);

  useEffect(() => {
    if (user) {
      form.setFieldsValue({
        ...user,
        birth_date: (user as any).birth_date ? dayjs((user as any).birth_date) : null,
      });
      fetchUserStats();
    }
  }, [user, form]);

  const fetchUserStats = async () => {
    try {
      const data = await httpClient.get('/users/stats/');
      setStats(data);
    } catch (error) {
      console.error('获取用户统计失败:', error);
    }
  };

  const handleUpdateProfile = async (values: any) => {
    try {
      setLoading(true);
      const updateData = {
        ...values,
        birth_date: values.birth_date ? values.birth_date.format('YYYY-MM-DD') : null,
      };
      await updateUser(updateData);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async (values: any) => {
    try {
      setPasswordLoading(true);
      await httpClient.post('/users/change-password/', {
        old_password: values.old_password,
        new_password: values.new_password,
      });
      message.success('密码修改成功');
      passwordForm.resetFields();
    } catch (error: any) {
      message.error(error.response?.data?.error || '密码修改失败');
    } finally {
      setPasswordLoading(false);
    }
  };

  const handleAvatarUpload = async (file: File) => {
    try {
      const formData = new FormData();
      formData.append('avatar', file);
      
      const response = await httpClient.upload('/users/profile/', formData);
      await updateUser({ avatar: response.avatar });
      message.success('头像上传成功');
    } catch (error) {
      message.error('头像上传失败');
    }
    return false; // 阻止默认上传行为
  };

  return (
    <div className="profile-page">
      <div className="page-header">
        <Title level={2}>个人资料</Title>
        <Text type="secondary">管理您的个人信息和偏好设置</Text>
      </div>

      <Row gutter={[24, 24]}>
        {/* 用户统计 */}
        <Col span={24}>
          <Card title="数据统计" className="stats-card">
            <Row gutter={[16, 16]}>
              <Col xs={12} sm={8} md={4}>
                <Statistic
                  title="网站数量"
                  value={stats?.websites_count || 0}
                  prefix={<UserOutlined />}
                />
              </Col>
              <Col xs={12} sm={8} md={4}>
                <Statistic
                  title="书签数量"
                  value={stats?.total_bookmarks || 0}
                />
              </Col>
              <Col xs={12} sm={8} md={4}>
                <Statistic
                  title="分类数量"
                  value={stats?.categories_count || 0}
                />
              </Col>
              <Col xs={12} sm={8} md={4}>
                <Statistic
                  title="标签数量"
                  value={stats?.tags_count || 0}
                />
              </Col>
              <Col xs={12} sm={8} md={4}>
                <Statistic
                  title="收藏夹"
                  value={stats?.collections_count || 0}
                />
              </Col>
              <Col xs={12} sm={8} md={4}>
                <Statistic
                  title="总访问量"
                  value={stats?.total_visits || 0}
                />
              </Col>
            </Row>
          </Card>
        </Col>

        {/* 个人信息 */}
        <Col xs={24} lg={12}>
          <Card title="个人信息" className="profile-card">
            <div className="avatar-section">
              <Avatar
                size={80}
                src={String((user as any)?.avatar || '')}
                icon={<UserOutlined />}
              />
              <Upload
                accept="image/*"
                showUploadList={false}
                beforeUpload={handleAvatarUpload}
              >
                <Button icon={<CameraOutlined />} type="link">
                  更换头像
                </Button>
              </Upload>
            </div>

            <Form
              form={form}
              layout="vertical"
              onFinish={handleUpdateProfile}
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    name="first_name"
                    label="姓"
                  >
                    <Input placeholder="请输入姓" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    name="last_name"
                    label="名"
                  >
                    <Input placeholder="请输入名" />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                name="email"
                label="邮箱"
                rules={[
                  { required: true, message: '请输入邮箱' },
                  { type: 'email', message: '请输入有效的邮箱地址' }
                ]}
              >
                <Input placeholder="请输入邮箱" />
              </Form.Item>

              <Form.Item
                name="bio"
                label="个人简介"
              >
                <Input.TextArea
                  placeholder="介绍一下自己..."
                  rows={3}
                />
              </Form.Item>

              <Form.Item
                name="website"
                label="个人网站"
              >
                <Input placeholder="https://example.com" />
              </Form.Item>

              <Form.Item
                name="location"
                label="所在地"
              >
                <Input placeholder="请输入所在地" />
              </Form.Item>

              <Form.Item
                name="birth_date"
                label="生日"
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  icon={<SaveOutlined />}
                >
                  保存更改
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>

        {/* 偏好设置和密码修改 */}
        <Col xs={24} lg={12}>
          <Space direction="vertical" style={{ width: '100%' }} size="large">
            {/* 偏好设置 */}
            <Card title="偏好设置" className="preferences-card">
              <Form
                layout="vertical"
                initialValues={{
                  theme: (user as any)?.theme || THEMES.LIGHT,
                  language: (user as any)?.language || LANGUAGES.ZH_CN,
                }}
                onValuesChange={(changedValues) => {
                  updateUser(changedValues);
                }}
              >
                <Form.Item
                  name="theme"
                  label="主题"
                >
                  <Select>
                    <Option value={THEMES.LIGHT}>浅色主题</Option>
                    <Option value={THEMES.DARK}>深色主题</Option>
                  </Select>
                </Form.Item>

                <Form.Item
                  name="language"
                  label="语言"
                >
                  <Select>
                    <Option value={LANGUAGES.ZH_CN}>简体中文</Option>
                    <Option value={LANGUAGES.EN}>English</Option>
                  </Select>
                </Form.Item>
              </Form>
            </Card>

            {/* 修改密码 */}
            <Card title="修改密码" className="password-card">
              <Form
                form={passwordForm}
                layout="vertical"
                onFinish={handleChangePassword}
              >
                <Form.Item
                  name="old_password"
                  label="当前密码"
                  rules={[{ required: true, message: '请输入当前密码' }]}
                >
                  <Input.Password placeholder="请输入当前密码" />
                </Form.Item>

                <Form.Item
                  name="new_password"
                  label="新密码"
                  rules={[
                    { required: true, message: '请输入新密码' },
                    { min: 8, message: '密码至少8个字符' }
                  ]}
                >
                  <Input.Password placeholder="请输入新密码" />
                </Form.Item>

                <Form.Item
                  name="confirm_password"
                  label="确认新密码"
                  dependencies={['new_password']}
                  rules={[
                    { required: true, message: '请确认新密码' },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('new_password') === value) {
                          return Promise.resolve();
                        }
                        return Promise.reject(new Error('两次输入的密码不一致'));
                      },
                    }),
                  ]}
                >
                  <Input.Password placeholder="请再次输入新密码" />
                </Form.Item>

                <Form.Item>
                  <Button
                    type="primary"
                    htmlType="submit"
                    loading={passwordLoading}
                    icon={<LockOutlined />}
                  >
                    修改密码
                  </Button>
                </Form.Item>
              </Form>
            </Card>
          </Space>
        </Col>
      </Row>
    </div>
  );
};

export default Profile;