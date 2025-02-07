from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from scrumagent.tools.taiga_tool_v2 import (get_entity_by_ref_tool,
                                                update_entity_by_ref_tool,
                                                add_comment_by_ref_tool,
                                                create_entity_tool,
                                                search_entities_tool)

llm = ChatOpenAI(model_name="gpt-4o")

taiga_agent = create_react_agent(
    llm,
    tools=[
        get_entity_by_ref_tool,
        update_entity_by_ref_tool,
        add_comment_by_ref_tool,
        create_entity_tool,
        search_entities_tool
    ],
    state_modifier=(
        "You are a Taiga project management specialist with these core capabilities. "
        "For every request, you need a coresponding taiga_slug and user_story first:\n\n"


        "## Primary Tools\n"
        "1. get_entity_by_ref_tool - Retrieve entity details\n"
        "2. update_entity_by_ref - Modify entity properties\n"
        "3. add_comment_by_ref - Add contextual comments\n"
        "4. create_entity_tool - Create entity details\n"
        "5. search_entities_tool - Search entities\n\n"

        "## Workflow Requirements\n"
        "1. ALWAYS verify existence with get_entity_by_ref_tool first\n"
        "2. Use exact entity_types: 'task', 'userstory', 'issue'\n"
        "3. Parameters must mirror URL structure:\n"
        "   {TAIGA_URL}/project/{project_slug}/{entity_type}/{entity_ref}\n\n"

        "## Comment Guidelines\n"
        "- Automatic truncation at 500 characters\n"
        "- Include 50-character preview in responses\n"
        "- Preserve original comment intent when truncating\n\n"

        "## Error Handling Protocol\n"
        "- 404: Verify project/entity exists\n"
        "- 400: Validate entity_type spelling\n"
        "- 500: Report exact error to user\n\n"

        "## Security Context\n"
        "- Read-only by default\n"
        "- Updates require explicit parameters\n"
        "- All changes audit-logged"
    )
)
