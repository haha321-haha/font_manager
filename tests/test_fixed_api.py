#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版API测试脚本
测试新的API密钥和修复后的代码
"""

import requests
import json
import time
from datetime import datetime

def test_api_connection():
    """测试API连接"""
    
    # 新的API密钥
    API_KEY = "affa9596d74247c58b407eebe58b990f"
    
    # API配置
    base_url = "https://api.twitterapi.io"
    endpoint = "/twitter/tweet/advanced_search"
    
    print("=" * 60)
    print("🔍 修复版API连接测试")
    print("=" * 60)
    print(f"API密钥: {API_KEY[:10]}...")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 请求头
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # 测试查询
    test_queries = [
        "feng shui",
        "风水",
        "bazi"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"🧪 测试 {i}/{len(test_queries)}: '{query}'")
        
        # 构建查询
        search_query = f'"{query}" (lang:zh OR lang:en) -is:retweet'
        
        params = {
            "query": search_query,
            "count": 5,  # 只获取5条进行测试
            "queryType": "recent"
        }
        
        try:
            print(f"📡 发送请求...")
            response = requests.get(
                f"{base_url}{endpoint}",
                headers=headers,
                params=params,
                timeout=15
            )
            
            print(f"📊 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 连接成功!")
                
                # 检查响应结构
                if data.get("status") == "success":
                    tweets = data.get("data", [])
                    print(f"📝 获取到 {len(tweets)} 条推文")
                    
                    # 显示第一条推文的详细信息
                    if tweets:
                        first_tweet = tweets[0]
                        print("\n📋 第一条推文详情:")
                        print(f"  ID: {first_tweet.get('id', 'N/A')}")
                        print(f"  内容: {first_tweet.get('text', 'N/A')[:100]}...")
                        print(f"  作者: {first_tweet.get('author', {}).get('userName', 'N/A')}")
                        print(f"  时间: {first_tweet.get('createdAt', 'N/A')}")
                        print(f"  点赞: {first_tweet.get('likeCount', 0)}")
                        print(f"  转发: {first_tweet.get('retweetCount', 0)}")
                    
                    # 显示余额信息
                    if "credits_remaining" in data:
                        print(f"💰 剩余积分: {data['credits_remaining']}")
                    
                    # 显示分页信息
                    pagination = data.get("pagination", {})
                    if pagination:
                        print(f"📄 分页信息: {pagination}")
                        
                else:
                    print(f"❌ API返回错误: {data.get('message', 'Unknown error')}")
                    
            elif response.status_code == 402:
                print("❌ 402错误 - 积分不足")
                try:
                    error_data = response.json()
                    print(f"错误详情: {error_data}")
                except:
                    print(f"原始响应: {response.text}")
                    
            elif response.status_code == 401:
                print("❌ 401错误 - 认证失败")
                print(f"错误详情: {response.text}")
                
            elif response.status_code == 429:
                print("❌ 429错误 - 频率限制")
                print(f"错误详情: {response.text}")
                
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应内容: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
        except requests.exceptions.ConnectionError:
            print("❌ 连接错误")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        
        print("-" * 40)
        
        # 请求间隔
        if i < len(test_queries):
            print("⏳ 等待3秒...")
            time.sleep(3)
    
    print("=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    print("✅ 如果看到成功响应，说明API密钥和代码都正常")
    print("❌ 如果看到402错误，说明积分不足")
    print("❌ 如果看到401错误，说明API密钥有问题")
    print("❌ 如果看到429错误，说明请求过于频繁")
    print("=" * 60)

def test_single_query():
    """测试单个查询的详细响应"""
    
    API_KEY = "affa9596d74247c58b407eebe58b990f"
    base_url = "https://api.twitterapi.io"
    endpoint = "/twitter/tweet/advanced_search"
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # 测试查询
    query = "feng shui"
    search_query = f'"{query}" (lang:zh OR lang:en) -is:retweet'
    
    params = {
        "query": search_query,
        "count": 1,
        "queryType": "recent"
    }
    
    print("🔍 详细响应测试")
    print(f"查询: {search_query}")
    
    try:
        response = requests.get(
            f"{base_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=15
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n📋 完整响应结构:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000] + "...")
            
            # 分析响应结构
            print("\n🔍 响应结构分析:")
            print(f"状态: {data.get('status', 'N/A')}")
            print(f"数据条数: {len(data.get('data', []))}")
            print(f"分页信息: {data.get('pagination', 'N/A')}")
            
            # 检查关键字段
            if data.get('data'):
                tweet = data['data'][0]
                print(f"\n📝 推文字段检查:")
                print(f"  id: {'✅' if 'id' in tweet else '❌'}")
                print(f"  text: {'✅' if 'text' in tweet else '❌'}")
                print(f"  createdAt: {'✅' if 'createdAt' in tweet else '❌'}")
                print(f"  author: {'✅' if 'author' in tweet else '❌'}")
                print(f"  retweetCount: {'✅' if 'retweetCount' in tweet else '❌'}")
                print(f"  likeCount: {'✅' if 'likeCount' in tweet else '❌'}")
                
        else:
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"测试异常: {str(e)}")

if __name__ == "__main__":
    print("🚀 开始API测试...")
    test_api_connection()
    
    print("\n" + "=" * 60)
    print("🔍 详细响应测试")
    print("=" * 60)
    test_single_query() 