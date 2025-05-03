import os
import random
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.data import find
from nltk import pos_tag, word_tokenize

# Define NLTK data path
nltk_data_path = "C:/Users/PcHelps/AppData/Roaming/nltk_data"
nltk.data.path.append(nltk_data_path)

# Map of required resources and their type (corpora or tokenizers)
resources = {
    "punkt": "tokenizers",
    "punkt_tab": "tokenizers",
    "wordnet": "corpora",
    "omw-1.4": "corpora",
    "averaged_perceptron_tagger": "taggers",
}

# Silent downloader using subprocess
import subprocess
import sys


def safe_download(package, resource_type):
    try:
        find(f"{resource_type}/{package}")
    except LookupError:
        subprocess.run(
            [sys.executable, "-m", "nltk.downloader", "-d", nltk_data_path, package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


# Download only missing resources
for pkg, typ in resources.items():
    safe_download(pkg, typ)

nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")


# Paraphrasing logic
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.name().lower() != word.lower():
                synonyms.add(lemma.name().replace("_", " "))
    return list(synonyms)


def basic_paraphrase(text, replacement_prob=0.5):
    words = word_tokenize(text)
    tagged_words = pos_tag(words)
    paraphrased = []

    for word, tag in tagged_words:
        if word.isalpha() and random.random() < replacement_prob:
            # Replace only nouns, verbs, adjectives, or adverbs
            if (
                tag.startswith("NN")
                or tag.startswith("VB")
                or tag.startswith("JJ")
                or tag.startswith("RB")
            ):
                syns = get_synonyms(word)
                new_word = random.choice(syns) if syns else word
                paraphrased.append(new_word)
            else:
                paraphrased.append(word)
        else:
            paraphrased.append(word)

    return " ".join(paraphrased)


# Example usage
input_text = input("Enter a sentence to paraphrase: ")
paraphrased_text = basic_paraphrase(input_text)
print("Original:", input_text)
print("Paraphrased:", paraphrased_text)
