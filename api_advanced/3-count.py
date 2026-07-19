#!/usr/bin/python3
"""Recursively count keyword occurrences in a subreddit's hot post titles."""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of keywords found across all hot post titles."""
    if counts is None:
        counts = {}
        for word in word_list:
            counts[word.lower()] = counts.get(word.lower(), 0)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-scripting:api_advanced:v1.0 (by /u/student)"}
    params = {"limit": 100, "after": after}
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    for post in data.get("children", []):
        title_words = post.get("data", {}).get("title", "").lower().split()
        for word in word_list:
            counts[word.lower()] += title_words.count(word.lower())

    after = data.get("after")
    if after is not None:
        return count_words(subreddit, word_list, after, counts)

    sorted_counts = sorted(
        [(key, value) for key, value in counts.items() if value > 0],
        key=lambda item: (-item[1], item[0]))
    for word, count in sorted_counts:
        print("{}: {}".format(word, count))
