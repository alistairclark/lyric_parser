import requests


def search_genius(search_term):
    headers = {
        "Authorization": "Bearer {}".format(
            "umuTypKle_tO2TrPvkM6FDqDiV1LIevm8QvHd92fJ4o-2Ui0h2yfnsyNwxeY9cUa")
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