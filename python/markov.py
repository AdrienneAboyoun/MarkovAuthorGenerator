import string
import random
import parse
import os


def markov(text, length):
    mark = dict()
    i = 0
    while i < len(text) - length:
        prefix = ' '.join(text[i:i + length])
        if prefix not in mark:
            mark[prefix] = [text[i + length]]
        else:
            mark[prefix].append(text[i + length])
        i += 1
    return mark


def chain(mark, length, prefix):
    sentence = []
    i = 0
    start = random.choice(list(mark.keys()))
    sentence.extend(start.split())
    while i < length:
        next = random.choice(mark[start])
        sentence.append(next)
        start = ' '.join(sentence[-prefix:])
        i += 1
    return(' '.join(sentence))

def author_freq(directory, length, punctuation):
    frequencies = dict()
    files = parse.process_folder(directory, punctuation)
    for file in files:
        temp = markov(file, length)
        for t in temp.keys():
            if t not in frequencies:
                frequencies[t] = temp.get(t)
            else:
                frequencies[t].extend(temp.get(t))
    os.chdir("..")
    return frequencies

def merge_authors(authors):
    frequencies = dict()
    for author in authors:
        for a in author.keys():
            if a not in frequencies:
                frequencies[a] = author.get(a)
            else:
                frequencies[a].extend(author.get(a))
    return frequencies
