import requests
import json
import argparse

def getQueryData(authKey, query, type):

    payload = {
        "query": query,
        "variables": {},
        "operationName": "MyQuery"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": authKey
    }

    url = "https://api.hardcover.app/v1/graphql"

    response = requests.post(url, json=payload, headers=headers)

    response.raise_for_status()

    data = response.json()

    if "errors" in data:
        print("Errors occurred:")
        print(json.dumps(data["errors"], indent=2))
    else:
        with open(f"{type}.json", "w") as f:
            json.dump(data["data"], f, indent=2)
        
        print(f"Data saved to {type}.json")


def getData(auth):
    bookQuery = """
    query MyQuery {
    editions(
      where: {isbn_10: {_is_null: false}, pages: {_is_null: false}, description: {_is_null: false}, publisher_id: {_is_null: false}, book: {book_category_id: {_is_null: false}, image: {url: {_is_null: false}}}, language: {language: {_is_null: false}}}
    ) {
      images {
        url
      }
      isbn_10
      title
      pages
      release_date
      description
      language {
        language
      }
    }
  }
    """

    publisherQuery = """
    query MyQuery {
    publishers {
      name
    }
  }
    """

    genreQuery = """
    query MyQuery {
    book_categories {
        name
    }
    }
    """

    authorQuery = """
    query MyQuery {
    authors {
      name
      death_date
      born_date
    }
  }
    """

    getQueryData(auth, publisherQuery, "publisher")
    getQueryData(auth, authorQuery, "author")
    getQueryData(auth, genreQuery, "genre")
    getQueryData(auth, bookQuery, "book")


def main():
    parser = argparse.ArgumentParser(description="Fetch book genres from Hardcover API.")
    parser.add_argument("--auth", type=str, help="Authorization token (e.g., 'Bearer <token>')")

    args = parser.parse_args()

    if args.auth:
        getData(args.auth)

    else:
        print("No authKey")

if __name__ == "__main__":
    main()