import os
import unittest
from dotenv import load_dotenv


from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()
os.environ.pop("MONGO_DB_URL", None)
#del os.environ['MONGO_DB_URL'] # force MemorySaver


class SupervisorAgent(unittest.TestCase):
    def test_msg_trim(self):
        os.environ['MAX_MSG_COUNT'] = "5"
        os.environ['MAX_MSG_MODE'] = "trim"

        from scrumagent.build_agent_graph import build_graph
        multi_agent_graph = build_graph()

        test_chat_history = [
            HumanMessage(content="Hey there! I'm Nemo."),
            AIMessage(content="Hello!"),
            HumanMessage(content="How are you today?"),
            AIMessage(content="Fine thanks!"),
        ]

        result = multi_agent_graph.invoke(
            {
                "messages": test_chat_history
                            + [HumanMessage(content="What's my name?")]
            },
            config = {"configurable": {"thread_id": "2"}},
            debug=True
        )
        self.assertTrue("Nemo" in result["messages"][-1].content)


        test_chat_history = [
            HumanMessage(content="Hey there!"),
            HumanMessage(content="I'm Nemo."),
            AIMessage(content="Hello!"),
            HumanMessage(content="How are you today?"),
            AIMessage(content="Fine thanks!"),
            HumanMessage(content="That is nice to hear :)"),
        ]

        result = multi_agent_graph.invoke(
            {
                "messages": test_chat_history
                            + [HumanMessage(content="What's my name?")]
            },
            config = {"configurable": {"thread_id": "2"}},
            debug=True
        )

        self.assertTrue("Nemo" not in result["messages"][-1].content)




    def test_msg_sum(self):
        os.environ['MAX_MSG_COUNT'] = "5"
        os.environ['MAX_MSG_MODE'] = "summary"

        from scrumagent.build_agent_graph import build_graph
        multi_agent_graph = build_graph()


        test_chat_history = [
            HumanMessage(content="Hey there! I'm Nemo."),
            AIMessage(content="Hello!"),
            HumanMessage(content="How are you today?"),
            AIMessage(content="Fine thanks!"),
            HumanMessage(content="That is nice to hear"),
            AIMessage(content=":)"),
        ]

        result = multi_agent_graph.invoke(
            {
                "messages": test_chat_history
                            + [HumanMessage(content="What's my name?")]
            },
            config={"configurable": {"thread_id": "2"}},
            debug=True
        )

        self.assertTrue(result["messages"][0].content.startswith("Chat History:"))
        self.assertTrue("Nemo" in result["messages"][-1].content)  # Bot knows the name because of the summary



if __name__ == '__main__':
     unittest.main()
