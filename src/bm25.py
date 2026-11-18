import json
import bm25s
import Stemmer

with open("./data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

stemmer = Stemmer.Stemmer("english")

corpus_tokens = bm25s.tokenize(
    [chunk["text"] for chunk in chunks],
    stopwords="en",
    stemmer=stemmer
)

retriever = bm25s.BM25(corpus=chunks)
retriever.index(corpus_tokens)

def search(query, k=2):
    query_tokens = bm25s.tokenize(
        query,
        stopwords="en",
        stemmer=stemmer
    )

    results, scores = retriever.retrieve(
        query_tokens,
        k=min(k, len(chunks))
    )

    for i in range(results.shape[1]):
        doc = results[0, i]
        score = scores[0, i]

        print(f"Rank {i+1} (score: {score:.2f}):")
        print(doc["text"])
        print()

results = search("revenue growth")


# import json
# import re   
# from collections import Counter
# import math

# #term freq
# #raraty 
# #doc length

# with open("./data/chunks.json", "r", encoding="utf-8") as f:
#     chunks = json.load(f)

# def tokenizer(text):
#     text = text.lower()
#     tokens = re.findall(r"\b\w+\b", text)
#     return tokens

# tokenized_chunks = []

# for chunk in chunks:
#     tokens = tokenizer(chunk["text"])
#     tokenized_chunks.append(tokens)

# #['the', 'business', 'financial', 'condition']

# #term freq
# term_frequencies = []

# for token in tokenized_chunks:
#     term_frequencies.append(Counter(token)) 

# #doc freq rarer word
# document_frequencies = Counter()

# for tokens in tokenized_chunks:
#     unique_tokens = set(tokens)

#     for word in unique_tokens:
#         document_frequencies[word] += 1

# N = len(tokenized_chunks)
# idf = {}

# for word, df in document_frequencies.items():
#     idf[word] = math.log(1+ (N-df + 0.5) / (df + 0.5))

# #doc length
# document_lengths = []

# for tokens in tokenized_chunks:
#     document_lengths.append(len(tokens))

# total_length = sum(document_lengths)

# avgdl = total_length / N

# # IDF	How rare the word is
# # TF	How often the word appears in the chunk
# # k1	Controls how much repeated words help
# # b	Controls document-length normalization
# # D	The chunk we're scoring
# # avgdl	Average chunk length

# def bm25_score(word, doc_index):
#     k1 = 1.5
#     b = 0.75

#     doc_length = document_lengths[doc_index]
#     length_norm = 1 - b + b * (doc_length / avgdl)

#     tf = term_frequencies[doc_index][word]

#     if tf == 0:
#         return 0.0

#     word_idf = idf.get(word, 0)

#     #term frequency adjustment
#     numerator = tf * (k1 + 1)
#     #adjusts for term frequency and chunk length
#     denominator = tf + k1 * length_norm

#     score = word_idf * (numerator / denominator)

#     return score

# def score_query(query, doc_index):
#     query_tokens = tokenizer(query)
#     total_score = 0

#     for word in query_tokens:
#         total_score += bm25_score(word, doc_index)

#     return total_score  


# def search(query):
#     scores = []

#     for doc_index in range(len(chunks)):
#         score = score_query(query, doc_index)
#         scores.append((doc_index, score))

#     return scores

# results = search("revenue growth")
