# MongoDB Atlas Vector Search Configuration

To enable vector search capabilities for the DecisionOS database, you must create a Vector Search index in the MongoDB Atlas console.

## Configuration Steps

1. Log in to your **MongoDB Atlas** account.
2. Navigate to **Atlas Search** in the left-hand sidebar.
3. Click on **Create Search Index**.
4. Select **JSON Editor**.
5. Select the `DecisionOS` database and the `decisions` collection.
6. Paste the following JSON specification:

```json
{
  "name": "vector_index",
  "type": "vectorSearch",
  "definition": {
    "fields": [
      {
        "type": "vector",
        "path": "embedding",
        "numDimensions": 1536,
        "similarity": "cosine"
      }
    ]
  }
}
```

## Technical Details
- **Index Name**: `vector_index`
- **Field Path**: `embedding` (matches the field in [`models.py`](models.py))
- **Dimensions**: `1536` (standard for `text-embedding-3-small`)
- **Similarity Metric**: `cosine` (recommended for text embeddings)

## Verification
Once the index is created, the `DatabaseService.verify_vector_index()` method in [`database_service.py`](database_service.py) can be used to ensure the system is ready for vector queries.
