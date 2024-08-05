import os

from langchain.vectorstores import Chroma, PGVector
import psycopg2
from psycopg2 import pool
from config.config import (
    postgres_database,
    postgres_user,
    postgres_password,
    postgres_host,
    postgres_port,
)


class ChromaDB:
    def __init__(self, persist_directory, embeddings, init=False):
        self.persist_directory = persist_directory

        if init:
            os.system(f"rm -rf {self.persist_directory}")

        self.vectordb = Chroma(
            persist_directory=persist_directory, embedding_function=embeddings
        )

    def store(self, texts):
        self.vectordb.add_texts(texts)
        self.vectordb.persist()

    def store_with_metadata(self, texts, metadata):
        self.vectordb.add_texts(texts, metadata)

    def store_list(self, texts_list):
        for texts in texts_list:
            self.vectordb.add_texts(texts)

        self.vectordb.persist()

    def similarity_search(self, search_string, k=3):
        docs = self.vectordb.similarity_search(search_string, k=k)
        return docs

    def similarity_search_with_score(self, search_string, k=3):
        docs = self.vectordb.similarity_search_with_score(search_string, k=k)
        return docs

    def max_marginal_relevance_search(self, search_string, k=3):
        docs = self.vectordb.max_marginal_relevance_search(search_string, k=k)
        return docs


class PostgresDB:
    _connection_pool = None

    @classmethod
    def initialize_connection_pool(cls):
        cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,
            100,
            user=postgres_user,
            password=postgres_password,
            host=postgres_host,
            port=postgres_port,
            database=postgres_database,
        )

    @classmethod
    def get_connection(cls):
        return cls._connection_pool.getconn()

    @classmethod
    def put_connection(cls, conn):
        cls._connection_pool.putconn(conn)

    def __init__(
        self,
        collection_name,
        connection_string,
        embeddings,
        init=False,
        session_id="000000",
    ):
        self.session_id = session_id
        self.vector = PGVector(
            collection_name=collection_name,
            connection_string=connection_string,
            embedding_function=embeddings,
            pre_delete_collection=init,
        )
        PostgresDB.initialize_connection_pool()
        self.create_query = "CREATE TABLE IF NOT EXISTS chat_history(id SERIAL PRIMARY KEY, conversation_id TEXT, input TEXT, output TEXT, created_at TIMESTAMPTZ)"
        self.create_table(self.create_query)

    def create_table(self, create_query):
        conn = self.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(create_query)
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()
            self.put_connection(conn)

    def insert(self, query, new_row):
        conn = self.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(query, new_row)
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()
            self.put_connection(conn)

    def fetch(self, fetch_query):
        conn = self.get_connection()
        result = None
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(fetch_query)
            result = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            if cursor:
                cursor.close()
            self.put_connection(conn)
        return result

    def store(self, text, metadata, embeddings_):
        return self.vector.add_embeddings(
            texts=text, metadatas=metadata, embeddings=embeddings_
        )

    def get_as_retriever(self):
        return self.vector.as_retriever()

    def store_textx(self, texts):
        self.vector.add_texts(texts)

    def store_texts_with_metadata(self, texts, metadata):
        self.vector.add_texts(texts, metadata)

    def store_documents(self, documents):
        self.vector.add_documents(documents)

    def similarity_search(self, search_string, k=3):
        docs = self.vector.similarity_search(search_string, k=k)
        return docs

    def similarity_search_with_score(self, search_string, k=3):
        docs = self.vector.similarity_search_with_score(search_string, k=k)
        return docs

    def max_marginal_relevance_search(self, search_string, k=3):
        docs = self.vector.max_marginal_relevance_search(search_string, k=k)
        return docs
