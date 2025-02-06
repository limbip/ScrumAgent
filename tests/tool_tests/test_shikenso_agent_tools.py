# import unittest
#
# from dotenv import load_dotenv
#
# load_dotenv()
#
# import chromadb
# from langchain_chroma import Chroma
# from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
#
#
# class ShikensoAgentToolsTest(unittest.TestCase):
#     def test_search(self):
#         embeddings = SpacyEmbeddings(model_name="en_core_web_sm")
#         persistent_chromadb = chromadb.PersistentClient("../resources/chroma")
#         persistent_chromadb.get_or_create_collection("discord_chat_data")
#
#         chroma_db_inst = Chroma(
#             client=persistent_chromadb,
#             collection_name="discord_chat_data",
#             embedding_function=embeddings,
#         )
#
#         shikenso_discord_search_tool = ShikensoDiscordSearch(chroma_db_inst=chroma_db_inst)
#
#         result = shikenso_discord_search_tool.invoke("Wahed")
#         print(result)
#         self.assertTrue("Wahed Hemati ist in Entwickler und Mitbegründer" in result)
#
#
#     def test_channel_msgs(self):
#         embeddings = SpacyEmbeddings(model_name="en_core_web_sm")
#         #persistent_chromadb = chromadb.PersistentClient("../resources/chroma")
#         #persistent_chromadb.get_or_create_collection("bot_context_data")
#
#         persistent_chromadb = chromadb.PersistentClient("discord_multi_agent/resources/chroma")
#         persistent_chromadb.get_or_create_collection("discord_chat_data")
#
#         chroma_db_inst = Chroma(
#             client=persistent_chromadb,
#             collection_name="discord_chat_data",
#             embedding_function=embeddings,
#         )
#         shikenso_msg_tool = ShikensoDiscordChannelMsgs(chroma_db_inst=chroma_db_inst)
#
#         #result = shikenso_msg_tool.invoke({"channel_name": "awgfawf", "limit": None, "before": None, "after": None})
#         #print(len(result))
#
#         result = shikenso_msg_tool.invoke({"channel_name": "#1821 Chatbot v2 (Agent system)"})
#         print(len(result))
#         print(result)
#         print("!!!!!!!!!!!!!!!!!!")
#
#
#
#
# if __name__ == '__main__':
#     unittest.main()
