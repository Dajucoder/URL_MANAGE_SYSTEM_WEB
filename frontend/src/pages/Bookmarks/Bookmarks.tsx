  import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Input,
  Select,
  Switch,
  Modal,
  Form,
  message,
  Popconfirm,
  Tag,
  Typography,
  Row,
  Col,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  StarOutlined,
  StarFilled,
  SearchOutlined,
  ExportOutlined,
  ImportOutlined,
} from '@ant-design/icons';
import httpClient from '../../services/httpClient';
import { safeRender, safeRenderUrl, safeRenderDate } from '../../utils/renderSafe';
import './Bookmarks.css';

const { Title } = Typography;
const { Option } = Select;

interface Bookmark {
  id: number;
  title: string;
  url: string;
  description: string;
  is_favorite: boolean;
  collection?: number;
  collection_name?: string;
  is_archived?: boolean;
  visit_count?: number;
  last_visited?: string;
  created_at: string;
  updated_at: string;
}

interface Collection {
  id: number;
  name: string;
  description: string;
  bookmarks_count: number;
}

const Bookmarks: React.FC = () => {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [collections, setCollections] = useState<Collection[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingBookmark, setEditingBookmark] = useState<Bookmark | null>(null);
  const [searchText, setSearchText] = useState('');
  const [selectedCollection, setSelectedCollection] = useState<number | undefined>();
  const [showFavorites, setShowFavorites] = useState(false);
  const [form] = Form.useForm();

  const fetchBookmarksAndCollections = async () => {
    await Promise.all([fetchBookmarks(), fetchCollections()]);
  };

  useEffect(() => {
    fetchBookmarksAndCollections();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchBookmarks = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (searchText) params.search = searchText;
      if (selectedCollection) params.collection = selectedCollection;
      if (showFavorites) params.is_favorite = true;

      const data = await httpClient.get('/bookmarks/', { params });
      const bookmarks = Array.isArray(data.results) ? data.results : Array.isArray(data) ? data : [];
      setBookmarks(bookmarks);
    } catch (error) {
      message.error('获取书签列表失败');
      setBookmarks([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchCollections = async () => {
    try {
      const data = await httpClient.get('/bookmarks/collections/');
      const collections = Array.isArray(data.results) ? data.results : Array.isArray(data) ? data : [];
      setCollections(collections);
    } catch (error) {
      console.error('获取收藏夹失败:', error);
      setCollections([]);
    }
  };

  // 搜索和过滤效果
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchBookmarks();
    }, 300);
    return () => clearTimeout(timer);
  }, [searchText, selectedCollection, showFavorites]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleAdd = () => {
    setEditingBookmark(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (bookmark: Bookmark) => {
    setEditingBookmark(bookmark);
    form.setFieldsValue(bookmark);
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await httpClient.delete(`/bookmarks/${id}/`);
      message.success('删除成功');
      fetchBookmarks();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleToggleFavorite = async (bookmark: Bookmark) => {
    try {
      await httpClient.patch(`/bookmarks/${bookmark.id}/`, {
        is_favorite: !bookmark.is_favorite
      });
      message.success(bookmark.is_favorite ? '取消收藏' : '添加收藏');
      fetchBookmarks();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      if (editingBookmark) {
        await httpClient.patch(`/bookmarks/${editingBookmark.id}/`, values);
        message.success('更新成功');
      } else {
        await httpClient.post('/bookmarks/', values);
        message.success('创建成功');
      }
      setModalVisible(false);
      fetchBookmarks();
    } catch (error) {
      message.error(editingBookmark ? '更新失败' : '创建失败');
    }
  };

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: (text: string, record: Bookmark) => (
        <Space>
          <a href={safeRenderUrl(record?.url)} target="_blank" rel="noopener noreferrer">
            {safeRender(text)}
          </a>
          <Button
            type="text"
            size="small"
            icon={record?.is_favorite ? <StarFilled style={{ color: '#faad14' }} /> : <StarOutlined />}
            onClick={() => handleToggleFavorite(record)}
          />
        </Space>
      ),
    },
    {
      title: 'URL',
      dataIndex: 'url',
      key: 'url',
      ellipsis: true,
      render: (url: string) => {
        const urlString = safeRenderUrl(url);
        return urlString && urlString !== '#' ? (
          <a href={urlString} target="_blank" rel="noopener noreferrer">
            {urlString}
          </a>
        ) : '-';
      },
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (description: string) => safeRender(description, '-'),
    },
    {
      title: '收藏夹',
      dataIndex: 'collection_name',
      key: 'collection_name',
      render: (name: string) => name ? (
        <Tag color="blue">{safeRender(name)}</Tag>
      ) : '-',
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => safeRenderDate(date),
    },
    {
      title: '操作',
      key: 'actions',
      render: (_: any, record: Bookmark) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个书签吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button
              type="link"
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="bookmarks-page">
      <div className="page-header">
        <Title level={2}>书签管理</Title>
        <Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加书签
          </Button>
          <Button icon={<ImportOutlined />}>
            导入书签
          </Button>
          <Button icon={<ExportOutlined />}>
            导出书签
          </Button>
        </Space>
      </div>

      <Card>
        <Row gutter={[16, 16]} className="filter-row">
          <Col xs={24} sm={8} md={6}>
            <Input
              placeholder="搜索书签..."
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              allowClear
            />
          </Col>
          <Col xs={24} sm={8} md={6}>
            <Select
              placeholder="选择收藏夹"
              value={selectedCollection}
              onChange={setSelectedCollection}
              allowClear
              style={{ width: '100%' }}
            >
              {collections.map(collection => (
                <Option key={collection.id} value={collection.id}>
                  {collection.name} ({collection.bookmarks_count || 0})
                </Option>
              ))}
            </Select>
          </Col>
          <Col xs={24} sm={8} md={6}>
            <Space>
              <Switch
                checked={showFavorites}
                onChange={setShowFavorites}
                checkedChildren="收藏"
                unCheckedChildren="全部"
              />
            </Space>
          </Col>
        </Row>

        <Table
          columns={columns}
          dataSource={bookmarks}
          rowKey="id"
          loading={loading}
          pagination={{
            total: bookmarks.length,
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 条记录`,
          }}
        />
      </Card>

      <Modal
        title={editingBookmark ? '编辑书签' : '添加书签'}
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
            label="标题"
            rules={[{ required: true, message: '请输入书签标题' }]}
          >
            <Input placeholder="请输入书签标题" />
          </Form.Item>

          <Form.Item
            name="url"
            label="URL"
            rules={[
              { required: true, message: '请输入URL' },
              { type: 'url', message: '请输入有效的URL' }
            ]}
          >
            <Input placeholder="https://example.com" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea
              placeholder="请输入书签描述..."
              rows={3}
            />
          </Form.Item>

          <Form.Item
            name="collection"
            label="收藏夹"
          >
            <Select placeholder="选择收藏夹" allowClear>
              {collections.map(collection => (
                <Option key={collection.id} value={collection.id}>
                  {collection.name}
                </Option>
              ))}
            </Select>
          </Form.Item>


          <Form.Item
            name="is_favorite"
            valuePropName="checked"
          >
            <Switch checkedChildren="收藏" unCheckedChildren="普通" />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingBookmark ? '更新' : '创建'}
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

export default Bookmarks;