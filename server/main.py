import io
import json
import sys
import json
import nltk
import numpy
import requests
from newspaper import Article

#fix the encoding to print text to the Windows command line
def fix_encoding(txt):
    return txt.encode('utf-8', 'ignore')

# Adapted from "The Automatic Creation of Literature Abstracts" by H.P. Luhn
# Parameters:
# * n  - Number of words to consider
# * cluster_threshold - Distance between words to consider
# * top_sentences - Number of sentences to return for a "top n" summary
def summarize(url=None, n=250, cluster_threshold=10, top_sentences=10):

    def get_stop_words():
        words = nltk.corpus.stopwords.words('english')
        words.extend([";", "/", "\\", "`", "|", "*", "<", ">", "(", ")", "{", "}", "[", "]", "#"])
        return words

    stopWords = get_stop_words()
            
    # Begin - nested helper function
    def score_sentences(sentences, important_words):
        scores = []
        sentence_idx = -1

        for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
    
            sentence_idx += 1
            word_idx = []
    
            # For each word in the word list...
            for w in important_words:
                try:
                    # Compute an index for important words in each sentence
    
                    word_idx.append(s.index(w))
                except ValueError, e: # w not in this particular sentence
                    pass
    
            word_idx.sort()
    
            # It is possible that some sentences may not contain any important words
            if len(word_idx)== 0: continue
    
            # Using the word index, compute clusters with a max distance threshold
            # for any two consecutive words
    
            clusters = []
            cluster = [word_idx[0]]
            i = 1
            while i < len(word_idx):
                if word_idx[i] - word_idx[i - 1] < cluster_threshold:
                    cluster.append(word_idx[i])
                else:
                    clusters.append(cluster[:])
                    cluster = [word_idx[i]]
                i += 1
            clusters.append(cluster)
    
            # Score each cluster. The max score for any given cluster is the score 
            # for the sentence.
    
            max_cluster_score = 0
            for c in clusters:
                significant_words_in_cluster = len(c)
                total_words_in_cluster = c[-1] - c[0] + 1
                score = 1.0 * significant_words_in_cluster \
                    * significant_words_in_cluster / total_words_in_cluster
    
                if score > max_cluster_score:
                    max_cluster_score = score
    
            scores.append((sentence_idx, score))
    
        return scores    
    
    # End - nested helper function
    
    article = Article(url)
    article.download()
    article.parse()

    # It's entirely possible that this "clean page" will be a big mess. YMMV.
    # The good news is that the summarize algorithm inherently accounts for handling
    # a lot of this noise.

    txt = article.text
    title = article.title
    
    # TODO: instead of converting all html to plain text, remember all content wrapped in <p> tags and their indices, 
    # convert all of the paragraphs into plain texts to tokenize them
    # map index of sentences back to their paragraph index, so that we get a list of paragraphs containing the best sentences
    
    sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
    normalized_sentences = [s.lower() for s in sentences]

    words = [w.lower() for sentence in normalized_sentences for w in
             nltk.tokenize.word_tokenize(sentence)]

    fdist = nltk.FreqDist(words)

    top_n_words = [w[0] for w in fdist.items() 
            if w[0] not in stopWords][:n]

    scored_sentences = score_sentences(normalized_sentences, top_n_words)

    # Summarization Approach 1:
    # Filter out nonsignificant sentences by using the average score plus a
    # fraction of the std dev as a filter

    avg = numpy.mean([s[1] for s in scored_sentences])
    std = numpy.std([s[1] for s in scored_sentences])
    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences
                   if score > avg + 0.5 * std]

    # Summarization Approach 2:
    # Another approach would be to return only the top N ranked sentences

    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-top_sentences:]
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

    top_n_summary = [fix_encoding(sentences[idx]) for (idx, score) in top_n_scored]
    mean_scored_summary = [fix_encoding(sentences[idx]) for (idx, score) in mean_scored]
    summaries = list(set(top_n_summary).union(set(mean_scored_summary)))

    return dict(url=url, title=title, summary=summaries)

def get_summaries(source_filename):
    summaries = list()
    urls = io.open(source_filename, 'r+')
    for url in urls:
        summary = summarize(url=url.strip())
        summaries.append(summary)
    urls.close()
    return summaries

summaries = get_summaries(sys.argv[1])
with io.open(sys.argv[2], 'w', encoding='utf-8') as output:
    output.write(unicode(json.dumps(summaries)))


