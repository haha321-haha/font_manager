#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的TwitterAPI收集器
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fixed_twitterapi_collector import FixedTwitterAPICollector

def test_collector():
    """测试收集器"""
    
    print("🚀 测试修复后的TwitterAPI收集器")
    print("=" * 60)
    
    # 从配置文件读取API密钥
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            api_key = config['api_config']['api_key']
            print(f"✅ 成功读取API密钥: {api_key[:10]}...")
    except Exception as e:
        print(f"❌ 读取配置文件失败: {str(e)}")
        return
    
    # 创建收集器
    collector = FixedTwitterAPICollector(api_key)
    
    # 测试单个关键词
    test_keyword = "feng shui"
    print(f"\n🧪 测试关键词: {test_keyword}")
    
    try:
        # 收集少量数据进行测试
        tweets = collector.collect_keyword_data(test_keyword, max_tweets=10, delay=2.0)
        
        if tweets:
            print(f"✅ 成功收集 {len(tweets)} 条推文")
            
            # 显示第一条推文的详细信息
            if tweets:
                first_tweet = tweets[0]
                print(f"\n📋 第一条推文示例:")
                print(f"  ID: {first_tweet.get('tweet_id', 'N/A')}")
                print(f"  内容: {first_tweet.get('text', 'N/A')[:100]}...")
                print(f"  作者: {first_tweet.get('author_username', 'N/A')}")
                print(f"  时间: {first_tweet.get('created_at', 'N/A')}")
                print(f"  点赞: {first_tweet.get('like_count', 0)}")
                print(f"  转发: {first_tweet.get('retweet_count', 0)}")
            
            # 保存测试数据
            csv_file = collector.save_to_csv(tweets, "test_fixed_collector.csv")
            json_file = collector.save_to_json(tweets, "test_fixed_collector.json")
            
            print(f"\n💾 测试数据已保存:")
            print(f"  CSV: {csv_file}")
            print(f"  JSON: {json_file}")
            
        else:
            print("⚠️ 没有收集到数据")
            
        # 打印统计信息
        collector.print_stats()
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

def test_multiple_keywords():
    """测试多个关键词"""
    
    print("\n" + "=" * 60)
    print("🧪 测试多个关键词")
    print("=" * 60)
    
    # 从配置文件读取API密钥
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            api_key = config['api_config']['api_key']
    except Exception as e:
        print(f"❌ 读取配置文件失败: {str(e)}")
        return
    
    # 创建收集器
    collector = FixedTwitterAPICollector(api_key)
    
    # 测试少量关键词
    test_keywords = ["feng shui", "风水", "bazi"]
    
    try:
        # 收集数据
        all_tweets = []
        for keyword in test_keywords:
            print(f"\n📌 收集关键词: {keyword}")
            tweets = collector.collect_keyword_data(keyword, max_tweets=5, delay=3.0)
            all_tweets.extend(tweets)
            print(f"✅ 收集到 {len(tweets)} 条推文")
        
        if all_tweets:
            print(f"\n🎉 总共收集到 {len(all_tweets)} 条推文")
            
            # 保存数据
            csv_file = collector.save_to_csv(all_tweets, "test_multiple_keywords.csv")
            json_file = collector.save_to_json(all_tweets, "test_multiple_keywords.json")
            
            print(f"💾 数据已保存:")
            print(f"  CSV: {csv_file}")
            print(f"  JSON: {json_file}")
            
        else:
            print("⚠️ 没有收集到数据")
            
        # 打印统计信息
        collector.print_stats()
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 测试单个关键词
    test_collector()
    
    # 测试多个关键词
    test_multiple_keywords()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成!")
    print("=" * 60) 