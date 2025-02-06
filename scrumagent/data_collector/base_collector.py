import discord
from langchain_chroma import Chroma
from langchain_core.documents import Document


class BaseCollector:
    # DB_IDENTIFIER is used to identify the source of the data in the DB
    # Add as source in the metadata of the document
    # And in front of the ID of the document
    # TODO: Do this automatic in the base class
    DB_IDENTIFIER = "base"

    def __init__(self, bot: discord.Client, db: Chroma):
        self.bot = bot
        self.db = db

    async def on_startup(self):
        raise NotImplementedError

    def add_to_db(self, _id: str, text: str, metadata: {}) -> [str]:
        return self.add_to_db_batch(ids=[_id], texts=[text], metadatas=[metadata])

    def add_to_db_batch(self, ids: [str], texts: [str], metadatas: [{}]) -> [str]:
        print(f"Adding {len(ids)} docs to the DB")
        return self.db.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    def add_to_db_docs(self, docs: [Document], ids: [str] = None) -> [str]:
        texts = [doc.page_content for doc in docs]
        metadatas = [doc.metadata for doc in docs]
        return self.add_to_db_batch(ids=ids, texts=texts, metadatas=metadatas)
