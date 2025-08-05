#!/usr/bin/env python3
"""
簡單設置腳本
創建配置文件並設置 API Key
"""

import json
from pathlib import Path

def setup():
    """設置系統"""
    print("=== 產品生成器設置 ===")
    
    # 創建配置文件
    config_file = Path(__file__).parent / 'config.json'
    
    if config_file.exists():
        print("配置文件已存在")
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        current_key = config.get('openai_api_key', '')
        if current_key and current_key != 'your-api-key-here':
            print("✅ API Key 已設置")
            return True
        else:
            print("❌ API Key 未設置")
    else:
        print("創建新配置文件")
        config = {
            "openai_api_key": "your-api-key-here",
            "packages_dir": "product-packages",
            "output_dir": "src/_data/content/products/details",
            "images_dir": "static/assets/images/product",
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "max_tokens": 2000
        }
    
    # 設置 API Key
    print("\n請輸入你的 OpenAI API Key:")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ API Key 不能為空")
        return False
    
    config['openai_api_key'] = api_key
    
    # 保存配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 配置已保存到: {config_file}")
    return True

def main():
    if setup():
        print("\n🎉 設置完成！")
        print("現在可以運行產品生成器了：")
        print("python start_watcher.py")
    else:
        print("\n❌ 設置失敗")

if __name__ == "__main__":
    main() 