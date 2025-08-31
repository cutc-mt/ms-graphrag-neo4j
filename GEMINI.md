# Project Overview

This project is a Python library named `ms-graphrag-neo4j` that implements Microsoft's GraphRAG methodology using Neo4j as the graph database backend. It is designed to extract entities and relationships from unstructured text, build a knowledge graph in Neo4j, and then use this graph for retrieval-augmented generation (RAG). The library leverages OpenAI's language models for text processing and summarization, and it uses Neo4j's Graph Data Science (GDS) library for community detection.

The core of the library is the `MsGraphRAG` class, which provides methods to:
- Extract nodes (entities) and relationships from text.
- Summarize nodes and relationships.
- Detect and summarize communities within the graph.

The project is structured as a standard Python package with a `src` directory containing the main source code and a `pyproject.toml` file for packaging and dependency management.

# Building and Running

## Installation

To install the package and its dependencies, run the following command in the project root:

```bash
pip install -e .
```

## Dependencies

The project has the following dependencies:
- `neo4j>=5.28.1`
- `openai>=1.69.0`
- `python-dotenv>=0.21.0`
- `asyncio>=3.4.3`

## Running the code

To use the library, you need to have a Neo4j database (version 5.26+ with APOC and GDS plugins installed) and an OpenAI API key. You can then use the `MsGraphRAG` class as shown in the `README.md` and the example below:

```python
import os
from ms_graphrag_neo4j import MsGraphRAG
from neo4j import GraphDatabase

# Set your environment variables
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"

# Connect to Neo4j
driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
)

# Initialize MsGraphRAG
ms_graph = MsGraphRAG(driver=driver, model='gpt-4o')

# Define example texts and entity types
example_texts = [
    "Tomaz works for Neo4j",
    "Tomaz lives in Grosuplje",
    "Tomaz went to school in Grosuplje"
]
allowed_entities = ["Person", "Organization", "Location"]

# Extract entities and relationships
result = ms_graph.extract_nodes_and_rels(example_texts, allowed_entities)
print(result)

# Generate summaries for nodes and relationships
result = ms_graph.summarize_nodes_and_rels()
print(result)

# Identify and summarize communities
result = ms_graph.summarize_communities()
print(result)

# Close the connection
ms_graph.close()
```

### Azure OpenAI Support

To use Azure OpenAI, set the following environment variables in your `.env` file:

```
AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint"
AZURE_OPENAI_DEPLOYMENT="your-azure-openai-deployment"
AZURE_OPENAI_API_VERSION="your-azure-openai-api-version"
AZURE_OPENAI_API_KEY="your-azure-openai-api-key"
```

Then, initialize `MsGraphRAG` like this:

```python
ms_graph = MsGraphRAG(
    driver=driver,
    azure_openai_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    azure_openai_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    azure_openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY")
)
```

### Neo4j Database Read/Write Separation

You can specify different databases for read and write operations in the `extract_nodes_and_rels`, `summarize_nodes_and_rels`, and `summarize_communities` methods.

Example:

```python
# Extract entities and relationships to a specific write database
result = await ms_graph.extract_nodes_and_rels(example_texts, allowed_entities, write_database="my_write_db")

# Summarize nodes and relationships, reading from one database and writing to another
result = await ms_graph.summarize_nodes_and_rels(read_database="my_read_db", write_database="my_write_db")

# Summarize communities, reading from one database and writing to another
result = await ms_graph.summarize_communities(read_database="my_read_db", write_database="my_write_db")
```

# Development Conventions

- The project follows a standard Python project structure.
- The main logic is encapsulated in the `MsGraphRAG` class in `src/ms_graphrag_neo4j/ms_graphrag.py`.
- Cypher queries are separated into `src/ms_graphrag_neo4j/cypher_queries.py`.
- Prompts for the OpenAI API are stored in `src/ms_graphrag_neo4j/prompts.py`.
- Utility functions are in `src/ms_graphrag_neo4j/utils.py`.
- The code makes extensive use of asynchronous programming with `asyncio`.
- The project uses `hatchling` for building.
