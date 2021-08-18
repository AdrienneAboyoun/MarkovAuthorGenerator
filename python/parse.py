import os, string

def process_file(file):
    f = open(file)
    lines = f.readlines()
    start, x, end = 0, 0, 0
    while x < len(lines):
        if "*** START" in lines[x] or '***START' in lines[x]:
            start = x + 1
        elif "*** END" in lines[x] or "***END" in lines[x]:
            end = x - 2
            break
        x += 1
    return lines[start:end]


def to_words(book, punctuation):
    new_words = []
    for line in book:
        if (punctuation):
            new_words.extend(line.split())
        else:
            for word in line.split():
                new_words.append(word.strip(string.punctuation))
    return new_words


def process_folder(directory, punctuation):
    files = []
    bad_files = []
    if (os.path.basename(os.getcwd()) != 'data'):
        os.chdir(os.path.join(os.path.abspath(os.getcwd()), 'data/' + directory))
    else:
        os.chdir(os.path.join(os.path.abspath(os.getcwd()), directory))
    for file in os.listdir():
        f = open(file)
        lines = f.readlines()
        for line in lines:
            if '*******************************************************************' in line:
                bad_files.append(file)
                break
    for file in os.listdir():
        if file not in bad_files:
            files.append(to_words(process_file(file), punctuation))
    return files


