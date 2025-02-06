import unittest
from dotenv import load_dotenv
load_dotenv()

from autobotcentral.agents import web_agent


class WebAgentToolsTest(unittest.TestCase):
    def test_ddg(self):
        first_result = web_agent.ddg_tool.run("What is the capital of France?")[0]
        self.assertTrue("link" in first_result)
        self.assertTrue("snippet" in first_result)
        self.assertTrue("title" in first_result)

    def test_arxiv(self):
        result = web_agent.arxiv_tool.run("Wahed Hemati")
        self.assertTrue(type(result) == str)
        self.assertTrue(len(result) > 0)
        self.assertTrue("Wahed Hemati" in result)
        self.assertTrue("Published:" in result)
        self.assertTrue("Title:" in result)
        self.assertTrue("Authors:" in result)
        self.assertTrue("Summary:" in result)

    def test_youtube(self):
        result = web_agent.youtube_tool.run("Shikenso Analytics")
        self.assertTrue("https://www.youtube.com/watch?v=O93sxJaI0vE" in result)

    def test_wikipedia(self):
        result = web_agent.wiki_tool.run("Konrad Zuse")
        self.assertTrue("Page: Konrad Zuse" in result)
        self.assertTrue("Summary:" in result)


if __name__ == '__main__':
    unittest.main()
