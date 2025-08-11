#!/usr/bin/env python
"""
测试API文档功能的脚本
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(url, description, expected_status=200):
    """测试API端点"""
    print(f"\n🔍 测试 {description}...")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"   ✅ {description} - 成功")
            
            # 如果是JSON响应，显示部分内容
            try:
                if 'application/json' in response.headers.get('content-type', ''):
                    data = response.json()
                    if isinstance(data, dict) and len(str(data)) < 500:
                        print(f"   响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
                    else:
                        print(f"   响应长度: {len(response.text)} 字符")
                else:
                    print(f"   响应类型: {response.headers.get('content-type', 'unknown')}")
            except:
                print(f"   响应长度: {len(response.text)} 字符")
            
            return True
        else:
            print(f"   ❌ {description} - 状态码错误 (期望: {expected_status})")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ {description} - 连接失败 (服务器未启动?)")
        return False
    except requests.exceptions.Timeout:
        print(f"   ❌ {description} - 请求超时")
        return False
    except Exception as e:
        print(f"   ❌ {description} - 错误: {str(e)}")
        return False

def main():
    print("🧪 开始测试API文档功能...")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试端点列表
    tests = [
        (f"{BASE_URL}/api/health/", "健康检查接口"),
        (f"{BASE_URL}/api/info/", "API信息接口"),
        (f"{BASE_URL}/api/schema/", "OpenAPI Schema"),
        (f"{BASE_URL}/api/docs/", "Swagger UI文档页面"),
        (f"{BASE_URL}/api/redoc/", "ReDoc文档页面"),
        (f"{BASE_URL}/admin/", "Django管理后台"),
    ]
    
    success_count = 0
    total_count = len(tests)
    
    for url, description in tests:
        if test_endpoint(url, description):
            success_count += 1
    
    print(f"\n📊 测试结果:")
    print(f"   总计: {total_count} 个端点")
    print(f"   成功: {success_count} 个")
    print(f"   失败: {total_count - success_count} 个")
    print(f"   成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 所有测试通过！API文档功能正常")
        return True
    else:
        print(f"\n⚠️ 有 {total_count - success_count} 个测试失败")
        print("\n💡 解决建议:")
        print("   1. 确保Django开发服务器正在运行: python manage.py runserver")
        print("   2. 检查是否安装了所有依赖: pip install -r requirements.txt")
        print("   3. 确保数据库迁移已完成: python manage.py migrate")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)