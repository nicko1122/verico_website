#!/usr/bin/env python3
"""
Step 1: 文件處理
解包 ZIP 文件，移動圖片，讀取規格文件
"""

import zipfile
import shutil
import time
from pathlib import Path
import json

def extract_package(zip_path):
    """解包產品包"""
    print(f"正在處理: {zip_path.name}")
    
    # 創建臨時目錄
    temp_dir = Path(f"temp_{int(time.time())}")
    temp_dir.mkdir(exist_ok=True)
    
    # 解壓縮
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    print(f"解包完成: {temp_dir}")
    return temp_dir

def handle_images(temp_dir, product_name):
    """處理圖片文件"""
    # 檢查圖片目錄
    possible_image_dirs = ['images', 'image', 'img']
    source_dir = None
    
    for dir_name in possible_image_dirs:
        img_dir = temp_dir / dir_name
        if img_dir.exists():
            source_dir = img_dir
            print(f"找到圖片目錄: {dir_name}")
            break
    
    if source_dir is None:
        source_dir = temp_dir
        print("使用根目錄查找圖片")
    
    # 移動圖片
    target_dir = Path("static/assets/images/product") / product_name
    target_dir.mkdir(parents=True, exist_ok=True)
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    moved_files = []
    
    for img_file in source_dir.glob('*'):
        if img_file.is_file() and img_file.suffix.lower() in image_extensions:
            shutil.copy2(img_file, target_dir / img_file.name)
            moved_files.append(img_file.name)
            print(f"圖片已移動: {img_file.name}")
    
    print(f"共移動了 {len(moved_files)} 個圖片文件")
    return moved_files

def read_spec_file(temp_dir):
    """讀取規格文件"""
    spec_files = list(temp_dir.glob('*.md')) + list(temp_dir.glob('spec.*'))
    
    if spec_files:
        spec_file = spec_files[0]
        with open(spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"規格文件已讀取: {spec_file.name}")
        return content
    
    print("未找到規格文件")
    return None

def save_step1_data(product_name, spec_content, image_files):
    """保存第一階段的數據"""
    data = {
        'product_name': product_name,
        'spec_content': spec_content,
        'image_files': image_files,
        'timestamp': int(time.time())
    }
    
    output_file = Path(f"step1_data_{product_name}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"第一階段數據已保存: {output_file}")
    return output_file

def main():
    """主函數"""
    # 檢查是否有 ZIP 文件
    zip_files = list(Path("product-packages").glob("*.zip"))
    
    if not zip_files:
        print("未找到 ZIP 文件")
        return
    
    for zip_file in zip_files:
        try:
            # 1. 解包
            temp_dir = extract_package(zip_file)
            
            # 2. 處理圖片
            product_name = zip_file.stem
            image_files = handle_images(temp_dir, product_name)
            
            # 3. 讀取規格文件
            spec_content = read_spec_file(temp_dir)
            
            if spec_content:
                # 4. 保存數據
                save_step1_data(product_name, spec_content, image_files)
                
                # 5. 清理臨時文件
                shutil.rmtree(temp_dir)
                
                print(f"✅ {product_name} 第一階段處理完成")
            else:
                print(f"❌ {product_name} 處理失敗：未找到規格文件")
                
        except Exception as e:
            print(f"❌ 處理 {zip_file.name} 時發生錯誤: {e}")

if __name__ == "__main__":
    main() 