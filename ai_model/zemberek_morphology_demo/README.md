# Zemberek Morfolojik Çözümleme Demo

Bu proje, [Zemberek NLP](https://github.com/ahmetaa/zemberek-nlp) Python arayüzünü kullanarak Türkçe cümleleri morfolojik olarak çözümlemektedir.

## Gereksinimler

- Python 3.8+
- `zemberek-python` kütüphanesi (aşağıda nasıl kurulur anlatılmıştır)

## Kurulum

```bash
pip install zemberek-python

## KULLANIM
```bash
python zemberek_morphology_demo.py

## ÖRNEK ÇIKTI

İnternetimin → kök: internet, ekler: ['internet', 'im', 'in']
hızını → kök: hız, ekler: ['hız', 'ın', 'ı']
yükseltmek → kök: yüksel, ekler: ['yüksel', 't', 'mek']
istiyorum → kök: iste, ekler: ['iyor', 'um']
. → kök: ., ekler: ['.']
