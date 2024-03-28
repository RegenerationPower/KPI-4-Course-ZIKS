import sys
import re
import string
import math
from collections import Counter
from functools import reduce, wraps

NON_ALPHABET = re.compile('[^a-zA-Z]+')
ALPHABET = string.ascii_lowercase
FREQUENCY_ALPHABET = "etaoinshrdlcumwfgypbvkjxqz"
MODULE = len(ALPHABET)
MAX_SCORE = (MODULE - 1)*MODULE
ENGLISH_IC = 0.067
MIN_ENGLISH_IC = 1/MODULE
FAILED = (None, None)


def memoize(f):
    class MemoDictionary(dict):

        def __init__(self, funk):
            super().__init__()
            self.f = funk

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return MemoDictionary(f)


def read(text=None, binary=False):
    if not text:
        text = sys.stdin.buffer.read() if binary else sys.stdin.read()
        if text[-1] == '\n':
            text = text[:-1]
        return text
    return str.encode(text) if binary else text


def read_file(file_name, binary=False):
    mode = 'rb' if binary else 'r'
    return open(file_name, mode).read()


def read_from_file(file_path, binary=False):
    try:
        with open(file_path, 'rb' if binary else 'r') as file:
            return file.read()
    except FileNotFoundError:
        error(f"File not found: {file_path}")


def clean(text):
    return NON_ALPHABET.sub('', text.lower())


def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(0)


def flatmap(f, items):
    return [x for mappedList in map(f, items) for x in mappedList]


def flatten(list_of_lists):
    return flatmap(lambda input_list: input_list, list_of_lists)


def repetitions(input_list):
    result = Counter(input_list).most_common(len(input_list))

    def comparator(x):
        return -x[1], x[0]
    result.sort(key=comparator)
    return result


def most_frequent_chars(text, size=MODULE):
    return Counter(text).most_common(size)


def most_frequent_char(text):
    return most_frequent_chars(text, size=1)[0][0]


@memoize
def divisors(n, max_value=None):
    limit = math.ceil(math.sqrt(n))
    if max_value is not None:
        limit = min(limit, max_value)
    yield 1
    for i in range(2, limit + 1):
        if n % i == 0:
            yield i
            if i != n:
                op = n//i
                if op != i:
                    yield op
    if max_value is None or n <= max_value:
        yield n


@memoize
def shift_by(char, shift):
    if char.isalpha():
        aux = ord(char) + shift
        z = 'z' if char.islower() else 'Z'
        if aux > ord(z):
            aux -= MODULE
        char = chr(aux)
    return char


def reversed_shifts(text, verbose=False):
    most_frequent = ord(most_frequent_char(text))
    if verbose:
        print(f"Most frequent character: {chr(most_frequent)}")
    shifts = []
    for i in range(MODULE):
        possible_original = ord(FREQUENCY_ALPHABET[i])
        shift = possible_original - most_frequent
        if shift < 0:
            shift += MODULE
        shifts.append(shift)
    return shifts


def coincidence_index(text, frequencies=None):
    if frequencies is None:
        frequencies = most_frequent_chars(text)
    size = len(text)
    freq_sum = reduce(lambda x, y: x + y, map(lambda freq: freq[1]*(freq[1] - 1), frequencies))
    size_mult = size * (size - 1)
    return freq_sum / size_mult


def distance(char, target_index, alphabet):
    try:
        return abs(alphabet.index(char) - target_index)
    except ValueError:
        return MODULE - 1


def match_score(frequencies):
    score = 0
    for i, char in enumerate(frequencies):
        score += MODULE - 1 - distance(char, i, FREQUENCY_ALPHABET)
    return score


def find_sequence_duplicates(text, min_length=3):
    size_alpha = len(text) + 1
    seq_spacings = {}

    lengths = [[0] * i for i in range(size_alpha)]

    for i in range(1, size_alpha):
        if args.verbose:
            sys.stdout.write("\r")
            sys.stdout.write(f"{round(100 * (i/(size_alpha - 1)))}% ")
            sys.stdout.flush()
        for j in range(1, i):
            if text[i - 1] == text[j - 1]:
                duplicate_length = lengths[i][j] = lengths[i - 1][j - 1] + 1
                spacing = i - j
                if duplicate_length >= min_length and (i >= (size_alpha - 1) or text[i] != text[j]):
                    duplication = text[i - duplicate_length:i]
                    if duplication not in seq_spacings:
                        seq_spacings[duplication] = []
                    seq_spacings[duplication].append(spacing)
    if args.verbose:
        print()
    return seq_spacings
