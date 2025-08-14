#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Güvenli Eğitim Durdurma ve GPU Temizleme Script'i
RTX 4060 için ekran gitme sorununu önler
"""

import os
import sys
import time
import signal
import psutil
import subprocess
import torch
from pathlib import Path

class SafeTrainingStop:
    def __init__(self):
        self.cleanup_done = False
        
    def emergency_gpu_cleanup(self):
        """Acil GPU temizleme"""
        print("🚨 ACİL GPU TEMİZLEME BAŞLATILIYOR...")
        
        try:
            # CUDA temizleme
            if torch.cuda.is_available():
                print("🧹 CUDA cache temizleniyor...")
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
                
                # Tüm CUDA context'leri temizle
                for i in range(torch.cuda.device_count()):
                    with torch.cuda.device(i):
                        torch.cuda.empty_cache()
                        torch.cuda.ipc_collect()
                
                print("✅ CUDA temizlik tamamlandı")
            
            # GPU frekanslarını sıfırla
            print("🔄 GPU frekansları sıfırlanıyor...")
            try:
                subprocess.run(['nvidia-smi', '-rgc'], timeout=10, capture_output=True)
                subprocess.run(['nvidia-smi', '-rmc'], timeout=10, capture_output=True)
                print("✅ GPU frekansları sıfırlandı")
            except:
                print("⚠️ GPU frekans sıfırlama başarısız")
            
            # GPU persistence mode kapat
            print("🔌 GPU persistence mode kapatılıyor...")
            try:
                subprocess.run(['nvidia-smi', '-pm', '0'], timeout=10, capture_output=True)
                print("✅ Persistence mode kapatıldı")
            except:
                print("⚠️ Persistence mode kapatılamadı")
                
        except Exception as e:
            print(f"❌ GPU temizleme hatası: {e}")
    
    def find_training_processes(self):
        """Eğitim process'lerini bul"""
        training_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Python process'leri ara
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    # Eğitim script'lerini tespit et
                    if any(keyword in cmdline.lower() for keyword in [
                        'expert_trainer', 'trainer', 'finetune', 'train',
                        'llama', 'model', 'torch', 'transformers'
                    ]):
                        training_processes.append(proc)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return training_processes
    
    def safe_kill_process(self, proc, timeout=30):
        """Process'i güvenle öldür"""
        try:
            print(f"🔄 Process {proc.pid} ({proc.info['name']}) durduruluyor...")
            
            # Önce SIGTERM gönder
            proc.terminate()
            
            # Bekleme
            try:
                proc.wait(timeout=timeout)
                print(f"✅ Process {proc.pid} güvenle durduruldu")
                return True
            except psutil.TimeoutExpired:
                print(f"⏰ Process {proc.pid} timeout, zorla kapatılıyor...")
                proc.kill()
                proc.wait(timeout=5)
                print(f"🔪 Process {proc.pid} zorla kapatıldı")
                return True
                
        except Exception as e:
            print(f"❌ Process {proc.pid} durdurulamadı: {e}")
            return False
    
    def emergency_stop_training(self):
        """Acil eğitim durdurma"""
        print("🛑 ACİL EĞİTİM DURDURMA BAŞLATILIYOR...")
        print("=" * 50)
        
        # 1. GPU temizleme (önce)
        self.emergency_gpu_cleanup()
        
        # 2. Training process'leri bul ve durdur
        print("\n🔍 Eğitim process'leri aranıyor...")
        training_procs = self.find_training_processes()
        
        if not training_procs:
            print("ℹ️ Aktif eğitim process'i bulunamadı")
        else:
            print(f"🎯 {len(training_procs)} eğitim process'i bulundu")
            for proc in training_procs:
                self.safe_kill_process(proc)
        
        # 3. GPU durumunu kontrol et
        print("\n📊 GPU durumu kontrol ediliyor...")
        try:
            result = subprocess.run([
                'nvidia-smi', '--query-gpu=temperature.gpu,power.draw,memory.used',
                '--format=csv,noheader,nounits'
            ], capture_output=True, text=True, timeout=10)
            
            temp, power, memory = result.stdout.strip().split(', ')
            print(f"🌡️ Sıcaklık: {temp}°C")
            print(f"⚡ Güç: {power}W")
            print(f"🧠 VRAM: {memory}MB")
            
            if float(power) < 30:
                print("✅ GPU idle duruma geçti")
            else:
                print("⚠️ GPU hala aktif")
                
        except Exception as e:
            print(f"⚠️ GPU durumu kontrol edilemedi: {e}")
        
        # 4. Son temizlik
        print("\n🧹 Son temizlik...")
        self.emergency_gpu_cleanup()
        
        print("\n✅ ACİL DURDURMA TAMAMLANDI!")
        print("Ekran gitmemesi için 10 saniye bekleniyor...")
        time.sleep(10)
        
        return True
    
    def monitor_and_safe_stop(self, max_hours=12):
        """Eğitimi izle ve güvenle durdur"""
        print(f"⏰ Eğitim {max_hours} saat sonra otomatik durdurulacak")
        
        start_time = time.time()
        max_seconds = max_hours * 3600
        
        while True:
            elapsed = time.time() - start_time
            remaining = max_seconds - elapsed
            
            if remaining <= 0:
                print(f"\n⏰ {max_hours} saat doldu, eğitim durduruluyor...")
                self.emergency_stop_training()
                break
            
            # Her 30 dakikada durum raporu
            if int(elapsed) % 1800 == 0:
                hours = elapsed / 3600
                print(f"📊 Geçen süre: {hours:.1f} saat")
            
            time.sleep(60)  # 1 dakikada bir kontrol

def main():
    """Ana fonksiyon"""
    print("🛑 Güvenli Eğitim Durdurma Aracı")
    print("=" * 40)
    
    stopper = SafeTrainingStop()
    
    print("Seçenekler:")
    print("1. Şimdi güvenle durdur")
    print("2. X saat sonra otomatik durdur")
    print("3. Sadece GPU temizle")
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == "1":
        stopper.emergency_stop_training()
        
    elif choice == "2":
        try:
            hours = float(input("Kaç saat sonra durdurulsun? "))
            stopper.monitor_and_safe_stop(hours)
        except ValueError:
            print("❌ Geçersiz saat değeri")
            
    elif choice == "3":
        stopper.emergency_gpu_cleanup()
        
    else:
        print("❌ Geçersiz seçenek")

if __name__ == "__main__":
    main() 