#!/usr/bin/env python3
"""
Step 1: 文件處理
解包 ZIP 文件，移動圖片，讀取規格文件
"""

import zipfile
import shutil
import time
import re
import yaml
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

def parse_markdown_front_matter(content):
    """解析 Markdown 文件的 front matter"""
    # 檢查是否有 YAML front matter
    front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    
    if front_matter_match:
        try:
            front_matter = yaml.safe_load(front_matter_match.group(1))
            return front_matter
        except yaml.YAMLError as e:
            print(f"Front matter 解析錯誤: {e}")
            return None
    
    return None

def extract_feature_paragraphs_with_images(content):
    """提取特點段落與圖片的關聯"""
    features = []
    
    # 方法 1: 從 front matter 提取
    front_matter = parse_markdown_front_matter(content)
    if front_matter and 'images' in front_matter and 'features' in front_matter['images']:
        features_config = front_matter['images']['features']
        if isinstance(features_config, dict):
            for key, config in features_config.items():
                features.append({
                    'image': config.get('image'),
                    'title': config.get('title', key.replace('_', ' ').title()),
                    'description': config.get('description', ''),
                    'key': key
                })
    
    # 方法 2: 從特殊標記提取 {feature:image.jpg}
    feature_matches = re.findall(r'###\s+(.+?)\s+\{feature:([^}]+)\}', content)
    for title, image in feature_matches:
        features.append({
            'image': image.strip(),
            'title': title.strip(),
            'description': '',
            'key': title.lower().replace(' ', '_')
        })
    
    # 方法 3: 從 HTML 註釋提取（優化版本）
    # 查找所有 FEATURE 註釋
    feature_comment_pattern = r'<!--\s*FEATURE:([^>]+)\s*-->\s*\n(.+?)(?=\n<!--|$)'
    feature_comment_matches = re.findall(feature_comment_pattern, content, re.DOTALL)
    
    for image, paragraph in feature_comment_matches:
        # 清理段落內容
        paragraph = paragraph.strip()
        
        # 提取標題（從粗體文字中提取）
        title_match = re.search(r'^\*\*(.+?)\*\*:', paragraph)
        if title_match:
            title = title_match.group(1).strip()
            # 移除標題部分，保留描述
            description = re.sub(r'^\*\*[^:]+:\*\*\s*', '', paragraph).strip()
        else:
            # 如果沒有粗體標題，嘗試從第一行提取
            lines = paragraph.split('\n')
            title = lines[0].strip().replace('**', '').replace('*', '')
            description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else paragraph
        
        features.append({
            'image': image.strip(),
            'title': title,
            'description': description,
            'key': title.lower().replace(' ', '_').replace('-', '_')
        })
    
    # 方法 4: 提取沒有圖片關聯的特點段落
    # 查找所有以 "- **" 開頭的行，但前面沒有 FEATURE 註釋
    lines = content.split('\n')
    current_feature = None
    
    for i, line in enumerate(lines):
        # 檢查是否有 FEATURE 註釋
        if '<!-- FEATURE:' in line:
            # 下一行應該是有圖片的特點
            continue
        elif line.strip().startswith('- **') and line.strip().endswith(':'):
            # 這是一個特點標題，檢查前面是否有 FEATURE 註釋
            if i > 0 and '<!-- FEATURE:' not in lines[i-1]:
                # 沒有圖片關聯的特點
                title_match = re.search(r'^\*\*(.+?)\*\*:', line.strip())
                if title_match:
                    title = title_match.group(1).strip()
                    # 查找描述（下一行）
                    description = ""
                    if i + 1 < len(lines) and not lines[i + 1].strip().startswith('- **'):
                        description = lines[i + 1].strip()
                    
                    features.append({
                        'image': None,  # 沒有圖片
                        'title': title,
                        'description': description,
                        'key': title.lower().replace(' ', '_').replace('-', '_')
                    })
    
    return features

def extract_image_config_from_markdown(content):
    """從 Markdown 內容中提取圖片配置"""
    # 嘗試解析 front matter
    front_matter = parse_markdown_front_matter(content)
    
    if front_matter and 'images' in front_matter:
        image_config = front_matter['images']
        # 添加特點段落關聯
        image_config['feature_paragraphs'] = extract_feature_paragraphs_with_images(content)
        return image_config
    
    # 如果沒有 front matter，嘗試從註釋中提取
    image_config = {
        'main': None,
        'gallery': [],
        'features': [],
        'feature_paragraphs': extract_feature_paragraphs_with_images(content)
    }
    
    # 查找圖片配置註釋
    main_match = re.search(r'<!--\s*IMAGES:\s*(.+?)\s*-->', content)
    if main_match:
        image_config['main'] = main_match.group(1).strip()
    
    gallery_match = re.search(r'<!--\s*GALLERY:\s*(.+?)\s*-->', content)
    if gallery_match:
        gallery_files = gallery_match.group(1).split(',')
        image_config['gallery'] = [f.strip() for f in gallery_files]
    
    features_match = re.search(r'<!--\s*FEATURES:\s*(.+?)\s*-->', content)
    if features_match:
        feature_files = features_match.group(1).split(',')
        image_config['features'] = [f.strip() for f in feature_files]
    
    return image_config

def handle_images(temp_dir, product_name, image_config=None):
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
    
    # 如果有圖片配置，優先使用配置的圖片
    if image_config:
        print("使用 Markdown 中的圖片配置")
        
        # 處理主圖
        if image_config.get('main'):
            main_file = source_dir / image_config['main']
            if main_file.exists():
                shutil.copy2(main_file, target_dir / main_file.name)
                moved_files.append(main_file.name)
                print(f"主圖已移動: {main_file.name}")
        
        # 處理輪播圖
        for gallery_file in image_config.get('gallery', []):
            gallery_path = source_dir / gallery_file
            if gallery_path.exists():
                shutil.copy2(gallery_path, target_dir / gallery_path.name)
                moved_files.append(gallery_path.name)
                print(f"輪播圖已移動: {gallery_path.name}")
        
        # 處理特點圖
        for feature_file in image_config.get('features', []):
            feature_path = source_dir / feature_file
            if feature_path.exists():
                shutil.copy2(feature_path, target_dir / feature_path.name)
                moved_files.append(feature_path.name)
                print(f"特點圖已移動: {feature_path.name}")
    
    # 如果沒有配置或配置的圖片不存在，使用默認方式
    if not moved_files:
        print("使用默認圖片處理方式")
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

def save_step1_data(product_name, spec_content, image_files, image_config=None):
    """保存第一階段的數據"""
    data = {
        'product_name': product_name,
        'spec_content': spec_content,
        'image_files': image_files,
        'image_config': image_config,
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
            # 解包
            temp_dir = extract_package(zip_file)
            
            # 讀取規格文件
            spec_content = read_spec_file(temp_dir)
            if not spec_content:
                print(f"跳過 {zip_file.name}：未找到規格文件")
                continue
            
            # 提取圖片配置
            image_config = extract_image_config_from_markdown(spec_content)
            
            # 獲取產品名稱
            product_name = zip_file.stem
            
            # 處理圖片
            image_files = handle_images(temp_dir, product_name, image_config)
            
            # 保存數據
            save_step1_data(product_name, spec_content, image_files, image_config)
            
            # 清理臨時目錄
            shutil.rmtree(temp_dir)
            print(f"產品包 {zip_file.name} 處理完成！")
            
        except Exception as e:
            print(f"處理 {zip_file.name} 時發生錯誤: {e}")
            continue

if __name__ == "__main__":
    main() 