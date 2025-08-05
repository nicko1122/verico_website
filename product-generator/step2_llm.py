#!/usr/bin/env python3
"""
Step 2: LLM 處理
使用 LLM 生成英文和德文 YAML
"""

import json
import yaml
import openai
from pathlib import Path
from config import get_config

def load_step1_data(product_name):
    """載入第一階段的數據"""
    data_file = Path(f"step1_data_{product_name}.json")
    
    if not data_file.exists():
        print(f"❌ 未找到第一階段數據: {data_file}")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ 載入第一階段數據: {data_file}")
    return data

def create_yaml_template(spec_content, image_files, product_name):
    """創建 YAML 模板"""
    template = f"""
請將以下產品文本轉換為結構化的 YAML 格式。

產品文本：
{spec_content}

圖片文件：
{', '.join(image_files)}

請生成完整的 YAML 結構，包含以下部分：
1. product: 基本信息（name, badge, model_name, sku, ean）
2. hero: 英雄區塊（title, subtitle, description, cta_text, cta_link）
3. images: 圖片路徑（使用 /assets/images/product/{product_name}/ 格式）
4. features: 產品特色（title, description, icon）
5. specifications: 技術規格（technical, performance, features）
6. compatibility: 相容性（title, subtitle, devices）
7. package: 包裝內容（section_title, items）
8. product_info: 產品信息（model_name, sku, ean）
9. meta: SEO 信息（title, description, keywords）

注意：
- 圖片路徑應該使用 /assets/images/product/{product_name}/[filename] 格式
- 保持數據準確性和結構完整性
- 適合多語言網站使用

只返回 YAML 內容，不要包含其他文字。
"""
    return template

def generate_yaml_with_llm(prompt, config):
    """使用 LLM 生成 YAML"""
    client = openai.OpenAI(api_key=config['openai_api_key'])
    
    try:
        response = client.chat.completions.create(
            model=config.get('model', 'gpt-4.1-mini'),
            messages=[
                {"role": "system", "content": "你是一個專業的產品數據轉換專家，擅長將產品文本轉換為結構化的 YAML 格式。"},
                {"role": "user", "content": prompt}
            ],
            temperature=config.get('temperature', 0.3),
            max_tokens=config.get('max_tokens', 2000)
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
        print(f"❌ LLM 生成 YAML 時發生錯誤: {e}")
        return None

def generate_german_yaml(en_yaml, config):
    """生成德文版本的 YAML"""
    prompt = f"""
請將以下英文 YAML 翻譯為德文版本。保持相同的結構，只翻譯文本內容。

英文 YAML：
{en_yaml}

請生成德文版本的 YAML，保持相同的結構和格式。
"""

    client = openai.OpenAI(api_key=config['openai_api_key'])
    
    try:
        response = client.chat.completions.create(
            model=config.get('model', 'gpt-4.1-mini'),
            messages=[
                {"role": "system", "content": "你是一個專業的德文翻譯專家，擅長將產品數據從英文翻譯為德文。"},
                {"role": "user", "content": prompt}
            ],
            temperature=config.get('temperature', 0.3),
            max_tokens=config.get('max_tokens', 2000)
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
        print(f"❌ 生成德文 YAML 時發生錯誤: {e}")
        return en_yaml  # 如果翻譯失敗，返回英文版本

def save_yaml_files(product_name, en_yaml, de_yaml):
    """保存 YAML 文件"""
    # 創建產品目錄
    product_dir = Path("src/_data/content/products/details") / product_name
    product_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存英文 YAML
    en_yaml_path = product_dir / 'en.yml'
    with open(en_yaml_path, 'w', encoding='utf-8') as f:
        f.write(en_yaml)
    
    # 保存德文 YAML
    de_yaml_path = product_dir / 'de.yml'
    with open(de_yaml_path, 'w', encoding='utf-8') as f:
        f.write(de_yaml)
    
    print(f"✅ YAML 文件已保存:")
    print(f"  - 英文: {en_yaml_path}")
    print(f"  - 德文: {de_yaml_path}")

def main():
    """主函數"""
    config = get_config()
    
    # 查找第一階段數據文件
    step1_files = list(Path(".").glob("step1_data_*.json"))
    
    if not step1_files:
        print("❌ 未找到第一階段數據文件")
        return
    
    for data_file in step1_files:
        try:
            # 提取產品名稱
            product_name = data_file.stem.replace('step1_data_', '')
            
            # 載入數據
            data = load_step1_data(product_name)
            if not data:
                continue
            
            # 創建模板
            template = create_yaml_template(
                data['spec_content'], 
                data['image_files'], 
                product_name
            )
            
            # 生成英文 YAML
            print(f"🔄 正在生成英文 YAML...")
            en_yaml = generate_yaml_with_llm(template, config)
            
            if en_yaml:
                # 生成德文 YAML
                print(f"🔄 正在生成德文 YAML...")
                de_yaml = generate_german_yaml(en_yaml, config)
                
                # 保存文件
                save_yaml_files(product_name, en_yaml, de_yaml)
                
                print(f"✅ {product_name} 第二階段處理完成")
            else:
                print(f"❌ {product_name} 第二階段處理失敗")
                
        except Exception as e:
            print(f"❌ 處理 {data_file.name} 時發生錯誤: {e}")

if __name__ == "__main__":
    main() 