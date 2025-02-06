import json
import unittest
from dotenv import load_dotenv

load_dotenv()


class TaigaAgentToolsTest(unittest.TestCase):
    def test_get_project(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import get_project
        projects = get_project()
        self.assertTrue(projects is None)

        projects = get_project(None)
        self.assertTrue(projects is None)

        projects = get_project("This does not exist")
        self.assertTrue(projects is None)

        projects = get_project("Development")
        self.assertTrue(projects is not None)

    def test_get_issues(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import get_issues
        issues = get_issues("")
        self.assertTrue(issues == [])

        issues = get_issues(None)
        self.assertTrue(issues == [])

        issues = get_issues("This does not exist")
        self.assertTrue(issues == [])

        issues = get_issues("Development")
        self.assertTrue(len(issues) > 1000)

        issues_filtered = get_issues("Development", 18)  # I think this one is closed
        self.assertTrue(len(issues_filtered) > 0)
        self.assertTrue(len(issues_filtered) < len(issues))

    def test_get_sprints(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import taiga_list_open_sprint_user_stories_tool

        sprints = taiga_list_open_sprint_user_stories_tool("This does not exist")
        self.assertEquals(sprints, "Project 'This does not exist' not found.")

        open_sprints = taiga_list_open_sprint_user_stories_tool("Development")
        open_sprints_json = json.loads(open_sprints)
        self.assertTrue(len(open_sprints_json) > 0)
        self.assertTrue(len(list(open_sprints_json.values())[0]) > 0)

    def test_get_user_story_infos(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import taiga_get_user_story_info_tool

        user_story = taiga_get_user_story_info_tool({"user_story_id": -1})
        self.assertTrue("error" in user_story)

        user_story = taiga_get_user_story_info_tool({"user_story_id": 0})
        self.assertTrue("error" in user_story)

        user_story = taiga_get_user_story_info_tool({"user_story_id": 1222})
        self.assertTrue("status" in user_story)
        self.assertTrue("assigned_to" in user_story)
        self.assertTrue("subject" in user_story)
        self.assertTrue("assigned_users" in user_story)
        self.assertTrue("tasks" in user_story)

    def test_update_user_story(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import taiga_update_user_story_tool
        # user_story = taiga_update_user_story_tool(None)
        # self.assertTrue("error" in user_story)
        #
        # user_story = taiga_update_user_story_tool(-1)
        # self.assertTrue("error" in user_story)
        #
        # user_story = taiga_update_user_story_tool(0)
        # self.assertTrue("error" in user_story)
        #
        # user_story = update_user_story(1298)
        # self.assertTrue("error" not in user_story)

        """ Could not test for now with my permissions
        user_story_update = update_user_story(1298, assigned_to=9, status=13, watchers=[9, 51]) # Default variables
        old_user_story = get_user_story_infos(1298)

        user_story_update = update_user_story(1298, description= "", assigned_to=10, status=14, watchers=[])
        new_user_story = get_user_story_infos(1298)

        self.assertTrue(old_user_story["assigned_to"] != new_user_story["assigned_to"])
        self.assertTrue(old_user_story["status"] != new_user_story["status"])
        self.assertTrue(old_user_story["watchers"] != new_user_story["watchers"])
        self.assertTrue(new_user_story["description"] == "")

        user_story_update = update_user_story(1298,description=old_user_story["description"], assigned_to=9, status=13, watchers=[9, 51]) # Default variables
        """

    def test_update_task(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import taiga_update_task_tool

        task = taiga_update_task_tool({"task_id": -1})
        self.assertTrue("error" in task)

        task = taiga_update_task_tool({"task_id": 0})
        self.assertTrue("error" in task)

        # Could not test for now with my permissions
        task = taiga_update_task_tool({"task_id": 3375})
        self.assertTrue("error" not in task and "Research about Langgraph agents" in json.loads(task)["subject"])

    def test_add_comment_to_user_story(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import add_comment_to_user_story
        result = add_comment_to_user_story(None, "This is a test comment")
        self.assertTrue("error" in result)
        result = add_comment_to_user_story(-1, "This is a test comment")
        self.assertTrue("error" in result)
        result = add_comment_to_user_story(0, "This is a test comment")
        self.assertTrue("error" in result)

    def test_add_comment_to_task(self):
        from autobotcentral.discord_multi_agent.agents.tools.taiga_tool import add_comment_to_task
        result = add_comment_to_task(None, "This is a test comment")
        self.assertTrue("error" in result)
        result = add_comment_to_task(-1, "This is a test comment")
        self.assertTrue("error" in result)
        result = add_comment_to_task(0, "This is a test comment")
        self.assertTrue("error" in result)

    # def test_add_comment_to_issue(self):
    #     result = add_comment_to_issue(None, "This is a test comment")
    #     self.assertTrue("error" in result)
    #     result = add_comment_to_issue(-1, "This is a test comment")
    #     self.assertTrue("error" in result)
    #     result = add_comment_to_issue(0, "This is a test comment")
    #     self.assertTrue("error" in result)


if __name__ == '__main__':
    unittest.main()
