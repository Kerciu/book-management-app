Database documentation:
POST REQUESTS:
  - create category - `curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "CategoryName"}'`
  - create author - `curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "AuthorName"}'`
  - create book - `curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "BookTitle",
    "published_at": "RRRR-MM-DD",
    "author_id": 1,
    "categories": [LIST_OF_ID]
  }'`
  - create collection - `curl -X POST http://localhost:8000/api/collections/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CollectionName",
    "user_id": 1,
    "books_id": [LIST_OF_ID]
  }'`
  - create Rating - `curl -X POST http://localhost:8000/api/ratings/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "book_id": 1,
    "rating": 5
  }'`
  - create Review - `curl -X POST http://localhost:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "book_id": 1,
    "review": "Review"
  }'`
GET REQUESTS:
  - `curl -X GET http://localhost:8000/api/TableName/`
