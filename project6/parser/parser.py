import nltk
import sys
from nltk import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S P S | S Conj VP
NP -> N | Det NP | AdjP NP | N PP
VP -> V | VP NP | VP AdvP | VP NP PP | VP PP | AdvP VP | VP PP AdvP
AdjP -> Adj | Adj AdjP
AdvP -> Adv
PP -> P NP | P
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    list = nltk.word_tokenize(sentence)
    for word in list:
        if not any(char.isalpha() for char in word):
            list.remove(word)

    return list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    list =[]
    for s in tree.subtrees():
        if s.label() == "NP":
            list.append(s)
            #print(f"{s}")

    # according to our implementation it will only leave nouns, as they are considered Noun Phrases and they will be present in any Noun Phrase
    # can be solved by removing N from possible Noun Phrases and adding new NONTERMINALs replacing NP for N in addition to the former ones.
    for chunk in list.copy():
        for otherchunk in list.copy():
            if chunk in otherchunk:
                list.remove(otherchunk)


    return list


if __name__ == "__main__":
    main()
