def word_freq(words):
    freq = dict()
    for word in words:
        if word not in freq:
            freq[word] = 1
        else:
            freq[word] += 1
    return freq


def word_count(dict):
    return sum(dict.values())


def unique_count(dict):
    return len(dict)


def most_common(hist):
    t = []
    for key, value in hist.items():
        t.append((value, key))
    t.sort(reverse=True)
    return t


def select_random(hist):
    keys = sorted(hist.keys())
    sums = []
    x = 0
    i = 0
    while i < len(keys):
        x += hist.get(keys[i])
        sums.append(x)
        i += 1
    index = bin_search(random.randint(0, sums[-1]), sums)
    return keys[index]


def bin_search(val, list):
    l = 0
    r = len(list) - 1
    m = 0
    while l <= r:
        m = (l + r) // 2
        if list[m] < val:
            l = m + 1
        elif list[m] > val:
            r = m - 1
        else:
            break
    return m
