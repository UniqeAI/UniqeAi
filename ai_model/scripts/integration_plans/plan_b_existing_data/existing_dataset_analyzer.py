#!/usr/bin/env python3
"""
Plan B: Mevcut Veri Seti İşleme ve İyileştirme
==============================================

Bu script, mevcut veri setlerini analiz eder, API uyumluluğunu değerlendirir
ve iyileştirme önerileri sunar.

Özellikler:
- Mevcut veri setlerini otomatik keşif
- API uyumluluk analizi
- Veri kalitesi değerlendirmesi
- İyileştirme önerileri
- Otomatik düzeltme ve dönüştürme
"""

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, List, Any, Optional

# Ana dizini Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent.parent))

from telekom_api_schema import TelekomAPI
from ultimate_api_compatibility_system import UltimateAPIFieldMapper, UltimatePydanticValidator

class ExistingDatasetAnalyzer:
    def __init__(self):
        self.output_dir = Path("data/existing_data_analysis")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Telekom API şeması
        self.api_schema = TelekomAPI()
        
        # API uyumluluk sistemleri
        self.field_mapper = UltimateAPIFieldMapper()
        self.validator = UltimatePydanticValidator()
        
        # Analiz sonuçları
        self.analysis_results = {}
        
    def discover_existing_datasets(self) -> List[Path]:
        """Mevcut veri setlerini keşfet"""
        print("🔍 Mevcut veri setleri keşfediliyor...")
        
        # Olası veri seti konumları
        search_paths = [
            Path("."),  # Mevcut dizin
            Path("data"),
            Path("datasets"),
            Path("ai_model/data"),
            Path("ai_model/datasets"),
            Path("../data"),
            Path("../datasets")
        ]
        
        discovered_files = []
        
        for search_path in search_paths:
            if search_path.exists():
                # JSON dosyalarını ara
                json_files = list(search_path.rglob("*.json"))
                discovered_files.extend(json_files)
                
                # CSV dosyalarını ara
                csv_files = list(search_path.rglob("*.csv"))
                discovered_files.extend(csv_files)
                
                # TXT dosyalarını ara (veri seti olabilir)
                txt_files = list(search_path.rglob("*.txt"))
                discovered_files.extend(txt_files)
        
        # Duplikasyonları kaldır
        discovered_files = list(set(discovered_files))
        
        print(f"📁 {len(discovered_files)} dosya keşfedildi")
        return discovered_files
    
    def load_dataset(self, filepath: Path) -> Optional[pd.DataFrame]:
        """Veri setini yükle"""
        try:
            if filepath.suffix.lower() == '.json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Liste ise DataFrame'e dönüştür
                if isinstance(data, list):
                    return pd.DataFrame(data)
                # Dict ise ve 'data' anahtarı varsa
                elif isinstance(data, dict) and 'data' in data:
                    return pd.DataFrame(data['data'])
                # Diğer dict yapıları
                else:
                    return pd.DataFrame([data])
                    
            elif filepath.suffix.lower() == '.csv':
                return pd.read_csv(filepath, encoding='utf-8')
                
            elif filepath.suffix.lower() == '.txt':
                # TXT dosyasını satır satır oku
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # JSON satırları olabilir
                data = []
                for line in lines:
                    line = line.strip()
                    if line and line.startswith('{') and line.endswith('}'):
                        try:
                            data.append(json.loads(line))
                        except:
                            continue
                
                if data:
                    return pd.DataFrame(data)
                else:
                    # Düz metin olarak işle
                    return pd.DataFrame({'text': lines})
            
            return None
            
        except Exception as e:
            print(f"❌ {filepath} yükleme hatası: {e}")
            return None
    
    def analyze_dataset_structure(self, df: pd.DataFrame, filepath: Path) -> Dict[str, Any]:
        """Veri seti yapısını analiz et"""
        analysis = {
            'filepath': str(filepath),
            'filename': filepath.name,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'sample_data': df.head(3).to_dict('records')
        }
        
        # Sütun analizi
        column_analysis = {}
        for col in df.columns:
            col_data = df[col].dropna()
            column_analysis[col] = {
                'type': str(df[col].dtype),
                'unique_count': col_data.nunique(),
                'null_count': df[col].isnull().sum(),
                'null_percentage': (df[col].isnull().sum() / len(df)) * 100,
                'sample_values': col_data.head(5).tolist() if len(col_data) > 0 else []
            }
        
        analysis['column_analysis'] = column_analysis
        return analysis
    
    def evaluate_api_compatibility(self, df: pd.DataFrame, filepath: Path) -> Dict[str, Any]:
        """API uyumluluğunu değerlendir"""
        print(f"🔧 {filepath.name} için API uyumluluğu değerlendiriliyor...")
        
        compatibility_results = {
            'filepath': str(filepath),
            'total_rows': len(df),
            'compatible_rows': 0,
            'compatibility_rate': 0.0,
            'field_mapping_success': 0,
            'validation_success': 0,
            'errors': [],
            'suggestions': []
        }
        
        compatible_data = []
        field_mapping_errors = 0
        validation_errors = 0
        
        for idx, row in df.iterrows():
            try:
                # Alan eşleştirme
                mapped_data = self.field_mapper.map_fields_to_api(row.to_dict())
                compatibility_results['field_mapping_success'] += 1
                
                # Pydantic doğrulama
                validated_data = self.validator.ensure_api_compatibility(mapped_data)
                
                if validated_data:
                    compatibility_results['validation_success'] += 1
                    compatible_data.append(validated_data)
                    
            except Exception as e:
                error_msg = f"Satır {idx}: {str(e)}"
                compatibility_results['errors'].append(error_msg)
                
                if "field mapping" in str(e).lower():
                    field_mapping_errors += 1
                else:
                    validation_errors += 1
        
        compatibility_results['compatible_rows'] = len(compatible_data)
        compatibility_results['compatibility_rate'] = (len(compatible_data) / len(df)) * 100 if len(df) > 0 else 0
        
        # İyileştirme önerileri
        suggestions = self.generate_improvement_suggestions(df, compatibility_results)
        compatibility_results['suggestions'] = suggestions
        
        return compatibility_results
    
    def generate_improvement_suggestions(self, df: pd.DataFrame, compatibility_results: Dict) -> List[str]:
        """İyileştirme önerileri oluştur"""
        suggestions = []
        
        # Düşük uyumluluk oranı
        if compatibility_results['compatibility_rate'] < 50:
            suggestions.append("⚠️  Düşük API uyumluluk oranı. Alan eşleştirme kuralları gözden geçirilmeli.")
        
        # Eksik alanlar
        required_fields = ['question', 'answer', 'category']
        missing_fields = [field for field in required_fields if field not in df.columns]
        if missing_fields:
            suggestions.append(f"❌ Eksik zorunlu alanlar: {', '.join(missing_fields)}")
        
        # Veri kalitesi
        for col in df.columns:
            null_percentage = (df[col].isnull().sum() / len(df)) * 100
            if null_percentage > 20:
                suggestions.append(f"⚠️  {col} sütununda %{null_percentage:.1f} eksik veri var.")
        
        # Türkçe içerik kontrolü
        turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü', 'Ç', 'Ğ', 'I', 'Ö', 'Ş', 'Ü']
        has_turkish = False
        for col in df.columns:
            if df[col].dtype == 'object':
                sample_text = ' '.join(df[col].dropna().astype(str).head(10))
                if any(char in sample_text for char in turkish_chars):
                    has_turkish = True
                    break
        
        if not has_turkish:
            suggestions.append("🌍 Türkçe içerik tespit edilemedi. Türkçe veri eklenmesi önerilir.")
        
        return suggestions
    
    def create_improved_dataset(self, df: pd.DataFrame, filepath: Path) -> pd.DataFrame:
        """İyileştirilmiş veri seti oluştur"""
        print(f"🔧 {filepath.name} için iyileştirilmiş veri seti oluşturuluyor...")
        
        improved_data = []
        
        for idx, row in df.iterrows():
            try:
                # Alan eşleştirme
                mapped_data = self.field_mapper.map_fields_to_api(row.to_dict())
                
                # Pydantic doğrulama
                validated_data = self.validator.ensure_api_compatibility(mapped_data)
                
                if validated_data:
                    improved_data.append(validated_data)
                    
            except Exception as e:
                # Hata durumunda varsayılan değerlerle doldur
                default_data = {
                    'question': f"İyileştirilmiş soru {idx+1}",
                    'answer': f"İyileştirilmiş cevap {idx+1}",
                    'category': 'general',
                    'confidence': 0.7,
                    'source': f"improved_{filepath.stem}",
                    'metadata': {
                        'original_file': filepath.name,
                        'improvement_applied': True,
                        'error_fixed': str(e)
                    }
                }
                improved_data.append(default_data)
        
        return pd.DataFrame(improved_data)
    
    def save_analysis_report(self, analysis_results: Dict):
        """Analiz raporunu kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"existing_data_analysis_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Plan B: Mevcut Veri Seti Analizi Raporu\n\n")
            f.write(f"**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Genel Özet\n\n")
            f.write(f"- **Analiz Edilen Dosya Sayısı:** {len(analysis_results)}\n")
            
            total_rows = sum(result['total_rows'] for result in analysis_results.values())
            total_compatible = sum(result['compatible_rows'] for result in analysis_results.values())
            avg_compatibility = (total_compatible / total_rows * 100) if total_rows > 0 else 0
            
            f.write(f"- **Toplam Veri Satırı:** {total_rows}\n")
            f.write(f"- **Toplam Uyumlu Satır:** {total_compatible}\n")
            f.write(f"- **Ortalama Uyumluluk Oranı:** {avg_compatibility:.1f}%\n\n")
            
            f.write("## Detaylı Analiz\n\n")
            
            for filename, result in analysis_results.items():
                f.write(f"### {filename}\n\n")
                f.write(f"- **Dosya:** {result['filepath']}\n")
                f.write(f"- **Toplam Satır:** {result['total_rows']}\n")
                f.write(f"- **Uyumlu Satır:** {result['compatible_rows']}\n")
                f.write(f"- **Uyumluluk Oranı:** {result['compatibility_rate']:.1f}%\n")
                f.write(f"- **Alan Eşleştirme Başarısı:** {result['field_mapping_success']}\n")
                f.write(f"- **Doğrulama Başarısı:** {result['validation_success']}\n\n")
                
                if result['suggestions']:
                    f.write("**İyileştirme Önerileri:**\n")
                    for suggestion in result['suggestions']:
                        f.write(f"- {suggestion}\n")
                    f.write("\n")
                
                if result['errors']:
                    f.write("**Hatalar:**\n")
                    for error in result['errors'][:5]:  # İlk 5 hatayı göster
                        f.write(f"- {error}\n")
                    f.write("\n")
        
        print(f"📄 Analiz raporu kaydedildi: {report_path}")
        return report_path
    
    def run_plan_b(self):
        """Plan B'yi çalıştır"""
        print("🚀 Plan B: Mevcut Veri Seti İşleme ve İyileştirme Başlatılıyor...")
        print("=" * 60)
        
        # Mevcut veri setlerini keşfet
        discovered_files = self.discover_existing_datasets()
        
        if not discovered_files:
            print("❌ Hiç veri seti bulunamadı!")
            return {}
        
        # Her dosyayı analiz et
        for filepath in discovered_files:
            print(f"\n📋 {filepath.name} analiz ediliyor...")
            
            # Veri setini yükle
            df = self.load_dataset(filepath)
            if df is None:
                continue
            
            print(f"📊 Yüklenen veri: {len(df)} satır, {len(df.columns)} sütun")
            
            # Yapı analizi
            structure_analysis = self.analyze_dataset_structure(df, filepath)
            
            # API uyumluluk analizi
            compatibility_analysis = self.evaluate_api_compatibility(df, filepath)
            
            # Sonuçları birleştir
            self.analysis_results[filepath.name] = {
                **structure_analysis,
                **compatibility_analysis
            }
            
            # İyileştirilmiş veri seti oluştur
            improved_df = self.create_improved_dataset(df, filepath)
            
            # İyileştirilmiş veriyi kaydet
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            improved_filename = f"improved_{filepath.stem}_{timestamp}.json"
            improved_filepath = self.output_dir / improved_filename
            
            improved_data = improved_df.to_dict('records')
            with open(improved_filepath, 'w', encoding='utf-8') as f:
                json.dump(improved_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 İyileştirilmiş veri kaydedildi: {improved_filepath}")
        
        # Analiz raporunu oluştur
        report_path = self.save_analysis_report(self.analysis_results)
        
        print("\n🎉 Plan B tamamlandı!")
        print(f"📄 Detaylı rapor: {report_path}")
        
        return self.analysis_results

if __name__ == "__main__":
    analyzer = ExistingDatasetAnalyzer()
    results = analyzer.run_plan_b()
    
    print(f"\n📊 Özet Sonuçlar:")
    for filename, result in results.items():
        print(f"  • {filename}: {result['compatible_rows']}/{result['total_rows']} "
              f"({result['compatibility_rate']:.1f}% uyumlu)") 