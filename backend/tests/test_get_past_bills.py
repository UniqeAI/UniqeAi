import asyncio
import sys
import os

# Backend dizinini Python path'ine ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.services.ai_endpoint_functions import ai_endpoint_functions

async def test_get_past_bills():
    print("\n=== GET PAST BILLS TESTİ ===")
    user_id = 1
    limit = 5
    result = await ai_endpoint_functions.telekom_get_bill_history(user_id=user_id, limit=limit)
    print(f"Kullanıcı ID: {user_id}, Limit: {limit}")
    print(f"Sonuç: {result}")

if __name__ == "__main__":
    asyncio.run(test_get_past_bills()) 