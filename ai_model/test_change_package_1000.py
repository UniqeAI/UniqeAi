#!/usr/bin/env python3
"""
1000 Change Package Senaryosu Test Scripti
"""

import json
import os
import sys
sys.path.append('modular_generator')

from modular_generator.generators.basic_scenarios.change_package import (
    generate_1000_unique_scenarios, 
    get_scenario_statistics
)

def main():
    print("🚀 1000 Change Package Senaryosu Test Ediliyor...")
    print("=" * 60)
    
    # 1000 senaryo üret
    scenarios = generate_1000_unique_scenarios()
    
    # İstatistikleri hesapla
    stats = get_scenario_statistics(scenarios)
    
    # Detaylı rapor
    print("\n📊 DETAYLI RAPOR:")
    print(f"📈 Toplam senaryo: {stats['total_scenarios']}")
    print(f"✅ Geçerli senaryo: {stats['quality_metrics']['valid_scenarios']}")
    print(f"❌ Geçersiz senaryo: {stats['quality_metrics']['invalid_scenarios']}")
    print(f"🎯 Ortalama karmaşıklık: {stats['quality_metrics']['average_complexity']:.3f}")
    
    # Paket çeşitliliği
    packages = [s['donguler'][2]['arac_cagrilari'][0]['parametreler']['new_package_name'] for s in scenarios]
    unique_packages = set(packages)
    print(f"\n📦 Paket çeşitliliği: {len(unique_packages)} farklı paket")
    
    # En popüler paketler
    from collections import Counter
    package_counts = Counter(packages)
    print("\n🎯 En popüler 5 paket:")
    for pkg, count in package_counts.most_common(5):
        print(f"  {pkg}: {count} kez (%{count/len(scenarios)*100:.1f})")
    
    # JSON'a kaydet
    filename = 'change_package_1000_scenarios.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scenarios, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 {len(scenarios)} senaryo {filename} dosyasına kaydedildi")
    print(f"📁 Dosya boyutu: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")
    
    # Örnek senaryo göster
    print(f"\n📋 ÖRNEK SENARYO:")
    sample = scenarios[0]
    print(f"ID: {sample['id']}")
    print(f"Kişilik: {sample['personality_profile']}")
    print(f"Bilişsel: {sample['cognitive_state']}")
    print(f"Duygusal: {sample['emotional_context']}")
    print(f"Paket: {sample['donguler'][2]['arac_cagrilari'][0]['parametreler']['new_package_name']}")
    print(f"Kullanıcı: {sample['donguler'][0]['icerik']}")
    print(f"Fingerprint: {sample['fingerprint']}")
    
    print("\n🎉 Test tamamlandı!")

if __name__ == "__main__":
    main() 