#!/usr/bin/env python3
"""
自動處理所有階段
一次性運行完整的產品處理流程
"""

import subprocess
import sys
from pathlib import Path

def run_stage(stage_name, script_name):
    """運行單個階段"""
    print(f"\n=== 運行 {stage_name} ===")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {stage_name} 完成")
            print(result.stdout)
        else:
            print(f"❌ {stage_name} 失敗")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 運行 {stage_name} 時發生錯誤: {e}")
        return False
    
    return True

def cleanup_intermediate_files():
    """清理中間文件"""
    print("\n=== 清理中間文件 ===")
    
    # 清理第一階段數據文件
    step1_files = list(Path(".").glob("step1_data_*.json"))
    for file in step1_files:
        file.unlink()
        print(f"🗑️  已刪除: {file.name}")
    
    # 清理臨時目錄
    temp_dirs = list(Path(".").glob("temp_*"))
    for temp_dir in temp_dirs:
        if temp_dir.is_dir():
            import shutil
            shutil.rmtree(temp_dir)
            print(f"🗑️  已刪除: {temp_dir.name}")

def main():
    """主函數"""
    print("🚀 開始自動處理所有階段")
    
    # 檢查是否有 ZIP 文件
    zip_files = list(Path("product-packages").glob("*.zip"))
    
    if not zip_files:
        print("❌ 未找到 ZIP 文件，請將產品包放入 product-packages/ 目錄")
        return
    
    print(f"📦 找到 {len(zip_files)} 個產品包:")
    for zip_file in zip_files:
        print(f"  - {zip_file.name}")
    
    # 運行各階段
    stages = [
        ("第一階段: 文件處理", "step1_extract.py"),
        ("第二階段: LLM 處理", "step2_llm.py"),
        ("第三階段: 頁面生成", "step3_pages.py")
    ]
    
    for stage_name, script_name in stages:
        if not run_stage(stage_name, script_name):
            print(f"\n❌ 處理失敗，停止執行")
            return
    
    # 清理中間文件
    cleanup_intermediate_files()
    
    print("\n🎉 所有階段處理完成！")
    print("📋 新產品已添加到網站中")

if __name__ == "__main__":
    main() 