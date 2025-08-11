# -*- coding: utf-8 -*-
"""
🎯 Ana Entegrasyon Yöneticisi
=============================

Bu script, 3 farklı entegrasyon planını yönetir ve koordine eder.
Tüm planları tek bir arayüzden çalıştırmanızı sağlar.

🔥 Özellikler:
- Plan A: Açık kaynak veri setleri entegrasyonu
- Plan B: Mevcut veri setlerini API uyumlu hale getirme
- Plan C: Sıfırdan sentetik veri seti oluşturma
- Modüler entegrasyon
- Birleşik raporlama
"""

import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import sys
from datetime import datetime
import shutil

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from ai_model.scripts.telekom_api_schema import (
        API_MAP, REQUEST_MODELS, RESPONSE_MODELS, ENDPOINT_MAP
    )
    print("✅ telekom_api_schema başarıyla yüklendi")
except ImportError as e:
    print(f"❌ telekom_api_schema yüklenemedi: {e}")
    sys.exit(1)

class MasterIntegrationManager:
    """
    Ana entegrasyon yöneticisi
    """
    
    def __init__(self):
        self.data_dir = Path(PROJECT_ROOT) / "ai_model" / "data"
        self.results_dir = self.data_dir / "integration_results"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.api_functions = list(API_MAP.keys())
        
        # Plan durumları
        self.plan_status = {
            'plan_a': {'status': 'not_started', 'results': None},
            'plan_b': {'status': 'not_started', 'results': None},
            'plan_c': {'status': 'not_started', 'results': None}
        }
    
    def run_plan_a(self, download_count: int = 1000) -> Dict:
        """Plan A: Açık kaynak veri setleri entegrasyonu"""
        print("🔄 Plan A: Açık Kaynak Veri Setleri Entegrasyonu Başlatılıyor...")
        print("=" * 70)
        
        try:
            # Plan A scriptini import et
            from ai_model.scripts.integration_plans.plan_a_open_source.open_source_dataset_downloader import OpenSourceDatasetDownloader
            
            # İndirici oluştur ve çalıştır
            downloader = OpenSourceDatasetDownloader()
            results = downloader.run_plan_a()
            
            # Sonuçları kaydet
            self.plan_status['plan_a']['status'] = 'completed'
            self.plan_status['plan_a']['results'] = results
            
            print("✅ Plan A tamamlandı!")
            return results
            
        except Exception as e:
            print(f"❌ Plan A hatası: {e}")
            self.plan_status['plan_a']['status'] = 'failed'
            self.plan_status['plan_a']['results'] = {'error': str(e)}
            return {'error': str(e)}
    
    def run_plan_b(self) -> Dict:
        """Plan B: Mevcut veri setlerini API uyumlu hale getirme"""
        print("⚙️ Plan B: Mevcut Veri Setleri Analizi Başlatılıyor...")
        print("=" * 70)
        
        try:
            # Plan B scriptini import et
            from ai_model.scripts.integration_plans.plan_b_existing_data.existing_dataset_analyzer import ExistingDatasetAnalyzer
            
            # Analizör oluştur ve çalıştır
            analyzer = ExistingDatasetAnalyzer()
            results = analyzer.run_plan_b()
            
            # Sonuçları kaydet
            self.plan_status['plan_b']['status'] = 'completed'
            self.plan_status['plan_b']['results'] = {'status': 'analysis_completed'}
            
            print("✅ Plan B tamamlandı!")
            return {'status': 'analysis_completed'}
            
        except Exception as e:
            print(f"❌ Plan B hatası: {e}")
            self.plan_status['plan_b']['status'] = 'failed'
            self.plan_status['plan_b']['results'] = {'error': str(e)}
            return {'error': str(e)}
    
    def run_plan_c(self, records_per_function: int = 50) -> Dict:
        """Plan C: Sıfırdan sentetik veri seti oluşturma"""
        print("🚀 Plan C: Sentetik Veri Seti Üretimi Başlatılıyor...")
        print("=" * 70)
        
        try:
            # Plan C scriptini import et
            from ai_model.scripts.integration_plans.plan_c_synthetic_data.synthetic_data_generator import SyntheticDataGenerator
            
            # Üretici oluştur ve çalıştır
            generator = SyntheticDataGenerator()
            results = generator.run_plan_c(records_per_function * 20)  # Toplam veri sayısı
            
            # Sonuçları kaydet
            self.plan_status['plan_c']['status'] = 'completed'
            self.plan_status['plan_c']['results'] = {'status': 'generation_completed'}
            
            print("✅ Plan C tamamlandı!")
            return {'status': 'generation_completed'}
            
        except Exception as e:
            print(f"❌ Plan C hatası: {e}")
            self.plan_status['plan_c']['status'] = 'failed'
            self.plan_status['plan_c']['results'] = {'error': str(e)}
            return {'error': str(e)}
    
    def run_all_plans(self, plan_a_count: int = 1000, plan_c_count: int = 50) -> Dict:
        """Tüm planları sırayla çalıştır"""
        print("🎯 Tüm Entegrasyon Planları Başlatılıyor...")
        print("=" * 70)
        
        overall_results = {
            'start_time': datetime.now().isoformat(),
            'plans': {},
            'summary': {}
        }
        
        # Plan A
        print("\n🔄 PLAN A BAŞLATILIYOR...")
        plan_a_results = self.run_plan_a(plan_a_count)
        overall_results['plans']['plan_a'] = plan_a_results
        
        # Plan B
        print("\n⚙️ PLAN B BAŞLATILIYOR...")
        plan_b_results = self.run_plan_b()
        overall_results['plans']['plan_b'] = plan_b_results
        
        # Plan C
        print("\n🚀 PLAN C BAŞLATILIYOR...")
        plan_c_results = self.run_plan_c(plan_c_count)
        overall_results['plans']['plan_c'] = plan_c_results
        
        # Özet oluştur
        overall_results['end_time'] = datetime.now().isoformat()
        overall_results['summary'] = self._create_summary()
        
        # Sonuçları kaydet
        self._save_overall_results(overall_results)
        
        print("\n🎯 TÜM PLANLAR TAMAMLANDI!")
        print("=" * 70)
        self._print_summary(overall_results['summary'])
        
        return overall_results
    
    def _create_summary(self) -> Dict:
        """Genel özet oluştur"""
        summary = {
            'total_plans': 3,
            'completed_plans': 0,
            'failed_plans': 0,
            'plan_details': {}
        }
        
        for plan_name, status_info in self.plan_status.items():
            if status_info['status'] == 'completed':
                summary['completed_plans'] += 1
            elif status_info['status'] == 'failed':
                summary['failed_plans'] += 1
            
            summary['plan_details'][plan_name] = {
                'status': status_info['status'],
                'results': status_info['results']
            }
        
        return summary
    
    def _save_overall_results(self, results: Dict):
        """Genel sonuçları kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"master_integration_results_{timestamp}.json"
        output_path = self.results_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Genel sonuçlar kaydedildi: {output_path}")
        
        # Rapor oluştur
        report = self._generate_master_report(results)
        report_path = output_path.with_suffix('.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Master rapor oluşturuldu: {report_path}")
    
    def _generate_master_report(self, results: Dict) -> str:
        """Master rapor oluştur"""
        report = []
        report.append("# 🎯 Master Entegrasyon Raporu")
        report.append(f"📅 Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Genel özet
        summary = results['summary']
        report.append("## 📊 Genel Özet")
        report.append("")
        report.append(f"- **Toplam Plan**: {summary['total_plans']}")
        report.append(f"- **Tamamlanan Plan**: {summary['completed_plans']}")
        report.append(f"- **Başarısız Plan**: {summary['failed_plans']}")
        report.append(f"- **Başarı Oranı**: {(summary['completed_plans'] / summary['total_plans']) * 100:.1f}%")
        report.append("")
        
        # Plan detayları
        report.append("## 📈 Plan Detayları")
        report.append("")
        
        for plan_name, details in summary['plan_details'].items():
            status_emoji = "✅" if details['status'] == 'completed' else "❌" if details['status'] == 'failed' else "⏳"
            report.append(f"### {status_emoji} {plan_name.upper()}")
            report.append(f"- **Durum**: {details['status']}")
            
            if details['results']:
                if 'error' in details['results']:
                    report.append(f"- **Hata**: {details['results']['error']}")
                elif 'status' in details['results']:
                    report.append(f"- **Sonuç**: {details['results']['status']}")
                elif 'total_records' in details['results']:
                    report.append(f"- **Toplam Kayıt**: {details['results']['total_records']}")
            
            report.append("")
        
        # Öneriler
        report.append("## 💡 Öneriler")
        report.append("")
        
        if summary['completed_plans'] == 3:
            report.append("- **Mükemmel**: Tüm planlar başarıyla tamamlandı!")
            report.append("- **Sonraki Adım**: Entegre veri setlerini birleştirin")
        elif summary['completed_plans'] >= 2:
            report.append("- **İyi**: Çoğu plan başarıyla tamamlandı")
            report.append("- **Sonraki Adım**: Başarısız planı tekrar deneyin")
        else:
            report.append("- **Dikkat**: Çoğu plan başarısız oldu")
            report.append("- **Sonraki Adım**: Hataları kontrol edin ve tekrar deneyin")
        
        report.append("")
        
        return "\n".join(report)
    
    def _print_summary(self, summary: Dict):
        """Özeti yazdır"""
        print(f"📊 Toplam Plan: {summary['total_plans']}")
        print(f"✅ Tamamlanan: {summary['completed_plans']}")
        print(f"❌ Başarısız: {summary['failed_plans']}")
        print(f"📈 Başarı Oranı: {(summary['completed_plans'] / summary['total_plans']) * 100:.1f}%")
        
        print(f"\n📁 Çıktı Dosyaları:")
        print(f"   - Sonuçlar: {self.results_dir}")
    
    def show_plan_menu(self):
        """Plan seçim menüsü göster"""
        print("🎯 Entegrasyon Planı Seçin:")
        print("=" * 50)
        print("1. 🔄 Plan A: Açık Kaynak Veri Setleri")
        print("2. ⚙️ Plan B: Mevcut Veri Setleri Analizi")
        print("3. 🚀 Plan C: Sentetik Veri Seti Üretimi")
        print("4. 🎯 Tüm Planları Çalıştır")
        print("5. 📊 Durum Raporu")
        print("6. ❌ Çıkış")
        print("=" * 50)
    
    def interactive_mode(self):
        """Etkileşimli mod"""
        while True:
            self.show_plan_menu()
            
            try:
                choice = input("Seçiminizi yapın (1-6): ").strip()
                
                if choice == '1':
                    count = input("İndirilecek veri sayısı (varsayılan: 1000): ").strip()
                    count = int(count) if count.isdigit() else 1000
                    self.run_plan_a(count)
                    
                elif choice == '2':
                    self.run_plan_b()
                    
                elif choice == '3':
                    count = input("Fonksiyon başına kayıt sayısı (varsayılan: 50): ").strip()
                    count = int(count) if count.isdigit() else 50
                    self.run_plan_c(count)
                    
                elif choice == '4':
                    plan_a_count = input("Plan A için veri sayısı (varsayılan: 1000): ").strip()
                    plan_a_count = int(plan_a_count) if plan_a_count.isdigit() else 1000
                    
                    plan_c_count = input("Plan C için fonksiyon başına kayıt (varsayılan: 50): ").strip()
                    plan_c_count = int(plan_c_count) if plan_c_count.isdigit() else 50
                    
                    self.run_all_plans(plan_a_count, plan_c_count)
                    
                elif choice == '5':
                    self._print_summary(self._create_summary())
                    
                elif choice == '6':
                    print("👋 Görüşürüz!")
                    break
                    
                else:
                    print("❌ Geçersiz seçim! Lütfen 1-6 arası bir sayı girin.")
                
                input("\nDevam etmek için Enter'a basın...")
                
            except KeyboardInterrupt:
                print("\n👋 Görüşürüz!")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
                input("\nDevam etmek için Enter'a basın...")

def main():
    """Ana fonksiyon"""
    print("🎯 Master Entegrasyon Yöneticisi")
    print("=" * 60)
    
    manager = MasterIntegrationManager()
    
    # Komut satırı argümanlarını kontrol et
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'plan-a':
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
            manager.run_plan_a(count)
        elif command == 'plan-b':
            manager.run_plan_b()
        elif command == 'plan-c':
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            manager.run_plan_c(count)
        elif command == 'all':
            plan_a_count = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
            plan_c_count = int(sys.argv[3]) if len(sys.argv) > 3 else 50
            manager.run_all_plans(plan_a_count, plan_c_count)
        else:
            print("❌ Geçersiz komut!")
            print("Kullanım:")
            print("  python master_integration_manager.py plan-a [count]")
            print("  python master_integration_manager.py plan-b")
            print("  python master_integration_manager.py plan-c [count]")
            print("  python master_integration_manager.py all [plan_a_count] [plan_c_count]")
    else:
        # Etkileşimli mod
        manager.interactive_mode()

if __name__ == "__main__":
    main() 