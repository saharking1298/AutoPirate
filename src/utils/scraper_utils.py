import re


def filter_search_results(query: str, results):
    filtered_results = {}
    keywords = re.sub("[\W\s]+", " ", query.strip().lower()).split(" ")
    for (key, item) in results.items():
        result = key.lower()
        valid = True
        for keyword in keywords:
            if keyword not in result:
                valid = False
                break
        if valid:
            filtered_results[key] = item
    return filtered_results
