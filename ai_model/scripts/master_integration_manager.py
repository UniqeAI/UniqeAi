#!/usr/bin/env python3
"""
Ana Entegrasyon Yöneticisi
==========================

Bu script, üç farklı entegrasyon planını (A, B, C) yönetir ve koordine eder.
Kullanıcı tek bir yerden tüm planları çalıştırabilir ve sonuçları görebilir.

Özellikler:
- Plan A: Açık Kaynak Veri Seti Entegrasyonu
- Plan B: Mevcut Veri Seti İşleme ve İyileştirme
- Plan C: %100 API Uyumlu Sentetik Veri Üretimi
- Kombine raporlama
- İnteraktif menü
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Ana dizini Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent))

class MasterIntegrationManager:
    def __init__(self):
        self.output_dir = Path("data/integration_results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Plan script'lerinin yolları
        self.plan_scripts = {
            'A': Path(__file__).parent / "integration_plans" / "plan_a_open_source" / "open_source_dataset_downloader.py",
            'B': Path(__file__).parent / "integration_plans" / "plan_b_existing_data" / "existing_dataset_analyzer.py",
            'C': Path(__file__).parent / "integration_plans" / "plan_c_synthetic_data" / "synthetic_data_generator.py"
        }
        
        # Plan açıklamaları
        self.plan_descriptions = {
            'A': "Açık Kaynak Veri Seti Entegrasyonu - HuggingFace, Kaggle, GitHub'dan veri indirir",
            'B': "Mevcut Veri Seti İşleme - Mevcut verileri analiz eder ve iyileştirir",
            'C': "Sentetik Veri Üretimi - %100 API uyumlu yeni veri üretir"
        }
        
        # Sonuçlar
        self.results = {}
        
    def run_plan_a(self) -> Dict[str, Any]:
        """Plan A'yı çalıştır"""
        print("\n🚀 Plan A: Açık Kaynak Veri Seti Entegrasyonu Başlatılıyor...")
        print("=" * 60)
        
        try:
            # Plan A script'ini import et ve çalıştır
            sys.path.append(str(self.plan_scripts['A'].parent))
            
            # Script'i doğrudan çalıştır
            import subprocess
            result = subprocess.run([
                sys.executable, 
                str(self.plan_scripts['A'])
            ], capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                print("✅ Plan A başarıyla tamamlandı!")
                return {
                    'status': 'success',
                    'output': result.stdout,
                    'error': result.stderr
                }
            else:
                print(f"❌ Plan A hatası: {result.stderr}")
                return {
                    'status': 'error',
                    'output': result.stdout,
                    'error': result.stderr
                }
                
        except Exception as e:
            print(f"❌ Plan A çalıştırma hatası: {e}")
            return {
                'status': 'error',
                'output': '',
                'error': str(e)
            }
    
    def run_plan_b(self) -> Dict[str, Any]:
        """Plan B'yi çalıştır"""
        print("\n🚀 Plan B: Mevcut Veri Seti İşleme ve İyileştirme Başlatılıyor...")
        print("=" * 60)
        
        try:
            # Plan B script'ini import et ve çalıştır
            sys.path.append(str(self.plan_scripts['B'].parent))
            
            import subprocess
            result = subprocess.run([
                sys.executable, 
                str(self.plan_scripts['B'])
            ], capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                print("✅ Plan B başarıyla tamamlandı!")
                return {
                    'status': 'success',
                    'output': result.stdout,
                    'error': result.stderr
                }
            else:
                print(f"❌ Plan B hatası: {result.stderr}")
                return {
                    'status': 'error',
                    'output': result.stdout,
                    'error': result.stderr
                }
                
        except Exception as e:
            print(f"❌ Plan B çalıştırma hatası: {e}")
            return {
                'status': 'error',
                'output': '',
                'error': str(e)
            }
    
    def run_plan_c(self) -> Dict[str, Any]:
        """Plan C'yi çalıştır"""
        print("\n🚀 Plan C: %100 API Uyumlu Sentetik Veri Üretimi Başlatılıyor...")
        print("=" * 60)
        
        try:
            # Plan C script'ini import et ve çalıştır
            sys.path.append(str(self.plan_scripts['C'].parent))
            
            import subprocess
            result = subprocess.run([
                sys.executable, 
                str(self.plan_scripts['C'])
            ], capture_output=True, text=True, cwd=Path.cwd())
            
            if result.returncode == 0:
                print("✅ Plan C başarıyla tamamlandı!")
                return {
                    'status': 'success',
                    'output': result.stdout,
                    'error': result.stderr
                }
            else:
                print(f"❌ Plan C hatası: {result.stderr}")
                return {
                    'status': 'error',
                    'output': result.stdout,
                    'error': result.stderr
                }
                
        except Exception as e:
            print(f"❌ Plan C çalıştırma hatası: {e}")
            return {
                'status': 'error',
                'output': '',
                'error': str(e)
            }
    
    def run_all_plans(self) -> Dict[str, Any]:
        """Tüm planları sırayla çalıştır"""
        print("🚀 Tüm Entegrasyon Planları Başlatılıyor...")
        print("=" * 60)
        
        all_results = {}
        
        # Plan A
        print("\n📋 Plan A çalıştırılıyor...")
        all_results['A'] = self.run_plan_a()
        
        # Plan B
        print("\n📋 Plan B çalıştırılıyor...")
        all_results['B'] = self.run_plan_b()
        
        # Plan C
        print("\n📋 Plan C çalıştırılıyor...")
        all_results['C'] = self.run_plan_c()
        
        # Kombine rapor oluştur
        self.create_combined_report(all_results)
        
        return all_results
    
    def create_combined_report(self, results: Dict[str, Any]):
        """Kombine rapor oluştur"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"combined_integration_report_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Entegrasyon Planları Kombine Raporu\n\n")
            f.write(f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Genel Özet\n\n")
            
            success_count = sum(1 for result in results.values() if result['status'] == 'success')
            total_count = len(results)
            
            f.write(f"- **Toplam Plan Sayısı:** {total_count}\n")
            f.write(f"- **Başarılı Plan Sayısı:** {success_count}\n")
            f.write(f"- **Başarı Oranı:** {(success_count/total_count)*100:.1f}%\n\n")
            
            f.write("## Detaylı Sonuçlar\n\n")
            
            for plan, result in results.items():
                f.write(f"### Plan {plan}\n\n")
                f.write(f"**Açıklama:** {self.plan_descriptions[plan]}\n\n")
                f.write(f"**Durum:** {'✅ Başarılı' if result['status'] == 'success' else '❌ Hata'}\n\n")
                
                if result['error']:
                    f.write(f"**Hata:** {result['error']}\n\n")
                
                if result['output']:
                    f.write("**Çıktı:**\n")
                    f.write("```\n")
                    f.write(result['output'][:1000])  # İlk 1000 karakter
                    f.write("\n```\n\n")
            
            f.write("## Öneriler\n\n")
            
            if success_count == total_count:
                f.write("🎉 Tüm planlar başarıyla tamamlandı! Veri entegrasyonu tamamlanmıştır.\n\n")
            elif success_count > 0:
                f.write("⚠️  Bazı planlar başarısız oldu. Başarılı planların sonuçları kullanılabilir.\n\n")
            else:
                f.write("❌ Hiçbir plan başarılı olmadı. Hataları kontrol edin ve tekrar deneyin.\n\n")
        
        print(f"📄 Kombine rapor oluşturuldu: {report_path}")
        return report_path
    
    def show_menu(self):
        """İnteraktif menü göster"""
        while True:
            print("\n" + "="*60)
            print("🎯 ENTEGRASYON PLANLARI YÖNETİCİSİ")
            print("="*60)
            print("1. Plan A: Açık Kaynak Veri Seti Entegrasyonu")
            print("2. Plan B: Mevcut Veri Seti İşleme ve İyileştirme")
            print("3. Plan C: %100 API Uyumlu Sentetik Veri Üretimi")
            print("4. Tüm Planları Çalıştır")
            print("5. Plan Açıklamalarını Göster")
            print("6. Çıkış")
            print("="*60)
            
            choice = input("\nSeçiminizi yapın (1-6): ").strip()
            
            if choice == '1':
                self.results['A'] = self.run_plan_a()
            elif choice == '2':
                self.results['B'] = self.run_plan_b()
            elif choice == '3':
                self.results['C'] = self.run_plan_c()
            elif choice == '4':
                self.results = self.run_all_plans()
            elif choice == '5':
                self.show_plan_descriptions()
            elif choice == '6':
                print("👋 Çıkış yapılıyor...")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-6 arasında bir sayı girin.")
    
    def show_plan_descriptions(self):
        """Plan açıklamalarını göster"""
        print("\n📋 PLAN AÇIKLAMALARI")
        print("="*60)
        
        for plan, description in self.plan_descriptions.items():
            print(f"\n🔹 Plan {plan}:")
            print(f"   {description}")
        
        print("\n" + "="*60)
        input("Devam etmek için Enter'a basın...")
    
    def show_quick_start(self):
        """Hızlı başlangıç rehberi"""
        print("\n🚀 HIZLI BAŞLANGIÇ REHBERİ")
        print("="*60)
        print("1. Plan C (Sentetik Veri) - En hızlı ve güvenilir seçenek")
        print("2. Plan B (Mevcut Veri) - Mevcut verilerinizi iyileştirin")
        print("3. Plan A (Açık Kaynak) - Dış kaynaklardan veri entegre edin")
        print("4. Tüm Planlar - Kapsamlı entegrasyon")
        print("="*60)
        
        choice = input("\nHangi planı denemek istiyorsunuz? (1-4): ").strip()
        
        if choice == '1':
            self.results['C'] = self.run_plan_c()
        elif choice == '2':
            self.results['B'] = self.run_plan_b()
        elif choice == '3':
            self.results['A'] = self.run_plan_a()
        elif choice == '4':
            self.results = self.run_all_plans()
        else:
            print("❌ Geçersiz seçim!")

def main():
    """Ana fonksiyon"""
    manager = MasterIntegrationManager()
    
    print("🎯 Telekom AI Veri Entegrasyon Sistemi")
    print("="*60)
    print("Bu sistem üç farklı entegrasyon planını yönetir:")
    print("• Plan A: Açık kaynak veri setleri")
    print("• Plan B: Mevcut veri işleme")
    print("• Plan C: Sentetik veri üretimi")
    print("="*60)
    
    # Argüman kontrolü
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        
        if arg == 'A':
            manager.results['A'] = manager.run_plan_a()
        elif arg == 'B':
            manager.results['B'] = manager.run_plan_b()
        elif arg == 'C':
            manager.results['C'] = manager.run_plan_c()
        elif arg == 'ALL':
            manager.results = manager.run_all_plans()
        elif arg == 'QUICK':
            manager.show_quick_start()
        else:
            print(f"❌ Geçersiz argüman: {arg}")
            print("Kullanım: python master_integration_manager.py [A|B|C|ALL|QUICK]")
    else:
        # İnteraktif mod
        manager.show_menu()
    
    # Sonuçları göster
    if manager.results:
        print("\n📊 SONUÇLAR")
        print("="*60)
        for plan, result in manager.results.items():
            status = "✅ Başarılı" if result['status'] == 'success' else "❌ Hata"
            print(f"Plan {plan}: {status}")

if __name__ == "__main__":
    main() 