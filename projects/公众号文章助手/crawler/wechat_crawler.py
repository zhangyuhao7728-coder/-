#!/usr/bin/env python3
"""
微信公众号文章抓取
"""
import os
import sys

CRAWLER_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("📥 微信公众号文章抓取")
    print("="*30)
    print("功能：")
    print("  1. 抓取公众号历史文章")
    print("  2. 解析文章内容")
    print("  3. 保存为Markdown")
    print()
    print("使用：")
    print("  python crawler/wechat_crawler.py --help")
    print()
    print("注意：需要微信授权，仅作参考")

if __name__ == '__main__':
    main()
