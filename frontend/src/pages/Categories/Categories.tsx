import React, { useState, useEffect, useCallback } from 'react';
import {
  Card,
  Tree,
  Button,
  Space,
  Input,
  Typography,
  Modal,
  Form,
  message,
  Popconfirm,
  Select,
  Row,
  Col,
  Spin,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  FolderOutlined,
  TagsOutlined,
} from '@ant-design/icons';
import type { DataNode } from 'antd/es/tree';
import httpClient from '../../services/httpClient';
import { DEFAULT_COLORS, ICON_OPTIONS } from '../../config/constants';
import './Categories.css';

const { Title, Text } = Typography;
const { Option } = Select;

interface Category {
  id: number;
  name: string;
  description: string;
  color: string;
  icon: string;
  parent?: number;
  website_count: number;
  children?: Category[];
  full_path: string;
}

interface CategoryTag {
  id: number;
  name: string;
  color: string;
  usage_count: number;
}

const Categories: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<CategoryTag[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [tagModalVisible, setTagModalVisible] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);
  const [editingTag, setEditingTag] = useState<CategoryTag | null>(null);
  const [form] = Form.useForm();
  const [tagForm] = Form.useForm();

  const fetchCategories = useCallback(async () => {
    try {
      setLoading(true);
      const data = await httpClient.get('/websites/categories/');
      const categories = Array.isArray(data.results) ? data.results : Array.isArray(data) ? data : [];
      setCategories(categories);
    } catch (error) {
      message.error('获取分类列表失败');
      setCategories([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchTags = useCallback(async () => {
    try {
      const data = await httpClient.get('/websites/tags/');
      const tags = Array.isArray(data.results) ? data.results : Array.isArray(data) ? data : [];
      setTags(tags);
    } catch (error) {
      message.error('获取标签列表失败');
      setTags([]);
    }
  }, []);

  const fetchCategoriesAndTags = useCallback(async () => {
    await Promise.all([fetchCategories(), fetchTags()]);
  }, [fetchCategories, fetchTags]);

  useEffect(() => {
    fetchCategoriesAndTags();
  }, [fetchCategoriesAndTags]);

  const handleAddCategory = () => {
    setEditingCategory(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditCategory = useCallback((category: Category) => {
    setEditingCategory(category);
    form.setFieldsValue(category);
    setModalVisible(true);
  }, [form]);

  const handleDeleteCategory = useCallback(async (id: number) => {
    try {
      await httpClient.delete(`/websites/categories/${id}/`);
      message.success('删除成功');
      fetchCategories();
    } catch (error) {
      message.error('删除失败');
    }
  }, [fetchCategories]);

  const handleSubmitCategory = async (values: any) => {
    try {
      if (editingCategory) {
        await httpClient.patch(`/websites/categories/${editingCategory.id}/`, values);
        message.success('更新成功');
      } else {
        await httpClient.post('/websites/categories/', values);
        message.success('创建成功');
      }
      setModalVisible(false);
      fetchCategories();
    } catch (error) {
      message.error(editingCategory ? '更新失败' : '创建失败');
    }
  };

  const handleAddTag = () => {
    setEditingTag(null);
    tagForm.resetFields();
    setTagModalVisible(true);
  };

  const handleEditTag = (tag: CategoryTag) => {
    setEditingTag(tag);
    tagForm.setFieldsValue(tag);
    setTagModalVisible(true);
  };

  const handleDeleteTag = async (id: number) => {
    try {
      await httpClient.delete(`/websites/tags/${id}/`);
      message.success('删除成功');
      fetchTags();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmitTag = async (values: any) => {
    try {
      if (editingTag) {
        await httpClient.patch(`/websites/tags/${editingTag.id}/`, values);
        message.success('更新成功');
      } else {
        await httpClient.post('/websites/tags/', values);
        message.success('创建成功');
      }
      setTagModalVisible(false);
      fetchTags();
    } catch (error) {
      message.error(editingTag ? '更新失败' : '创建失败');
    }
  };

  // 转换为Tree组件需要的格式
  const convertToTreeData = useCallback((cats: (Category & { children: Category[] })[]): DataNode[] => {
    return cats.map(cat => ({
      key: cat.id.toString(),
      title: (
        <div className="category-node">
          <Space>
            <FolderOutlined style={{ color: cat.color || '#1890ff' }} />
            <span>{cat.name || ''}</span>
            <span className="category-count">({cat.website_count || 0})</span>
            <Space size="small">
              <Button
                type="link"
                size="small"
                icon={<EditOutlined />}
                onClick={() => handleEditCategory(cat)}
              />
              <Popconfirm
                title="确定要删除这个分类吗？"
                onConfirm={() => handleDeleteCategory(cat.id)}
                okText="确定"
                cancelText="取消"
              >
                <Button
                  type="link"
                  size="small"
                  danger
                  icon={<DeleteOutlined />}
                />
              </Popconfirm>
            </Space>
          </Space>
        </div>
      ),
      children: cat.children && cat.children.length > 0 ? convertToTreeData(cat.children as (Category & { children: Category[] })[]) : undefined,
    }));
  }, [handleEditCategory, handleDeleteCategory]);

  // 构建树形数据
  const buildTreeData = useCallback((categories: Category[]): DataNode[] => {
    if (!categories || categories.length === 0) {
      return [];
    }

    type CategoryWithChildren = Category & { children: Category[] };
    const categoryMap = new Map<number, CategoryWithChildren>();
    
    // 初始化所有分类，确保children是数组
    categories.forEach(cat => {
      if (cat && cat.id) {
        categoryMap.set(cat.id, { ...cat, children: [] });
      }
    });
    
    // 构建父子关系
    const rootCategories: CategoryWithChildren[] = [];
    categories.forEach(cat => {
      if (!cat || !cat.id) return;
      
      const category = categoryMap.get(cat.id);
      if (!category) return;
      
      if (cat.parent) {
        const parent = categoryMap.get(cat.parent);
        if (parent) {
          parent.children.push(category);
        }
      } else {
        rootCategories.push(category);
      }
    });
    
    return convertToTreeData(rootCategories);
  }, [convertToTreeData]);

  return (
    <div className="categories-page">
      <div className="page-header">
        <Title level={2}>分类和标签管理</Title>
        <Text type="secondary">管理您的网站分类和标签</Text>
      </div>

      <Row gutter={[24, 24]}>
        {/* 分类管理 */}
        <Col xs={24} lg={12}>
          <Card
            title={
              <Space>
                <FolderOutlined />
                分类管理
              </Space>
            }
            extra={
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={handleAddCategory}
              >
                添加分类
              </Button>
            }
          >
            {loading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin size="large" />
              </div>
            ) : (
              <Tree
                treeData={buildTreeData(categories)}
                defaultExpandAll
                showLine
              />
            )}
          </Card>
        </Col>

        {/* 标签管理 */}
        <Col xs={24} lg={12}>
          <Card
            title={
              <Space>
                <TagsOutlined />
                标签管理
              </Space>
            }
            extra={
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={handleAddTag}
              >
                添加标签
              </Button>
            }
          >
            <div className="tags-container">
              {tags && tags.length > 0 ? tags.map(tag => (
                <div key={tag.id} className="tag-item">
                  <Space>
                    <div
                      className="tag-color"
                      style={{ backgroundColor: tag.color || '#1890ff' }}
                    />
                    <span>{tag.name || ''}</span>
                    <span className="tag-count">({tag.usage_count || 0})</span>
                    <Space size="small">
                      <Button
                        type="link"
                        size="small"
                        icon={<EditOutlined />}
                        onClick={() => handleEditTag(tag)}
                      />
                      <Popconfirm
                        title="确定要删除这个标签吗？"
                        onConfirm={() => handleDeleteTag(tag.id)}
                        okText="确定"
                        cancelText="取消"
                      >
                        <Button
                          type="link"
                          size="small"
                          danger
                          icon={<DeleteOutlined />}
                        />
                      </Popconfirm>
                    </Space>
                  </Space>
                </div>
              )) : (
                <div style={{ textAlign: 'center', padding: '20px' }}>
                  <Text type="secondary">暂无标签</Text>
                </div>
              )}
            </div>
          </Card>
        </Col>
      </Row>

      {/* 分类编辑模态框 */}
      <Modal
        title={editingCategory ? '编辑分类' : '添加分类'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmitCategory}
        >
          <Form.Item
            name="name"
            label="分类名称"
            rules={[{ required: true, message: '请输入分类名称' }]}
          >
            <Input placeholder="请输入分类名称" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea
              placeholder="请输入分类描述..."
              rows={3}
            />
          </Form.Item>

          <Form.Item
            name="parent"
            label="父分类"
          >
            <Select placeholder="选择父分类" allowClear>
              {categories
                .filter(cat => !editingCategory || cat.id !== editingCategory.id)
                .map(cat => (
                  <Option key={cat.id} value={cat.id}>
                    {cat.full_path}
                  </Option>
                ))}
            </Select>
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="color"
                label="颜色"
                initialValue={DEFAULT_COLORS[0]}
              >
                <Select>
                  {DEFAULT_COLORS.map(color => (
                    <Option key={color} value={color}>
                      <Space>
                        <div
                          style={{
                            width: 16,
                            height: 16,
                            backgroundColor: color,
                            borderRadius: 2,
                          }}
                        />
                        {color}
                      </Space>
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="icon"
                label="图标"
                initialValue={ICON_OPTIONS[0]}
              >
                <Select>
                  {ICON_OPTIONS.map(icon => (
                    <Option key={icon} value={icon}>
                      {icon}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingCategory ? '更新' : '创建'}
              </Button>
              <Button onClick={() => setModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* 标签编辑模态框 */}
      <Modal
        title={editingTag ? '编辑标签' : '添加标签'}
        open={tagModalVisible}
        onCancel={() => setTagModalVisible(false)}
        footer={null}
        width={400}
      >
        <Form
          form={tagForm}
          layout="vertical"
          onFinish={handleSubmitTag}
        >
          <Form.Item
            name="name"
            label="标签名称"
            rules={[{ required: true, message: '请输入标签名称' }]}
          >
            <Input placeholder="请输入标签名称" />
          </Form.Item>

          <Form.Item
            name="color"
            label="颜色"
            initialValue={DEFAULT_COLORS[0]}
          >
            <Select>
              {DEFAULT_COLORS.map(color => (
                <Option key={color} value={color}>
                  <Space>
                    <div
                      style={{
                        width: 16,
                        height: 16,
                        backgroundColor: color,
                        borderRadius: 2,
                      }}
                    />
                    {color}
                  </Space>
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingTag ? '更新' : '创建'}
              </Button>
              <Button onClick={() => setTagModalVisible(false)}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Categories;