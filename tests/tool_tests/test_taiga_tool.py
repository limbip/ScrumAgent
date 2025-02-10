import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import requests
from langchain_openai import ChatOpenAI
from taiga import TaigaAPI
from taiga.exceptions import TaigaException
from taiga.models import (
    Point,
    Project,
    Projects,
    Severity,
    SwimLane,
    User,
    UserStoryStatus,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from scrumagent.tools.taiga_tool import (
    add_comment_by_ref_tool,
    fetch_entity,
    get_entity_by_ref_tool,
    get_project,
    get_status,
    normalize_entity_type,
    update_entity_by_ref_tool,
)


class TestGetProject(unittest.TestCase):
    def setUp(self):
        # Mock the project object
        self.project_slug = "test-project"
        self.entity_ref = 123
        self.entity_type = "task"
        self.taiga_url = "http://localhost:9000/"
        self.project = MagicMock()

    @patch("scrumagent.tools.taiga_tool.normalize_entity_type")
    def test_unsupported_entity_type(self, mock_normalize):
        # Setup mock
        mock_normalize.return_value = None

        # Invoke the function
        response = get_entity_by_ref_tool(self.project_slug, self.entity_ref, "unknown")
        response_dict = json.loads(response)

        # Check the response
        self.assertEqual(
            response_dict["error"], "Entity type 'unknown' is not supported."
        )
        self.assertEqual(response_dict["code"], 400)

    # More tests for project not found, entity not found, fetching error, etc.

    @patch("scrumagent.tools.taiga_tool.fetch_entity")
    @patch("scrumagent.tools.taiga_tool.get_project")
    @patch("scrumagent.tools.taiga_tool.normalize_entity_type")
    def test_successful_comment_addition(
        self, mock_normalize, mock_get_project, mock_fetch_entity
    ):
        # Setup mocks
        mock_normalize.return_value = "task"
        mock_project = MagicMock()
        mock_project.name = "test-project"
        mock_get_project.return_value = mock_project
        mock_entity = MagicMock()
        mock_fetch_entity.return_value = mock_entity

        # Invoke the function
        comment_text = "QA verified fix"
        response = add_comment_by_ref_tool(
            {
                "project_slug": "test-project",
                "entity_ref": 1421,
                "entity_type": "task",
                "comment": comment_text,
            }
        )
        response_dict = json.loads(response)

        # Check the response
        self.assertTrue(response_dict["added"])
        self.assertEqual(response_dict["project"], "test-project")
        self.assertEqual(response_dict["type"], "task")
        self.assertEqual(response_dict["ref"], 1421)
        self.assertEqual(response_dict["comment_preview"], comment_text)
        mock_entity.add_comment.assert_called_once_with(comment_text[:500])

    @patch("scrumagent.tools.taiga_tool.normalize_entity_type")
    def test_unsupported_entity_type(self, mock_normalize):
        # Setup mock
        mock_normalize.return_value = None

        # Adjusted invoke
        response = add_comment_by_ref_tool(
            {
                "project_slug": "test-project",
                "entity_ref": 887,
                "entity_type": "unknown",
                "comment": "Sample comment",
            }
        )
        response_dict = json.loads(response)

        # Check the response
        self.assertEqual(response_dict["error"], "Invalid entity type 'unknown'")
        self.assertEqual(response_dict["code"], 400)

    @patch("scrumagent.tools.taiga_tool.get_project")
    @patch("scrumagent.tools.taiga_tool.normalize_entity_type")
    def test_project_not_found(self, mock_normalize, mock_get_project):
        # Setup mocks
        mock_normalize.return_value = "userstory"
        mock_get_project.return_value = None

        # Invoke the function
        response = add_comment_by_ref_tool(
            "invalid-project", 887, "userstory", "UX review completed"
        )
        response_dict = json.loads(response)

        # Check the response
        self.assertEqual(response_dict["error"], "Project 'invalid-project' not found")
        self.assertEqual(response_dict["code"], 404)

    @patch("scrumagent.tools.taiga_tool.get_project")
    @patch("scrumagent.tools.taiga_tool.normalize_entity_type")
    def test_project_not_found(self, mock_normalize, mock_get_project):
        # Set up mocks
        mock_normalize.return_value = "task"
        mock_get_project.return_value = None

        # Invoke the function
        response = update_entity_by_ref_tool(
            {
                "project_slug": "invalid-project",
                "entity_ref": 123,
                "entity_type": "task",
                "updates": {"status": "done"},
            }
        )
        response_dict = json.loads(response)

        # Check the response
        self.assertEqual(response_dict["error"], "Project 'invalid-project' not found")
        self.assertEqual(response_dict["code"], 404)

    @patch("scrumagent.tools.taiga_tool.fetch_entity")
    @patch("scrumagent.tools.taiga_tool.get_project")
    @patch("scrumagent.tools.taiga_tool.normalize_entity_type")
    def test_error_during_update(
        self, mock_normalize, mock_get_project, mock_fetch_entity
    ):
        # Set up mocks
        mock_normalize.return_value = "task"
        mock_project = MagicMock()
        mock_get_project.return_value = mock_project
        mock_entity = MagicMock()
        mock_entity.update.side_effect = Exception("Update failed")
        mock_fetch_entity.return_value = mock_entity

        # Invoke the function
        response = update_entity_by_ref_tool(
            {
                "project_slug": self.project_slug,
                "entity_ref": self.entity_ref,
                "entity_type": self.entity_type,
                "updates": {"status": "done"},
            }
        )
        response_dict = json.loads(response)

        # Check the response
        self.assertEqual(
            response_dict["error"], "Error updating task 123: Update failed"
        )
        self.assertEqual(response_dict["code"], 500)

    def test_fetch_task_entity(self):
        # Setup the mock for task
        self.project.get_task_by_ref.return_value = "Task Entity"
        result = fetch_entity(self.project, "task", 123)
        self.project.get_task_by_ref.assert_called_once_with(123)
        self.assertEqual(result, "Task Entity")

    def test_fetch_user_story_entity(self):
        # Setup the mock for user story
        self.project.get_userstory_by_ref.return_value = "User Story Entity"
        result = fetch_entity(self.project, "us", 456)
        self.project.get_userstory_by_ref.assert_called_once_with(456)
        self.assertEqual(result, "User Story Entity")

    def test_fetch_issue_entity(self):
        # Setup the mock for issue
        self.project.get_issue_by_ref.return_value = "Issue Entity"
        result = fetch_entity(self.project, "issue", 789)
        self.project.get_issue_by_ref.assert_called_once_with(789)
        self.assertEqual(result, "Issue Entity")

    def test_fetch_invalid_type(self):
        # Test fetching an entity with an unsupported type
        result = fetch_entity(self.project, "invalid_type", 101)
        self.assertIsNone(result)
        self.project.get_task_by_ref.assert_not_called()
        self.project.get_userstory_by_ref.assert_not_called()
        self.project.get_issue_by_ref.assert_not_called()

    @patch("scrumagent.tools.taiga_tool.taiga_api.task_statuses.get")
    @patch("scrumagent.tools.taiga_tool.get_project")
    @patch("scrumagent.tools.taiga_tool.normalize_entity_type")
    def test_get_status_successful(
        self, mock_normalize, mock_get_project, mock_task_status_get
    ):
        # Setup mocks
        mock_normalize.return_value = "task"
        mock_get_project.return_value = MagicMock(name="Test Project", id=1)

        # Mock task_statuses.get to return a mock object with a method to_dict
        mock_status = MagicMock()
        mock_status.to_dict.return_value = {
            "name": "New",
            "order": 1,
            "is_closed": False,
            "color": "#70728F",
            "project": 1,
        }
        mock_task_status_get.return_value = mock_status

        # Test function
        result = get_status("test_project", "task", 1)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "New")

    def test_normalize_entity_type(self):
        # Test normalization for each defined entity type
        self.assertEqual(normalize_entity_type("task"), "task")
        self.assertEqual(normalize_entity_type("tasks"), "task")
        self.assertEqual(normalize_entity_type("userstory"), "us")
        self.assertEqual(normalize_entity_type("userstories"), "us")
        self.assertEqual(normalize_entity_type("issue"), "issue")
        self.assertEqual(normalize_entity_type("issues"), "issue")
        # Test normalization for an undefined entity type
        self.assertIsNone(normalize_entity_type("invalid_type"))

    @patch("scrumagent.tools.taiga_tool.taiga_api.projects.get_by_slug")
    def test_get_project_success(self, mock_get_by_slug):
        # Set up the mock to return a Project object
        mock_project = MagicMock()
        mock_project.name = "Test Project"
        mock_get_by_slug.return_value = mock_project

        # Call the function
        result = get_project("Test Project")

        # Assertions to check if the function behaves as expected
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test Project")

    @patch("scrumagent.tools.taiga_tool.taiga_api.projects.get_by_slug")
    def test_get_project_not_found(self, mock_get_by_slug):
        # Set up the mock to raise an exception
        mock_get_by_slug.side_effect = Exception("Project not found")

        # Call the function
        result = get_project("invalid-slug")

        # Check if the result is None due to the exception
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
