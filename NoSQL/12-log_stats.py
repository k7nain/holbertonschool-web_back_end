#!/usr/bin/env python3
"""
Provides stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()
    collection = client.logs.nginx

    # total logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # status check
    status_count = collection.count_documents({
        "method": "GET",
        "path": "/status"
    })

    print(f"{status_count} status check")
