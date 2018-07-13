from src.utils.NLP_classics import *
from src.utils.freeling_module import *
from collections import Counter


N_grams = [1,2,3,4]

if __name__ == '__main__':
    list_of_tags = []

    # Llenar una lista de objetos tag (src.utils.freeling_module)
    #        Token       lemma      tag
    # Importante: Conservar los puntos como: tag(".", ".", "Fp")

    t = tag("Veronica", "veronica", "N")
    list_of_tags.append(t)
    t = tag("Tiene", "tener", "V")
    list_of_tags.append(t)
    t = tag("un", "un", "D")
    list_of_tags.append(t)
    t = tag("Perro", "perro", "N")
    list_of_tags.append(t)
    t = tag(",", ",", "Fc")
    list_of_tags.append(t)
    t = tag("un", "un", "D")
    list_of_tags.append(t)
    t = tag("gato", "gato", "N")
    list_of_tags.append(t)
    t = tag("y", "y", "CC")
    list_of_tags.append(t)
    t = tag("un", "un", "D")
    list_of_tags.append(t)
    t = tag("ratón", "ratón", "N")
    t = tag("y", "y", "CC")
    list_of_tags.append(t)
    t = tag("un", "un", "D")
    list_of_tags.append(t)
    t = tag("animal", "animal", "N")
    list_of_tags.append(t)
    t = tag(".", ".", "Fp")
    list_of_tags.append(t)
    t = tag("Laura", "laura", "N")
    list_of_tags.append(t)
    t = tag("Tiene", "tener", "V")
    list_of_tags.append(t)
    t = tag("un", "un", "D")
    list_of_tags.append(t)
    t = tag("Conejo", "conejo", "N")
    list_of_tags.append(t)
    t = tag(".", ".", "Fp")
    list_of_tags.append(t)

    # Lista de etiquetas que quiere conservar (Fp es de punto)
    # Junta dos verbos consecutivos y los vuelve uno ("was going"-> "was_going")
    reduced_POS = ["N", "V", "Fp"]
    list_of_reduced_tags = []
    previous_t = tag(original="", lemma="", tag="", certainty=-1)
    for tag_object in list_of_tags:
        current_t = tag_object
        t = tag_object.tag
        p_t = previous_t.tag

        if not t == "T":
            # Tag "to" in English is omitted by default
            if (t == "V") and p_t == t:
                # join two consecutive verbs or nouns:
                current_t = tag(original=previous_t.original + "_" + current_t.original,
                                lemma=previous_t.lemma + "_" + current_t.lemma,
                                tag=t,
                                certainty=(previous_t.certainty + current_t.certainty) / 2)

            else:
                if (p_t == "V" ):
                    if p_t in reduced_POS:
                        list_of_reduced_tags.append(previous_t)

                if t in reduced_POS and not (t == "V"):
                    list_of_reduced_tags.append(current_t)

            previous_t = current_t

    for t in list_of_reduced_tags:
        print(t.lemma)


    unigrams = retrieve_n_grams(1,list_of_reduced_tags, remove_punctuation=True, lemmas=True)
    bigrams = retrieve_n_grams(2, list_of_reduced_tags, remove_punctuation=True, lemmas=True)
    trigrams = retrieve_n_grams(3, list_of_reduced_tags, remove_punctuation=True, lemmas=True)
    trigrams = retrieve_n_grams(4, list_of_reduced_tags, remove_punctuation=True, lemmas=True)

    print(unigrams)
    print(bigrams)
    print(trigrams)

    # Conviertes a un diccionario Counter
    c = Counter(bigrams)
    print(c)

