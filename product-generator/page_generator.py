#!/usr/bin/env python3
"""
Product Page Generator
自動生成產品頁面文件
"""

import os
import yaml
from pathlib import Path

class PageGenerator:
    def __init__(self, config):
        self.config = config
        self.templates_dir = Path(config['templates_dir'])
        self.output_dir = Path(config['output_dir'])
        
    def generate_pages(self, product_name, product_data):
        """生成產品頁面"""
        try:
            # 創建英文頁面
            self.generate_english_page(product_name, product_data)
            
            # 創建德文頁面
            self.generate_german_page(product_name, product_data)
            
            print(f"產品頁面已生成: {product_name}")
            
        except Exception as e:
            print(f"生成頁面時發生錯誤: {e}")
    
    def generate_english_page(self, product_name, product_data):
        """生成英文頁面"""
        # 確定產品類別
        category = self.determine_category(product_data)
        
        # 創建目錄
        page_dir = self.output_dir / 'en' / 'products' / category / product_name
        page_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成頁面內容
        page_content = self.create_page_template(product_name, 'en', product_data)
        
        # 保存文件
        page_file = page_dir / 'index.njk'
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(page_content)
    
    def generate_german_page(self, product_name, product_data):
        """生成德文頁面"""
        # 確定產品類別
        category = self.determine_category(product_data)
        
        # 創建目錄
        page_dir = self.output_dir / 'de' / 'products' / category / product_name
        page_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成頁面內容
        page_content = self.create_page_template(product_name, 'de', product_data)
        
        # 保存文件
        page_file = page_dir / 'index.njk'
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(page_content)
    
    def determine_category(self, product_data):
        """根據產品數據確定類別"""
        # 這裡可以根據產品名稱或數據來判斷類別
        product_name = product_data.get('product', {}).get('name', '').lower()
        
        if 'ssd' in product_name or 'storage' in product_name:
            return 'storage'
        elif 'charger' in product_name or 'gan' in product_name:
            return 'gan-charger'
        elif 'power' in product_name or 'battery' in product_name:
            return 'powerbank'
        elif 'usb' in product_name or 'flash' in product_name:
            return 'flash-disk'
        elif 'loop' in product_name or 'energy' in product_name:
            return 'loopenergy'
        else:
            return 'storage'  # 默認類別
    
    def create_page_template(self, product_name, lang, product_data):
        """創建頁面模板"""
        # 將產品名稱轉換為 snake_case
        product_slug = product_name.replace('-', '_')
        
        if lang == 'en':
            title = product_data.get('product', {}).get('name', product_name)
            permalink = f"/en/products/{self.determine_category(product_data)}/{product_name}/"
        else:
            title = product_data.get('product', {}).get('name', product_name)  # 這裡應該使用德文名稱
            permalink = f"/de/products/{self.determine_category(product_data)}/{product_name}/"
        
        template = f"""---
title: "{title}"
lang: {lang}
permalink: {permalink}
---

{{% set product = content.products.details.{product_slug}.{lang} %}}

{{% include "product-detail.njk" %}}
"""
        return template

def main():
    # 配置
    config = {
        'templates_dir': 'src/_includes',
        'output_dir': 'src'
    }
    
    generator = PageGenerator(config)
    
    # 測試生成
    test_data = {
        'product': {
            'name': 'Test Product'
        }
    }
    
    generator.generate_pages('test-product', test_data)

if __name__ == "__main__":
    main() 