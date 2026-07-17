from app.database_mongo import generations_collection

result = generations_collection.insert_one(
    {
        "message": "MongoDB connection successful!"
    }
)

print("Inserted document ID:", result.inserted_id)