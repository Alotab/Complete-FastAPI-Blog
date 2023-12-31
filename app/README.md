# 

This API provides endpoints for managing posts.

##Authentication
This API requires OAuth2 authentication to access all endpoints.

##Endpoints

Get All Posts

### Get All Posts
GET /posts

Retrieves a list of posts.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Post Title",
    "content": "Post content",
    "owner_id": 1,
    "votes": 10
  },
  ...
]
```json

Parameters:
- limit (optional): The maximum number of posts to return (default: 10)
- skip (optional): The offset from which to start retrieving posts (default: 0)
- search (optional): A search term to filter posts by title (case-insensitive)


### Create Post
POST /posts

Creates a new post.

**Request Body:**
```
{
  "title": "Post Title",
  "content": "Post content"
}

```

**Response:**
```
{
  "id": 1,
  "title": "Post Title",
  "content": "Post content",
  "owner_id": 1,
  "votes": 0
}

```

### Get Post
GET /posts/{id}

Retrieves a specific post.

Parameters:
- `id`: The ID of the post

**Response:**
```
{
  "id": 1,
  "title": "Post Title",
  "content": "Post content",
  "owner_id": 1,
  "votes": 10
}

```

### Delete Post
DELETE /posts/delete/{id}

Deletes a specific post.

Parameters:
- `id`: The ID of the post

**Response:**
```
{
  "message": "posts was successfully deleted"
}
```


### Update Post
PUT /posts/{id}

Updates a specific post.

**Request Body:**
```
{
  "title": "Updated Post Title",
  "content": "Updated post content"
}
```
Parameters:

- `id`: The ID of the post

**Response:**
```
{
  "id": 1,
  "title": "Updated Post Title",
  "content": "Updated post content",
  "owner_id": 1,
  "votes": 10
}
```


# Database Migrations

This project uses Alembic for database migrations. Alembic is a tool for managing database schema changes. It allows you to define migrations, which are incremental changes to the database schema, and apply them to your database in a controlled manner.

To use Alembic, you will need to follow these steps:
1. Create an initial migration:
```
alembic init
```
2. Edit the migration file that is generated to make the desired schema changes.
3. Apply the migration to your database:
```
alembic upgrade
```
4. Repeat steps 2 and 3 for each schema change you make.