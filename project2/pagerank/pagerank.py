import os
import random
import re
import sys
from numpy.random import choice

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    sum = 0
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    pagesrank = dict.fromkeys(corpus)
    # N = number of all pages in given corpus
    n = len(pagesrank)
    # L = links for given page

    l = len(corpus[page])

    # CAMBIAR MENSAJE DE ALERTA EN EL FUTURO
    if n == 0:
        raise NotImplementedError

    for item in pagesrank:
        if l == 0:
            pagesrank[item] = 1 / n
        elif item in corpus[page]:
            pagesrank[item] = (1 - damping_factor) / n + damping_factor / l
        else:
            pagesrank[item] = (1 - damping_factor) / n

    return pagesrank

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagesrank = dict.fromkeys(corpus)

    # Counting our samples
    samples = []
    samples.append(random.choice(list(dict.fromkeys(pagesrank))))
    i = 1

    # we loop into future samples
    while i < n:

        currentpagelinks = transition_model(corpus, samples[i - 1], damping_factor)
        nextpage = choice(list(dict.fromkeys(currentpagelinks)), 1, p = list(currentpagelinks.values())).item(0)
        samples.append(nextpage)
        i = i + 1

    for page in pagesrank:
        p = samples.count(page)
        pagesrank[page] = p / n

    return pagesrank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagesrank = dict.fromkeys(corpus)
    pagesrank2 = dict.fromkeys(corpus)
    tolerances = dict.fromkeys(corpus)


    # N = number of all pages in given corpus
    n = len(pagesrank)

    # Check for pages with 0 links
    for page in pagesrank:
        if len(corpus[page]) == 0:
            for otherpages in pagesrank:
                corpus[page].add(otherpages)

    # We set the original pagesrank (equally random)
    for page in pagesrank:
        pagesrank[page] = 1 / n
    # We iterate
    while True:
        for page in pagesrank:
            sum = 0
            for otherpages in corpus:
                if page in corpus[otherpages]:
                    sum = sum + pagesrank[otherpages] / (len(corpus[otherpages]))


            #We set the tolerances dict to know when we have to stop the loop, and store our new pagerank in a diferent dict
            tolerances[page] = abs(pagesrank[page] - ((1 - damping_factor) / n + damping_factor * sum))
            pagesrank2[page] = (1 - damping_factor) / n + damping_factor * sum

        # We copy our "temporal pagerank" to our final pagerank
        for page in pagesrank2:
            pagesrank[page] = pagesrank2[page]

        # We check if our tolerances are met
        check=0
        for control in tolerances:
            if tolerances[control] > 0.001:
                check = check + 1
        if check == 0:
            break

    return pagesrank



if __name__ == "__main__":
    main()
