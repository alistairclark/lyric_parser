import requests


STOP_WORDS = [
        "a",
        "about",
        "all",
        "also",
        "and",
        "as",
        "at",
        "be",
        "because",
        "but",
        "by",
        "can",
        "come",
        "could",
        "day",
        "do",
        "even",
        "find",
        "first",
        "for",
        "from",
        "get",
        "give",
        "go",
        "have",
        "he",
        "her",
        "here",
        "him",
        "his",
        "how",
        "I",
        "if",
        "in",
        "into",
        "it",
        "its",
        "just",
        "know",
        "like",
        "look",
        "make",
        "man",
        "many",
        "me",
        "more",
        "my",
        "new",
        "no",
        "not",
        "now",
        "of",
        "on",
        "one",
        "only",
        "or",
        "other",
        "our",
        "out",
        "people",
        "say",
        "see",
        "she",
        "so",
        "some",
        "take",
        "tell",
        "than",
        "that",
        "the",
        "their",
        "them",
        "then",
        "there",
        "these",
        "they",
        "thing",
        "think",
        "this",
        "those",
        "time",
        "to",
        "two",
        "up",
        "use",
        "very",
        "want",
        "way",
        "we",
        "well",
        "what",
        "when",
        "which",
        "who",
        "will",
        "with",
        "would",
        "year",
        "you",
        "your",
        "[verse]"
    ]


def search_genius(search_term):
    headers = {
        "Authorization": "Bearer {}".format(
            "umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa"
        )
    }

    response = requests.get(
        "https://api.genius.com/search?q={}".format(search_term),
        headers=headers
    )

    results = response.json()["response"]["hits"]
    data = {}

    for result in results:
        data[result["result"]["primary_artist"]["id"]] = {
            "name": result["result"]["primary_artist"]["name"],
            "image_url": result["result"]["primary_artist"]["image_url"]
        }

    return data

