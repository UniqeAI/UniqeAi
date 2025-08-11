import json
from difflib import SequenceMatcher

def is_similar(a, b, threshold=0.9):
    return SequenceMatcher(None, a, b).ratio() >= threshold

with open("/Users/erkan/Documents/GitHub/Projects/UniqeAi/ai_model/data/ultimate_human_level_dataset_v2_enhanced_20250803_181419.json", "r") as f:
    data = json.load(f)

unique_data = []
icerik_list = []

for entry in data:
    donguler = entry.get("donguler", [])
    if not donguler:
        continue

    first_icerik = donguler[0].get("icerik", "").strip()
    if not first_icerik:
        continue

    is_duplicate = False
    for seen_icerik in icerik_list:
        if is_similar(first_icerik, seen_icerik):
            is_duplicate = True
            break

    if not is_duplicate:
        icerik_list.append(first_icerik)
        unique_data.append(entry)

print(f"Orijinal kayıt sayısı: {len(data)}")
print(f"%90 benzerliğe göre tekil kayıt sayısı: {len(unique_data)}")

with open("temizlenmis_veri_seti_benzerlikli.json", "w", encoding="utf-8") as f:
    json.dump(unique_data, f, ensure_ascii=False, indent=2)
