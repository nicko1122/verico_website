#!/usr/bin/env python3
"""
配置文件
直接讀取 config.json 文件
"""

import os
import json
from pathlib import Path

def get_config():
    """讀取配置文件"""
    config_file = Path(__file__).parent / 'config.json'
    
    # 如果配置文件不存在，創建默認配置
    if not config_file.exists():
        create_default_config()
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"讀取配置文件失敗: {e}")
        return None

def create_default_config():
    """創建默認配置文件"""
    config_file = Path(__file__).parent / 'config.json'
    
    default_config = {
        "openai_api_key": "your-api-key-here",
        "packages_dir": "product-packages",
        "output_dir": "src/_data/content/products/details",
        "images_dir": "static/assets/images/product",
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    print(f"已創建默認配置文件: {config_file}")
    print("請編輯此文件並設置你的 OpenAI API Key")

def check_api_key():
    """檢查 API Key 是否有效"""
    config = get_config()
    if not config:
        return False
    
    api_key = config.get('openai_api_key', '')
    if not api_key or api_key == 'your-api-key-here':
        print("❌ 請在 config.json 中設置實際的 OpenAI API Key")
        print("編輯文件: product-generator/config.json")
        return False
    
    print("✅ OpenAI API Key 已設置")
    return True

def get_api_key():
    """獲取 API Key"""
    config = get_config()
    if config:
        return config.get('openai_api_key', '')
    return ''

if __name__ == "__main__":
    # 創建默認配置
    create_default_config()
    
    # 檢查 API Key
    if check_api_key():
        print("API Key 設置正確！")
    else:
        print("請設置 API Key 後再運行系統") 