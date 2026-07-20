# scripts/list_pinecone_indexes.py
# Lists all Pinecone indexes using the official Pinecone Python client.
# This script expects the environment variable PINECONE_API_KEY to contain
# a valid Pinecone API key. If the variable is missing or still set to the
# placeholder value "***", the script will abort with a clear error message.

import os
from pinecone import Pinecone

# ------------------------------------------------------------
# Step 1: Validate that a real API key is available
# ------------------------------------------------------------
api_key = os.getenv("PINECONE_API_KEY")
if not api_key or api_key == "***":
    raise RuntimeError(
        "PINECONE_API_KEY is not set or still contains the placeholder value. "
        "Set it to your actual Pinecone API key and retry."
    )

# ------------------------------------------------------------
# Step 2: Connect to Pinecone and fetch index names
# ------------------------------------------------------------
pc = Pinecone(api_key=api_key)
try:
    # The `list_indexes()` call returns an object whose `.names` attribute
    # holds a list of index names.
    indexes = pc.list_indexes()
    index_names = indexes.names if hasattr(indexes, "names") else []
    print("Current Pinecone indexes:", index_names)
except Exception as e:
    print("Error while querying Pinecone:", e)
    raise