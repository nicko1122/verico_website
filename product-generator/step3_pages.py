#!/usr/bin/env python3
"""
Step 3: 頁面生成和配置更新
生成頁面文件，自動更新 Eleventy 配置
"""

import os
import re
from pathlib import Path
import subprocess

def scan_product_directories():
    """掃描產品目錄"""
    details_dir = Path("src/_data/content/products/details")
    
    if not details_dir.exists():
        print("❌ 產品詳情目錄不存在")
        return []
    
    products = []
    for product_dir in details_dir.iterdir():
        if product_dir.is_dir():
            # 檢查是否有 en.yml 和 de.yml
            en_file = product_dir / "en.yml"
            de_file = product_dir / "de.yml"
            
            if en_file.exists() and de_file.exists():
                products.append(product_dir.name)
                print(f"✅ 找到產品: {product_dir.name}")
    
    return products

def update_eleventy_config(products):
    """更新 Eleventy 配置"""
    config_file = Path("../.eleventy.js")
    
    if not config_file.exists():
        print("❌ 未找到 .eleventy.js 文件")
        return False
    
    # 讀取配置文件
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 productDetails 陣列
    pattern = r'const productDetails = \[([^\]]*)\]'
    match = re.search(pattern, content, re.MULTILINE)
    
    if not match:
        print("❌ 未找到 productDetails 陣列")
        return False
    
    # 解析現有產品
    existing_products = []
    if match.group(1).strip():
        existing_products = [p.strip().strip("'\"") for p in match.group(1).split(',')]
    
    # 添加新產品
    new_products = []
    for product in products:
        if product not in existing_products:
            new_products.append(product)
            existing_products.append(product)
    
    if new_products:
        # 更新配置
        new_array = "[\n      " + ",\n      ".join([f"'{p}'" for p in existing_products]) + "\n    ]"
        new_content = re.sub(pattern, f'const productDetails = {new_array}', content, flags=re.MULTILINE)
        
        # 寫回文件
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 已添加 {len(new_products)} 個新產品到 Eleventy 配置:")
        for product in new_products:
            print(f"  - {product}")
    else:
        print("✅ 所有產品都已存在於配置中")
    
    return True

def update_product_catalog(products):
    """更新產品目錄"""
    catalog_files = [
        Path("../src/_data/content/products/catalog/en.yml"),
        Path("../src/_data/content/products/catalog/de.yml")
    ]
    
    for catalog_file in catalog_files:
        if not catalog_file.exists():
            print(f"❌ 未找到產品目錄文件: {catalog_file}")
            continue
        
        # 讀取現有目錄
        with open(catalog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 YAML
        import yaml
        try:
            catalog_data = yaml.safe_load(content)
        except Exception as e:
            print(f"❌ 解析 {catalog_file.name} 時發生錯誤: {e}")
            continue
        
        # 為每個新產品添加到適當的類別
        for product in products:
            category = determine_category(product)
            
            # 確保類別存在
            if 'products' not in catalog_data:
                catalog_data['products'] = {}
            if category not in catalog_data['products']:
                catalog_data['products'][category] = []
            
            # 檢查產品是否已存在
            existing_products = [p.get('slug', '') for p in catalog_data['products'][category]]
            product_slug = product.replace(' ', '-').lower()
            
            if product_slug not in existing_products:
                # 添加新產品到目錄
                new_product = {
                    'name': product,
                    'description': f"New {product} product.",
                    'details': f"Details for {product}.",
                    'image': f"assets/images/product/{product.replace(' ', '-').lower()}/product-1.jpg",
                    'alt': product,
                    'link': f"/en/products/{category}/{product.replace(' ', '-').lower()}/",
                    'slug': product_slug
                }
                
                catalog_data['products'][category].append(new_product)
                print(f"✅ 已添加 {product} 到 {catalog_file.name} 的 {category} 類別")
        
        # 寫回文件
        with open(catalog_file, 'w', encoding='utf-8') as f:
            yaml.dump(catalog_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def update_navigation(products):
    """更新導航文件"""
    nav_file = Path("../src/_data/site/navigation.yml")
    
    if not nav_file.exists():
        print("❌ 未找到導航文件")
        return
    
    # 讀取現有導航
    with open(nav_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 YAML
    import yaml
    try:
        nav_data = yaml.safe_load(content)
    except Exception as e:
        print(f"❌ 解析導航文件時發生錯誤: {e}")
        return
    
    # 找到 Products 選單
    for item in nav_data['main']:
        if item.get('title', {}).get('en') == 'Products':
            # 找到適當的子選單
            for submenu in item.get('submenu', []):
                category_name = submenu.get('title', {}).get('en', '')
                
                # 根據類別名稱匹配
                if 'GaN Charger' in category_name and any('charger' in p.lower() or 'gan' in p.lower() for p in products):
                    # 添加新產品到 GaN Charger 子選單
                    for product in products:
                        if 'charger' in product.lower() or 'gan' in product.lower():
                            product_slug = product.replace(' ', '-').lower()
                            
                            # 檢查是否已存在
                            existing_items = [item.get('title', {}).get('en', '') for item in submenu.get('submenu', [])]
                            if product not in existing_items:
                                new_item = {
                                    'title': {
                                        'en': product,
                                        'de': product  # 可以後續翻譯
                                    },
                                    'url': {
                                        'en': f'/en/products/gan-charger/{product_slug}/',
                                        'de': f'/de/products/gan-charger/{product_slug}/'
                                    },
                                    'available_in': ['en', 'de']
                                }
                                
                                if 'submenu' not in submenu:
                                    submenu['submenu'] = []
                                submenu['submenu'].append(new_item)
                                print(f"✅ 已添加 {product} 到導航選單")
            
            # 處理其他類別（可以擴展）
            # 這裡可以添加其他類別的處理邏輯
    
    # 寫回文件
    with open(nav_file, 'w', encoding='utf-8') as f:
        yaml.dump(nav_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def generate_page_files(products):
    """生成頁面文件"""
    for product in products:
        try:
            # 確定產品類別
            category = determine_category(product)
            
            # 生成英文頁面
            generate_page(product, 'en', category)
            
            # 生成德文頁面
            generate_page(product, 'de', category)
            
            print(f"✅ 已生成頁面文件: {product}")
            
        except Exception as e:
            print(f"❌ 生成頁面時發生錯誤: {e}")

def determine_category(product_name):
    """根據產品名稱確定類別"""
    name_lower = product_name.lower()
    
    if 'ssd' in name_lower or 'storage' in name_lower:
        return 'storage'
    elif 'charger' in name_lower or 'gan' in name_lower:
        return 'gan-charger'
    elif 'power' in name_lower or 'battery' in name_lower:
        return 'powerbank'
    elif 'usb' in name_lower or 'flash' in name_lower:
        return 'flash-disk'
    elif 'loop' in name_lower or 'energy' in name_lower:
        return 'loopenergy'
    else:
        return 'gan-charger'  # 默認類別

def generate_page(product_name, lang, category):
    """生成單個頁面文件"""
    # 創建目錄
    page_dir = Path("src") / lang / "products" / category / product_name
    page_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成頁面內容
    page_content = f"""---
title: "{product_name}"
lang: {lang}
permalink: "/{lang}/products/{category}/{product_name}/"
---

{{% include "product-detail.njk" %}}
"""
    
    # 保存文件
    page_file = page_dir / "index.njk"
    with open(page_file, 'w', encoding='utf-8') as f:
        f.write(page_content)

def rebuild_site():
    """重新構建網站"""
    try:
        print("🔄 正在重新構建網站...")
        result = subprocess.run(
            ["npm", "run", "build"], 
            cwd="../", 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 網站重新構建完成")
        else:
            print(f"❌ 網站構建失敗: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 重新構建網站時發生錯誤: {e}")

def main():
    """主函數"""
    print("=== 第三階段: 頁面生成和配置更新 ===")
    
    # 1. 掃描產品目錄
    products = scan_product_directories()
    
    if not products:
        print("❌ 未找到有效的產品")
        return
    
    print(f"📋 找到 {len(products)} 個產品")
    
    # 2. 更新 Eleventy 配置
    if update_eleventy_config(products):
        print("✅ Eleventy 配置已更新")
    else:
        print("❌ Eleventy 配置更新失敗")
        return
    
    # 3. 更新產品目錄
    update_product_catalog(products)
    print("✅ 產品目錄已更新")
    
    # 4. 更新導航選單
    update_navigation(products)
    print("✅ 導航選單已更新")
    
    # 5. 生成頁面文件
    generate_page_files(products)
    
    # 4. 重新構建網站
    rebuild_site()
    
    print("🎉 第三階段處理完成！")

if __name__ == "__main__":
    main() 