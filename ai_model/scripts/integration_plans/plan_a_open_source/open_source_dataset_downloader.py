#!/usr/bin/env python3
"""
Plan A: Açık Kaynak Veri Seti Entegrasyonu
==========================================

Bu script, HuggingFace, Kaggle ve GitHub'dan açık kaynak veri setlerini indirir
ve Telekom API şemasına uygun hale getirir.

Özellikler:
- Çoklu kaynak desteği (HuggingFace, Kaggle, GitHub)
- API token kontrolü ve mock data fallback
- Otomatik veri temizleme ve format dönüştürme
- Telekom API şemasına uyumluluk kontrolü
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

# Ana dizini Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent.parent))

from telekom_api_schema import TelekomAPI
from ultimate_api_compatibility_system import UltimateAPIFieldMapper, UltimatePydanticValidator

class OpenSourceDatasetDownloader:
    def __init__(self):
        self.output_dir = Path("data/open_source_datasets")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # API token kontrolü
        self.hf_token = os.getenv("HF_TOKEN")
        self.kaggle_token = os.getenv("KAGGLE_API_TOKEN")
        
        # Telekom API şeması
        self.api_schema = TelekomAPI()
        
        # API uyumluluk sistemleri
        self.field_mapper = UltimateAPIFieldMapper()
        self.validator = UltimatePydanticValidator()
        
    def download_huggingface_dataset(self, dataset_name, split="train"):
        """HuggingFace'dan veri seti indir"""
        try:
            if not self.hf_token:
                print("⚠️  HF_TOKEN bulunamadı. Mock data oluşturuluyor...")
                return self.create_mock_hf_dataset(dataset_name)
            
            from datasets import load_dataset
            
            print(f"📥 HuggingFace'dan {dataset_name} indiriliyor...")
            dataset = load_dataset(dataset_name, split=split, token=self.hf_token)
            
            # Veriyi DataFrame'e dönüştür
            if hasattr(dataset, 'to_pandas'):
                df = dataset.to_pandas()
            else:
                df = pd.DataFrame(dataset)
            
            return df
            
        except Exception as e:
            print(f"❌ HuggingFace indirme hatası: {e}")
            return self.create_mock_hf_dataset(dataset_name)
    
    def download_kaggle_dataset(self, dataset_name):
        """Kaggle'dan veri seti indir"""
        try:
            if not self.kaggle_token:
                print("⚠️  KAGGLE_API_TOKEN bulunamadı. Mock data oluşturuluyor...")
                return self.create_mock_kaggle_dataset(dataset_name)
            
            import kaggle
            
            print(f"📥 Kaggle'dan {dataset_name} indiriliyor...")
            kaggle.api.dataset_download_files(dataset_name, path="temp", unzip=True)
            
            # CSV dosyalarını bul ve yükle
            csv_files = list(Path("temp").glob("*.csv"))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                return df
            else:
                return self.create_mock_kaggle_dataset(dataset_name)
                
        except Exception as e:
            print(f"❌ Kaggle indirme hatası: {e}")
            return self.create_mock_kaggle_dataset(dataset_name)
    
    def download_github_dataset(self, repo_url, file_path):
        """GitHub'dan veri seti indir"""
        try:
            print(f"📥 GitHub'dan {repo_url}/{file_path} indiriliyor...")
            
            # GitHub raw URL'ini oluştur
            raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + "/main/" + file_path
            
            response = requests.get(raw_url)
            response.raise_for_status()
            
            # JSON dosyası ise
            if file_path.endswith('.json'):
                data = response.json()
                return pd.DataFrame(data)
            # CSV dosyası ise
            elif file_path.endswith('.csv'):
                return pd.read_csv(io.StringIO(response.text))
            else:
                return self.create_mock_github_dataset(repo_url, file_path)
                
        except Exception as e:
            print(f"❌ GitHub indirme hatası: {e}")
            return self.create_mock_github_dataset(repo_url, file_path)
    
    def create_mock_hf_dataset(self, dataset_name):
        """HuggingFace için mock data oluştur"""
        print(f"🔄 {dataset_name} için mock data oluşturuluyor...")
        
        mock_data = []
        for i in range(100):
            mock_data.append({
                "question": f"Mock soru {i+1} - {dataset_name}",
                "answer": f"Mock cevap {i+1} - {dataset_name}",
                "category": "mock_category",
                "source": f"mock_{dataset_name}",
                "confidence": 0.8
            })
        
        return pd.DataFrame(mock_data)
    
    def create_mock_kaggle_dataset(self, dataset_name):
        """Kaggle için mock data oluştur"""
        print(f"🔄 {dataset_name} için mock data oluşturuluyor...")
        
        mock_data = []
        for i in range(100):
            mock_data.append({
                "question": f"Kaggle mock soru {i+1}",
                "answer": f"Kaggle mock cevap {i+1}",
                "category": "kaggle_mock",
                "source": f"mock_{dataset_name}",
                "confidence": 0.85
            })
        
        return pd.DataFrame(mock_data)
    
    def create_mock_github_dataset(self, repo_url, file_path):
        """GitHub için mock data oluştur"""
        print(f"🔄 {repo_url}/{file_path} için mock data oluşturuluyor...")
        
        mock_data = []
        for i in range(100):
            mock_data.append({
                "question": f"GitHub mock soru {i+1}",
                "answer": f"GitHub mock cevap {i+1}",
                "category": "github_mock",
                "source": f"mock_{Path(repo_url).name}",
                "confidence": 0.9
            })
        
        return pd.DataFrame(mock_data)
    
    def apply_api_compatibility(self, df, source_name):
        """Veriyi Telekom API şemasına uygun hale getir"""
        print(f"🔧 {source_name} için API uyumluluğu uygulanıyor...")
        
        compatible_data = []
        
        for _, row in df.iterrows():
            try:
                # Alan eşleştirme
                mapped_data = self.field_mapper.map_fields_to_api(row.to_dict())
                
                # Pydantic doğrulama
                validated_data = self.validator.ensure_api_compatibility(mapped_data)
                
                if validated_data:
                    compatible_data.append(validated_data)
                    
            except Exception as e:
                print(f"⚠️  Satır işleme hatası: {e}")
                continue
        
        return pd.DataFrame(compatible_data)
    
    def save_dataset(self, df, source_name):
        """Veri setini kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source_name}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        # DataFrame'i JSON'a dönüştür
        data_list = df.to_dict('records')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Veri seti kaydedildi: {filepath}")
        return filepath
    
    def run_plan_a(self):
        """Plan A'yı çalıştır"""
        print("🚀 Plan A: Açık Kaynak Veri Seti Entegrasyonu Başlatılıyor...")
        print("=" * 60)
        
        # Önerilen veri setleri
        datasets = [
            {
                "name": "turkish_qa",
                "type": "huggingface",
                "source": "mukayese/turkish-qa",
                "description": "Türkçe Soru-Cevap veri seti"
            },
            {
                "name": "customer_service",
                "type": "kaggle",
                "source": "datasets/ankurankan/customer-service-conversations",
                "description": "Müşteri hizmetleri konuşmaları"
            },
            {
                "name": "telecom_qa",
                "type": "github",
                "source": "https://github.com/example/telecom-qa",
                "file": "data/qa_pairs.json",
                "description": "Telekom sektörü soru-cevapları"
            }
        ]
        
        downloaded_datasets = []
        
        for dataset in datasets:
            print(f"\n📋 {dataset['name']} işleniyor...")
            print(f"📝 {dataset['description']}")
            
            # Veri setini indir
            if dataset['type'] == 'huggingface':
                df = self.download_huggingface_dataset(dataset['source'])
            elif dataset['type'] == 'kaggle':
                df = self.download_kaggle_dataset(dataset['source'])
            elif dataset['type'] == 'github':
                df = self.download_github_dataset(dataset['source'], dataset['file'])
            else:
                continue
            
            print(f"📊 İndirilen veri: {len(df)} satır")
            
            # API uyumluluğu uygula
            compatible_df = self.apply_api_compatibility(df, dataset['name'])
            print(f"✅ API uyumlu veri: {len(compatible_df)} satır")
            
            # Kaydet
            filepath = self.save_dataset(compatible_df, dataset['name'])
            downloaded_datasets.append({
                'name': dataset['name'],
                'filepath': str(filepath),
                'original_count': len(df),
                'compatible_count': len(compatible_df),
                'compatibility_rate': len(compatible_df) / len(df) * 100 if len(df) > 0 else 0
            })
        
        # Özet rapor oluştur
        self.create_summary_report(downloaded_datasets)
        
        print("\n🎉 Plan A tamamlandı!")
        return downloaded_datasets
    
    def create_summary_report(self, datasets):
        """Özet rapor oluştur"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"plan_a_summary_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Plan A: Açık Kaynak Veri Seti Entegrasyonu Özeti\n\n")
            f.write(f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## İndirilen Veri Setleri\n\n")
            f.write("| Veri Seti | Dosya | Orijinal | Uyumlu | Uyumluluk Oranı |\n")
            f.write("|-----------|-------|----------|--------|-----------------|\n")
            
            for dataset in datasets:
                f.write(f"| {dataset['name']} | {Path(dataset['filepath']).name} | "
                       f"{dataset['original_count']} | {dataset['compatible_count']} | "
                       f"{dataset['compatibility_rate']:.1f}% |\n")
            
            f.write(f"\n**Toplam İndirilen:** {len(datasets)} veri seti\n")
            f.write(f"**Toplam Uyumlu Veri:** {sum(d['compatible_count'] for d in datasets)} satır\n")
        
        print(f"📄 Özet rapor oluşturuldu: {report_path}")

if __name__ == "__main__":
    downloader = OpenSourceDatasetDownloader()
    results = downloader.run_plan_a()
    
    print(f"\n📊 Sonuçlar:")
    for result in results:
        print(f"  • {result['name']}: {result['compatible_count']} uyumlu veri "
              f"({result['compatibility_rate']:.1f}% uyumluluk)") 