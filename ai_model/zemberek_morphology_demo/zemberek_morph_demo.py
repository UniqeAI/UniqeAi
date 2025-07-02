from zemberek.morphology import TurkishMorphology

morphology = TurkishMorphology.create_with_defaults()

sentence = "İnternetimin hızını yükseltmek istiyorum."

analyses = morphology.analyze_sentence(sentence)

for analysis in analyses:
    surface_form = analysis.inp 
    first_analysis = analysis.analysis_results[0]  
    
    lemma = first_analysis.item.root  
        
    morpheme_data_list = first_analysis.morpheme_data_list
    morphemes = [md.surface for md in morpheme_data_list if md.surface != '']

    print(f"{surface_form} → kök: {lemma}, ekler: {morphemes}")
