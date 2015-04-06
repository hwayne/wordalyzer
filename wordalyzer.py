import string
from collections import defaultdict
from random import choice

def processed_list(words):
    return (word.lower() for word in trim_punctuation(words).split())

def trim_punctuation(s):
    return s.translate({ord(a): None for a in string.punctuation})

def add_to_word_counter(words, word_list):
    for word in processed_list(words):
        word_list[word] = (word_list.get(word, 0) + 1)
    return word_list

def make_readable(word_list):
    return sorted(word_list.items(), key = lambda x: x[1], reverse=True)

def markov_chain(word_blob, prefix_number=2):
    chain = defaultdict(list)
    prefixes = [""] * prefix_number
    for word in word_blob.split():
        chain[tuple(prefixes)].append(word)
        prefixes = prefixes[1:]
        prefixes.append(word)
    return chain

def chain_to_text(chain, size=10):
    output = []
    prefixes = [""] * len(next(iter(chain.keys())))
    for i in range(size):
        output.append(choice(chain.get(tuple(prefixes), [""])))
        prefixes = prefixes[1:] + [output[-1]]
    return output

if __name__ == '__main__':
    #for i in make_readable((add_to_word_counter(test, {}))):
    #    print(i)
    text_to_read = open("Path/goes/here")
    blob = " ".join(text_to_read.readlines())
    print(" ".join(chain_to_text(markov_chain(blob, 2), 720)))
