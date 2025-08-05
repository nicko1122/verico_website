#!/usr/bin/env python3
"""
Product Package Watcher
監控 product-packages 目錄，自動處理新的產品包
"""

import os
import json
import zipfile
import shutil
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import openai
from datetime import datetime

class ProductPackageHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        self.packages_dir = Path(config['packages_dir'])
        self.output_dir = Path(config['output_dir'])
        self.images_dir = Path(config['images_dir'])
        self.openai_client = openai.OpenAI(api_key=config['openai_api_key'])
        
        # 確保目錄存在
        self.packages_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        if file_path.suffix.lower() == '.zip':
            print(f"檢測到新的產品包: {file_path.name}")
            self.process_package(file_path)
    
    def process_package(self, zip_path):
        """處理產品包"""
        try:
            # 創建臨時目錄
            temp_dir = self.packages_dir / f"temp_{int(time.time())}"
            temp_dir.mkdir(exist_ok=True)
            
            # 解壓縮
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 處理文件
            self.handle_images(temp_dir)
            spec_content = self.handle_spec_file(temp_dir)
            
            if spec_content:
                # 生成 YAML
                yaml_content = self.generate_yaml(spec_content)
                
                # 保存文件
                self.save_files(zip_path.stem, yaml_content, temp_dir)
                
                # 生成頁面文件
                self.generate_pages(zip_path.stem, yaml_content)
                
                # 更新 Eleventy 配置
                self.update_eleventy_config(zip_path.stem)
                
                print(f"產品包 {zip_path.name} 處理完成！")
            
            # 清理臨時文件
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            print(f"處理產品包時發生錯誤: {e}")
    
    def handle_images(self, temp_dir):
        """處理圖片文件"""
        # 檢查不同的圖片目錄名稱
        possible_image_dirs = ['images', 'image', 'img']
        source_dir = None
        
        for dir_name in possible_image_dirs:
            img_dir = temp_dir / dir_name
            if img_dir.exists():
                source_dir = img_dir
                print(f"找到圖片目錄: {dir_name}")
                break
        
        if source_dir is None:
            # 如果沒有找到圖片目錄，使用根目錄
            source_dir = temp_dir
            print("使用根目錄查找圖片")
        
        # 使用 ZIP 文件名作為產品名稱
        product_name = temp_dir.name.replace('temp_', '')
        target_dir = self.images_dir / product_name
        target_dir.mkdir(exist_ok=True)
        
        # 移動圖片文件
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        moved_count = 0
        
        for img_file in source_dir.glob('*'):
            if img_file.is_file() and img_file.suffix.lower() in image_extensions:
                shutil.copy2(img_file, target_dir / img_file.name)
                print(f"圖片已移動: {img_file.name}")
                moved_count += 1
        
        if moved_count == 0:
            print("未找到圖片文件")
        else:
            print(f"共移動了 {moved_count} 個圖片文件")
    
    def handle_spec_file(self, temp_dir):
        """處理規格文件"""
        spec_files = list(temp_dir.glob('*.md')) + list(temp_dir.glob('spec.*'))
        
        if spec_files:
            spec_file = spec_files[0]
            with open(spec_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def generate_yaml(self, spec_content):
        """使用 LLM 生成 YAML"""
        prompt = f"""
你是一個產品數據轉換專家。請將以下產品文本轉換為結構化的 YAML 格式。

產品文本：
{spec_content}

請生成完整的 YAML 結構，包含以下部分：
1. product: 基本信息（name, badge, model_name, sku, ean）
2. hero: 英雄區塊（title, subtitle, description, cta_text, cta_link）
3. images: 圖片路徑（使用 static/assets/images/product/ 目錄）
4. features: 產品特色（title, description, icon）
5. specifications: 技術規格（technical, performance, features）
6. compatibility: 相容性（title, subtitle, devices）
7. package: 包裝內容（section_title, items）
8. product_info: 產品信息（model_name, sku, ean）
9. meta: SEO 信息（title, description, keywords）

注意：圖片路徑應該使用 /assets/images/product/[timestamp]/ 格式，其中 [timestamp] 是處理時間戳

請確保：
- 數據準確性
- 結構完整性
- 適合多語言網站使用
- 包含所有必要的字段

只返回 YAML 內容，不要包含其他文字。
"""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.config.get('model', 'gpt-4.1-mini'),
                messages=[
                    {"role": "system", "content": "你是一個專業的產品數據轉換專家，擅長將產品文本轉換為結構化的 YAML 格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.get('temperature', 0.3),
                max_tokens=self.config.get('max_tokens', 2000)
            )
            
            content = response.choices[0].message.content.strip()
            
            # 清理 markdown 代碼塊標記
            if content.startswith('```yaml'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            
            return content.strip()
            
        except Exception as e:
            print(f"LLM 生成 YAML 時發生錯誤: {e}")
            return None
    
    def save_files(self, product_name, yaml_content, temp_dir):
        """保存生成的文件"""
        if not yaml_content:
            return
            
        # 創建產品目錄
        product_dir = self.output_dir / product_name
        product_dir.mkdir(exist_ok=True)
        
        # 保存英文 YAML
        en_yaml_path = product_dir / 'en.yml'
        with open(en_yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        # 生成德文版本（簡化版）
        de_yaml_content = self.generate_german_yaml(yaml_content)
        de_yaml_path = product_dir / 'de.yml'
        with open(de_yaml_path, 'w', encoding='utf-8') as f:
            f.write(de_yaml_content)
        
        print(f"YAML 文件已保存: {product_name}")
    
    def generate_pages(self, product_name, yaml_content):
        """生成產品頁面文件"""
        try:
            # 導入頁面生成器
            from page_generator import PageGenerator
            
            # 創建頁面生成器
            page_config = {
                'templates_dir': 'src/_includes',
                'output_dir': 'src'
            }
            generator = PageGenerator(page_config)
            
            # 解析 YAML 內容
            import yaml
            product_data = yaml.safe_load(yaml_content)
            
            # 生成頁面
            generator.generate_pages(product_name, product_data)
            
            print(f"頁面文件已生成: {product_name}")
            
        except Exception as e:
            print(f"生成頁面時發生錯誤: {e}")
    
    def generate_german_yaml(self, en_yaml):
        """生成德文版本的 YAML"""
        prompt = f"""
請將以下英文 YAML 翻譯為德文版本。保持相同的結構，只翻譯文本內容。

英文 YAML：
{en_yaml}

請生成德文版本的 YAML，保持相同的結構和格式。
"""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.config.get('model', 'gpt-4.1-mini'),
                messages=[
                    {"role": "system", "content": "你是一個專業的德文翻譯專家，擅長將產品數據從英文翻譯為德文。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.get('temperature', 0.3),
                max_tokens=self.config.get('max_tokens', 2000)
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"生成德文 YAML 時發生錯誤: {e}")
            return en_yaml  # 如果翻譯失敗，返回英文版本
    
    def update_eleventy_config(self, product_name):
        """更新 Eleventy 配置"""
        config_file = Path('.eleventy.js')
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 檢查是否已經包含該產品
            if f"'{product_name}'" not in content:
                # 找到 productDetails 陣列並添加新產品
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'productDetails = [' in line:
                        # 在陣列結束前添加新產品
                        for j in range(i, len(lines)):
                            if ']' in lines[j] and 'productDetails' not in lines[j]:
                                lines.insert(j, f"  '{product_name}',")
                                break
                        break
                
                # 寫回文件
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                
                print(f"Eleventy 配置已更新，添加了產品: {product_name}")

def main():
    # 導入配置模組
    from config import get_config, check_api_key
    
    # 檢查 API Key
    if not check_api_key():
        return
    
    # 讀取配置
    config = get_config()
    if not config:
        print("❌ 無法讀取配置文件")
        return
    
    # 創建事件處理器
    event_handler = ProductPackageHandler(config)
    
    # 創建觀察者
    observer = Observer()
    observer.schedule(event_handler, config['packages_dir'], recursive=False)
    observer.start()
    
    print(f"開始監控目錄: {config['packages_dir']}")
    print("按 Ctrl+C 停止監控")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("監控已停止")
    
    observer.join()

if __name__ == "__main__":
    main() 