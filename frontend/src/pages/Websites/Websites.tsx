import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Select,
  Tag,
  Avatar,
  Typography,
  Modal,
  Form,
  message,
  Popconfirm,
  Tooltip,
  Switch,
} from 'antd';
import {
  PlusOutlined,
  SearchOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  GlobalOutlined,
  StarOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import httpClient from '../../services/httpClient';
import { safeRender, safeRenderUrl, safeRenderDate, safeRenderNumber } from '../../utils/renderSafe';
import './Websites.css';

const { Title, Text } = Typography;
const { Option } = Select;

interface Website {
  id: number;
  title: string;
  url: string;
  description: string;
  favicon?: string;
  category_name?: string;
  tags_count: number;
  is_active: boolean;
  is_public: boolean;
  visit_count: number;
  quality_score: number;
  created_at: string;
  last_visited?: string;
}

interface Category {
  id: number;
  name: string;
  color: string;
}

const Websites: React.FC = () => {
  const [websites, setWebsites] = useState<Website[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingWebsite, setEditingWebsite] = useState<Website | null>(null);
  const [searchText, setSearchText] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<number | undefined>();
  const [form] = Form.useForm();

  useEffect(() => {
    fetchWebsites();
    fetchCategories();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchWebsites = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (searchText) params.search = searchText;
      if (selectedCategory) params.category = selectedCategory;
      
      const data = await httpClient.get('/websites/', { params });
      const websites = Array.isArray(data.results) ? data.results : Array.isArray(data) ? data : [];
      setWebsites(websites);
    } catch (error) {
      message.error('获取网站列表失败');
      setWebsites([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const data = await httpClient.get('/websites/categories/');
      const categories = Array.isArray(data.results) ? data.results : Array.isArray(data) ? data : [];
      setCategories(categories);
    } catch (error) {
      console.error('获取分类失败:', error);
      setCategories([]);
    }
  };

  const handleSearch = () => {
    fetchWebsites();
  };

  const handleAdd = () => {
    setEditingWebsite(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (website: Website) => {
    setEditingWebsite(website);
    form.setFieldsValue(website);
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await httpClient.delete(`/websites/${id}/`);
      message.success('删除成功');
      fetchWebsites();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingWebsite) {
        await httpClient.patch(`/websites/${editingWebsite.id}/`, values);
        message.success('更新成功');
      } else {
        await httpClient.post('/websites/', values);
        message.success('创建成功');
      }
      setModalVisible(false);
      fetchWebsites();
    } catch (error) {
      message.error(editingWebsite ? '更新失败' : '创建失败');
    }
  };

  const columns: ColumnsType<Website> = [
    {
      title: '网站',
      key: 'website',
      render: (_, record) => (
        <Space>
          <Avatar
            size="small"
            src={record.favicon}
            icon={<GlobalOutlined />}
          />
          <div>
            <div>
              <Text strong>{safeRender(record.title)}</Text>
              {record.quality_score >= 8 && (
                <StarOutlined style={{ color: '#faad14', marginLeft: 4 }} />
              )}
            </div>
            <Text type="secondary" style={{ fontSize: '12px' }}>
              {safeRenderUrl(record.url)}
            </Text>
          </div>
        </Space>
      ),
      width: 300,
    },
    {
      title: '分类',
      dataIndex: 'category_name',
      key: 'category',
      render: (category) => category ? <Tag color="blue">{safeRender(category)}</Tag> : '-',
      width: 120,
    },
    {
      title: '标签',
      dataIndex: 'tags_count',
      key: 'tags',
      render: (count) => (
        <Text type="secondary">{count || 0} 个标签</Text>
      ),
      width: 100,
    },
    {
      title: '访问量',
      dataIndex: 'visit_count',
      key: 'visits',
      render: (count) => safeRenderNumber(count),
      sorter: true,
      width: 100,
    },
    {
      title: '质量评分',
      dataIndex: 'quality_score',
      key: 'quality',
      render: (score) => {
        const numScore = Number(score);
        return !isNaN(numScore) && numScore > 0 ? (
          <Tag color={numScore >= 8 ? 'green' : numScore >= 6 ? 'blue' : numScore >= 4 ? 'orange' : 'red'}>
            {numScore.toFixed(1)}
          </Tag>
        ) : '-';
      },
      sorter: true,
      width: 100,
    },
    {
      title: '状态',
      key: 'status',
      render: (_, record) => (
        <Space>
          {record.is_active && <Tag color="green">活跃</Tag>}
          {record.is_public && <Tag color="blue">公开</Tag>}
        </Space>
      ),
      width: 120,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => safeRenderDate(date),
      sorter: true,
      width: 120,
    },
    {
      title: '操作',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Tooltip title="查看">
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => window.open(record.url, '_blank')}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定要删除这个网站吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Tooltip title="删除">
              <Button
                type="text"
                danger
                icon={<DeleteOutlined />}
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
      width: 120,
      fixed: 'right',
    },
  ];

  return (
    <div className="websites-page">
      <div className="page-header">
        <Title level={2}>网站管理</Title>
        <Text type="secondary">管理您收藏的网站</Text>
      </div>

      <Card>
        <div className="toolbar">
          <Space>
            <Input
              placeholder="搜索网站..."
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onPressEnter={handleSearch}
              style={{ width: 300 }}
            />
            <Select
              placeholder="选择分类"
              allowClear
              value={selectedCategory}
              onChange={setSelectedCategory}
              style={{ width: 150 }}
            >
              {categories.map(category => (
                <Option key={category.id} value={category.id}>
                  {category.name}
                </Option>
              ))}
            </Select>
            <Button onClick={handleSearch}>搜索</Button>
          </Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加网站
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={websites}
          loading={loading}
          rowKey="id"
          scroll={{ x: 1200 }}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 条记录`,
          }}
        />
      </Card>

      <Modal
        title={editingWebsite ? '编辑网站' : '添加网站'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="title"
            label="网站标题"
            rules={[{ required: true, message: '请输入网站标题' }]}
          >
            <Input placeholder="请输入网站标题" />
          </Form.Item>

          <Form.Item
            name="url"
            label="网站链接"
            rules={[
              { required: true, message: '请输入网站链接' },
              { type: 'url', message: '请输入有效的URL' }
            ]}
          >
            <Input placeholder="https://example.com" />
          </Form.Item>

          <Form.Item
            name="description"
            label="网站描述"
          >
            <Input.TextArea
              placeholder="请输入网站描述"
              rows={3}
            />
          </Form.Item>

          <Form.Item
            name="category"
            label="分类"
          >
            <Select placeholder="选择分类" allowClear>
              {categories.map(category => (
                <Option key={category.id} value={category.id}>
                  {category.name}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="is_active"
            valuePropName="checked"
            label="激活状态"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            name="is_public"
            valuePropName="checked"
            label="公开显示"
          >
            <Switch />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingWebsite ? '更新' : '创建'}
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Websites;