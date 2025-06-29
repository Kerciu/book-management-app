import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from book.models import *
from authentication.models import *
import json

def readAuthors(path):
    with open(path, 'r+') as f:
        data = json.load(f)
        for author in data["authors"]:
            name = author["name"]
            death_date = author["death_date"]
            born_date = author["born_date"]
            Author.objects.create(name=name, death_date=death_date, birth_date=born_date)

def readPublishers(path):
    with open(path, 'r+') as f:
        data = json.load(f)
        for publisher in data["publishers"]:
            name = publisher["name"]
            Publisher.objects.create(name=name)

def readGenres(path):
    with open(path, 'r+') as f:
        data = json.load(f)
        for genre in data["book_categories"]:
            name = genre["name"]
            Genre.objects.create(name=name)

def readBooks(path):
    maxPublisher = Publisher.objects.count()
    maxAuthor = Author.objects.count()
    maxGenre = Genre.objects.count()
    with open(path, 'r+') as f:
        data = json.load(f)
        for book in data["editions"][:500]: 
            isbn = book["isbn_10"]
            title = book["title"]
            page_count = book["pages"]
            published_at = book["release_date"]
            description = book["description"]
            language = book["language"]["language"].split(";")[-1].strip()
            imageURL = None
            try:
                imageURL = book["images"][0]["url"]
            except:
                pass
            publisherID = random.sample(range(1, maxPublisher+1), random.randrange(1, min(4, maxPublisher+1)))
            authorID = random.sample(range(1, maxAuthor+1), random.randrange(1, min(4,maxAuthor+1)))
            genreID = random.sample(range(1, maxGenre+1), random.randrange(1, min(5,maxGenre+1)))
            publisher = []
            for ID in publisherID:
                publisher.append(Publisher.objects.get(id=ID))
            author = []
            for ID in authorID:
                author.append(Author.objects.get(id=ID))
            genre = []
            for ID in genreID:
                genre.append(Genre.objects.get(id=ID))

            try:
                book_obj = Book.objects.create(
                    title=title,
                    description=description,
                    isbn=isbn,
                    published_at=published_at,
                    page_count=page_count,
                    language=language,
                    cover_image=imageURL
                )
                book_obj.authors.set(author)
                book_obj.genres.set(genre)
                book_obj.publishers.set(publisher)
            except Exception:
                print("sth went wrong")

def addUser():
    name = 1
    lname = 1
    mail = "@gmail.com"
    for _ in range(30):
        nameChar = chr(name%26 + 65)
        lnameChar = chr(lname%26 + 65)
        if name > 26:
            nameChar += chr(name%26 + 65)
            lnameChar += chr(lname%26 + 65)
        name += 1
        lname += 1
        email = nameChar + lnameChar + mail
        try:
            CustomUser.objects.create(username=name+lname, email=email, first_name=nameChar, last_name=lnameChar)
        except Exception:
            print(email)




def fillDB():
    authorsPath = "author.json"
    publishersPath = "publisher.json"
    genresPath = "genre.json"
    booksPath = "book.json"
    readAuthors(authorsPath)
    readPublishers(publishersPath)
    readGenres(genresPath)
    readBooks(booksPath)
    addUser()

def main():
    fillDB()

if __name__ == "__main__":
    main()
