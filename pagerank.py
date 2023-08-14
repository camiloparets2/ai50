import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
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
    model = dict()
    
    # If the page has no links, return an equal probability for each page
    if not corpus[page]:
        for p in corpus:
            model[p] = 1 / len(corpus)
        return model
    
    # Probability of choosing a link at random from the current page
    for p in corpus:
        model[p] = (1 - damping_factor) / len(corpus)
    for link in corpus[page]:
        model[link] += damping_factor / len(corpus[page])
        
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = []
    # Starting with a random page
    page = random.choice(list(corpus.keys()))
    samples.append(page)
    
    for _ in range(n - 1):
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), weights=list(model.values()), k=1)[0]
        samples.append(page)
    
    ranks = dict()
    for page in corpus:
        ranks[page] = samples.count(page) / n
    
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    ranks = {page: 1/n for page in corpus}
    threshold = 0.001
    stable = False
    
    while not stable:
        new_ranks = dict()
        for page in corpus:
            sum_links = sum(ranks[i] / len(corpus[i]) for i in corpus if page in corpus[i])
            new_ranks[page] = (1 - damping_factor) / n + damping_factor * sum_links
        stable = all(abs(new_ranks[page] - ranks[page]) < threshold for page in corpus)
        ranks = new_ranks
        
    return ranks


if __name__ == "__main__":
    main()
