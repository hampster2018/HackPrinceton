from math import ceil
from tqdm import tqdm


def get_topics_textbook(textbook_path: str, extractor):
    import pke
    import spacy

    spacy.prefer_gpu()

    if extractor is None:
        extractor = pke.unsupervised.TopicRank()

    with open(textbook_path, "r", encoding="utf-8") as f:
        text = f.read()

    # break the text into a list of strings each of which hold 200,000 characters (17C = 3.4M)
    # ~100,000 characters = ~1 GB of RAM

    # current equation: total_characters^(1/5) = number_of_chunks rounded up,
    # then total_characters / number_of_chunks = chunk_size

    number_of_chunks = ceil(round(len(text) ** (1 / 5)))
    chunk_size = ceil(len(text) / number_of_chunks)
    chunk_list = []
    for i in range(0, len(text), chunk_size):
        chunk_list.append(text[i : i + chunk_size])

    # extract keyphrases from each chunk
    all_keyphrases = []
    all_relations = []
    banned_topics = [
        "chapter",
        "chapters",
        "section",
        "sections",
        "problem",
        "problems",
        "solution",
        "solutions",
        "example",
        "examples",
        "exercises",
        "exercise",
        "summary",
        "page",
        "pages",
        "page number",
        "figure",
        "figures",
        "employee",
        "employees",
    ]
    for chunk_index, chunk in tqdm(enumerate(chunk_list)):
        extractor.load_document(input=chunk, language="en")
        extractor.candidate_selection(pos={"NOUN"})  # PNOUN and ADJ are too slow :(
        extractor.candidate_weighting(threshold=0.74, method="average")
        keyphrases = extractor.get_n_best(n=20)
        chunk_keys = 0
        for keyphrase in keyphrases:
            keys = {}
            for key in all_keyphrases:
                # add variations of the keyphrase to the overlapping keys
                keys[key[0]] = key[0]
                keys[key[0] + "s"] = key[0]
                keys[key[0] + "es"] = key[0]
                keys[key[0] + "ies"] = key[0]
                keys[key[0][0:-1]] = key[0]
            if keyphrase[0] not in keys.keys() and keyphrase[0] not in banned_topics:
                all_keyphrases.append((keyphrase[0], keyphrase[1], chunk_index))
                chunk_keys += 1
                # aim for 10 keyphrases per chunk, and get 20 just in case
                if chunk_keys > 10:
                    break
            elif keyphrase[0] in keys.keys():
                # generate a relation between the two chunks
                # back reference means foundational concepts are shared
                all_keyphrase_index = -1
                for i, key in enumerate(all_keyphrases):
                    if key[0] == keys[keyphrase[0]]:
                        all_keyphrase_index = i

                print(
                    "found relation between",
                    chunk_index,
                    "and",
                    all_keyphrases[all_keyphrase_index][2],
                )
                all_relations.append(
                    (
                        all_keyphrases[all_keyphrase_index][2],
                        chunk_index,
                    )
                )

    return {"keyphrases": all_keyphrases, "relations": all_relations}
