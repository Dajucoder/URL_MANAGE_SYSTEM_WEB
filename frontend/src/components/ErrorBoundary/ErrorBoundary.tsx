import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Alert, Button, Typography } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    // 更新 state 使下一次渲染能够显示降级后的 UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // 记录错误信息
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  handleReload = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      // 如果提供了自定义fallback，使用它
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // 默认错误UI
      return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <Alert
            message="页面渲染出错"
            description="抱歉，页面遇到了一个错误。请尝试刷新页面或联系管理员。"
            type="error"
            showIcon
            style={{ marginBottom: '20px' }}
          />
          
          <Button 
            type="primary" 
            icon={<ReloadOutlined />} 
            onClick={this.handleReload}
          >
            重新加载页面
          </Button>

          {process.env.NODE_ENV === 'development' && this.state.error && (
            <div style={{ marginTop: '20px', textAlign: 'left' }}>
              <Title level={4}>错误详情 (开发模式)</Title>
              <Paragraph code>
                <pre style={{ fontSize: '12px', overflow: 'auto' }}>
                  {this.state.error.toString()}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </Paragraph>
            </div>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;