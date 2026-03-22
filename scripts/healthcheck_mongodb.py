#!/usr/bin/env python3
"""
MongoDB Healthcheck Script
- Verifies connectivity to MongoDB before Meltano runs
- Exits with non-zero code if connection fails
"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def main():
    # Load connection details from environment variables
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB", "test")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Force connection check
        client.admin.command("ping")
        db = client[db_name]
        print(f"✅ Connected to MongoDB at {mongo_uri}, database: {db_name}")
        sys.exit(0)
    except (ConnectionFailure, OperationFailure) as e:
        print(f"❌ Could not connect to MongoDB: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()