import os
import asyncio
from ms_graphrag_neo4j import MsGraphRAG
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def main():
    """This is the main function to run the example."""
    # 1. Connect to Neo4j
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
    )

    # 2. Initialize MsGraphRAG for Azure OpenAI
    ms_graph_azure = MsGraphRAG(
        driver=driver,
        azure_openai_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        azure_openai_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        azure_openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY")
    )

    # 3. Define example texts and entity types
    example_texts = [
        "Tomaz works for Neo4j",
        "Tomaz lives in Grosuplje",
        "Tomaz went to school in Grosuplje"
    ]
    allowed_entities = ["Person", "Organization", "Location"]

    # 4. Extract entities and relationships
    # You can specify a database for write operations
    result_azure = await ms_graph_azure.extract_nodes_and_rels(example_texts, allowed_entities, write_database="neo4j")
    print("Azure OpenAI Result:", result_azure)

    # 5. Generate summaries for nodes and relationships
    # You can specify separate databases for read and write operations
    result_summarize = await ms_graph_azure.summarize_nodes_and_rels(read_database="neo4j", write_database="neo4j")
    print("Summarize Result:", result_summarize)

    # 6. Identify and summarize communities
    # You can specify separate databases for read and write operations
    result_communities = await ms_graph_azure.summarize_communities(read_database="neo4j", write_database="neo4j")
    print("Communities Result:", result_communities)

    # 7. Close the connection
    ms_graph_azure.close()

if __name__ == "__main__":
    asyncio.run(main())
