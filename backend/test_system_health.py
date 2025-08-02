#!/usr/bin/env python3
"""
Sistem durumu test scripti
"""

import asyncio
import sys
import os

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.services.ai_endpoint_functions import ai_endpoint_functions

async def test_system_health():
    """Sistem durumu fonksiyonunu test et"""
    print("🔧 Sistem Durumu Testi")
    print("=" * 50)
    
    try:
        # system_get_health fonksiyonunu test et
        result = await ai_endpoint_functions.system_get_health()
        print(f"✅ system_get_health sonucu:")
        print(f"Success: {result.get('success')}")
        print(f"Data: {result.get('data')}")
        
        if result.get('success'):
            data = result.get('data', {})
            print(f"Status: {data.get('status')}")
            print(f"Version: {data.get('version')}")
            print(f"Components: {data.get('components')}")
        else:
            print(f"Error: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_system_health()) 