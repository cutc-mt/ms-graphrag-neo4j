# MsGraphRAG-Neo4j

QFS（Query-Focused Summarization）に基づいた、知識グラフを活用した検索拡張生成のためのMicrosoft GraphRAGアプローチのNeo4j実装です。
Query-Focused Summarization (QFS) は、ユーザーから提供された特定のクエリや質問に回答または対処するために、与えられたドキュメントまたは一連のドキュメントの簡潔で関連性の高い要約を作成することを目的とした要約タスクです。

GraphRAGについてさらに詳しく学ぶには、[こちら](https://graphrag.com/)をご覧ください。

## 概要

MsGraphRAG-Neo4jは、Neo4jをグラフデータベースのバックエンドとして使用し、MicrosoftのGraphRAG手法を実装したPythonライブラリです。このライブラリは、以下のことをシームレスに行うことができます。

1.  非構造化テキストからエンティティとリレーションシップを抽出する
2.  Neo4jに知識グラフを構築する
3.  ノードとリレーションシップの要約を生成する
4.  グラフ内のコミュニティを検出して要約する
5.  このグラフ構造を活用してRAGを強化する

この実装では、テキスト処理にOpenAIのモデルを使用し、Neo4jの強力なグラフ機能（Graph Data Science (GDS) ライブラリを含む）を活用しています。

> **⚠️ 重要な注意**: このリポジトリは実験的なものであり、現状のまま提供されます。現在の実装では、大規模なグラフに対する最適化が不足しており、大量のデータを処理する際に例外やパフォーマンスの問題が発生する可能性があります。本番環境での使用には注意し、大規模なデプロイメントには追加のエラー処理と最適化の実装を検討してください。

## 機能

-   **エンティティとリレーションシップの抽出**: LLMを使用して非構造化テキストから構造化情報を抽出します
-   **グラフ構築**: Neo4jに知識グラフを自動的に構築します
-   **ノードとリレーションシップの要約**: 検索を改善するために簡潔な要約を生成します
-   **コミュニティ検出**: Neo4j GDSを使用して関連エンティティのクラスターを特定します
-   **コミュニティ要約**: コンセプトクラスターの概要を高いレベルで提供します
-   **Neo4j統合**: 永続ストレージのためのNeo4jデータベースとのシームレスな統合
-   **Azure OpenAIサポート**: LLMとの対話にAzure OpenAI Serviceを使用します。
-   **Neo4jデータベース分離**: 読み取り操作と書き込み操作に異なるNeo4jデータベースを指定します。

## インストール

```bash
pip install -e .
```

## 要件

-   Neo4jデータベース (5.26+)
-   Neo4jにAPOCプラグインがインストールされていること
-   Neo4jにGraph Data Science (GDS) ライブラリがインストールされていること
-   OpenAI APIキー (またはAzure OpenAIの認証情報)

## クイックスタート

```python
import os
import asyncio
from ms_graphrag_neo4j import MsGraphRAG
from neo4j import GraphDatabase
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv()

async def main():
    # 環境変数を設定します (または .env ファイルを使用します)
    # os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    # os.environ["NEO4J_URI"] = "bolt://localhost:7687"
    # os.environ["NEO4J_USERNAME"] = "neo4j"
    # os.environ["NEO4J_PASSWORD"] = "password"

    # Azure OpenAI の場合:
    # os.environ["AZURE_OPENAI_ENDPOINT"] = "your-azure-openai-endpoint"
    # os.environ["AZURE_OPENAI_DEPLOYMENT"] = "your-azure-openai-deployment"
    # os.environ["AZURE_OPENAI_API_VERSION"] = "your-azure-openai-api-version"
    # os.environ["AZURE_OPENAI_API_KEY"] = "your-azure-openai-api-key"

    # Neo4j に接続
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"], 
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
    )

    # MsGraphRAG を初期化 (いずれかを選択):
    # 標準のOpenAI
    # ms_graph = MsGraphRAG(driver=driver, model='gpt-4o')

    # Azure OpenAI
    ms_graph = MsGraphRAG(
        driver=driver,
        azure_openai_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        azure_openai_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        azure_openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY")
    )

    # サンプルテキストとエンティティタイプを定義
    example_texts = [
        "Tomaz works for Neo4j",
        "Tomaz lives in Grosuplje", 
        "Tomaz went to school in Grosuplje"
    ]
    allowed_entities = ["Person", "Organization", "Location"]

    # エンティティとリレーションシップを抽出 (必要に応じて write_database を指定)
    result = await ms_graph.extract_nodes_and_rels(example_texts, allowed_entities, write_database="neo4j")
    print(result)

    # ノードとリレーションシップの要約を生成 (必要に応じて read/write_database を指定)
    result = await ms_graph.summarize_nodes_and_rels(read_database="neo4j", write_database="neo4j")
    print(result)

    # コミュニティを特定して要約 (必要に応じて read/write_database を指定)
    result = await ms_graph.summarize_communities(read_database="neo4j", write_database="neo4j")
    print(result)

    # 接続を閉じる
    ms_graph.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## 動作原理

1.  **ノードとリレーションシップの抽出**: ライブラリはOpenAIのモデルを使用して、テキストデータからエンティティとリレーションシップを抽出し、構造化されたグラフを作成します。

2.  **ノードとリレーションシップの要約**: 各エンティティとリレーションシップは、ソースドキュメント内のすべての言及からその本質を捉えるために要約されます。

3.  **コミュニティ検出**: Leidenアルゴリズムが適用され、関連するエンティティのコミュニティが特定されます。

4.  **コミュニティ要約**: 各コミュニティは、それが含む概念の概要を高いレベルで提供するために要約されます。
