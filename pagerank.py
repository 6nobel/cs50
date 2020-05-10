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
    #print(corpus)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print("sum", sum(ranks.values()))
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print("sum", sum(ranks.values()))

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
    
    link_list = dict()
    link_count = 0
    for key in corpus:
        if key == page:
            for value in corpus[key]:
                link_count += 1
                link_list[value] = 0

    distribution = dict()
    page_count = 0
    for key in corpus:
        distribution[key] = 0
        page_count += 1

    if link_count == 0:
        base_chance = ((damping_factor) / page_count)
    else:
        base_chance = ((1-damping_factor) / page_count)

    for key in distribution:
        distribution[key] += base_chance
    
    if link_count > 0:
        link_chance = (damping_factor / link_count)

        for key in distribution:
            if key in link_list:
                distribution[key] += link_chance

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank = dict()
    visit_counter = dict()

    for key in corpus:
        PageRank[key] = 0
        visit_counter[key] = 0

    start_page = random.choice(list(corpus)) 
    for j in visit_counter:
        if j == start_page:
            visit_counter[j] +=1
    
    transition = transition_model(corpus, start_page, damping_factor)
    elements = list()
    weights = list()

    for key in transition:
        elements.append(key)
        weights.append(transition[key])

    next_page = random.choices(elements, weights, k=1)
    next_page = next_page[0]

    for i in range(n-1):
        for j in visit_counter:
            if j == next_page:
                visit_counter[j] +=1
    
        transition = transition_model(corpus, next_page, damping_factor)
        elements = list()
        weights = list()

        for key in transition:
            elements.append(key)
            weights.append(transition[key])
    
        next_page = random.choices(elements, weights, k=1)
        next_page = next_page[0]

    for key in PageRank:
        for key in visit_counter:
            PageRank[key] = (visit_counter[key] / n)

    return PageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank = dict()
    page_count = 0

    for key in corpus:
        page_count += 1
    
    first_part = ((1 - damping_factor) / page_count)

    for key in corpus:
        PageRank[key] = (1 / page_count)

    
    for i in range(50):
        for page in corpus:
            sumi = 0
            for key in corpus:
                if corpus[key] == set():
                    sumi += PageRank[key]/page_count
                    PageRank[page] = first_part + (damping_factor*(sumi))                   
                elif page in corpus[key]:
                    sumi += PageRank[key]/len(corpus[key])
                    PageRank[page] = first_part + (damping_factor*(sumi))

    return PageRank

if __name__ == "__main__":
    main()
