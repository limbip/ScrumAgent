# Scrum Agent


![Shikenso Logo](https://shikenso.com/assets2/img/ShikensoAnalytics_Thumbnail.png)

<hr>
<div align="center" style="line-height: 1;">
  <a href="https://shikenso.com/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://img.shields.io/badge/Homepage-Shikenso-blue" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://de.linkedin.com/company/shikenso-gmbh" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/LinkedIn-Shikenso-7289da?logo=linkedin&logoColor=white&color=7289da" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="./LICENSE" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-GPL-f5de53?&color=f5de53" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>


## 1. Introduction

The **Scrum Agent** is an open-source AI-powered supervisor agent designed to facilitate agile project management within Discord communities. 
Acting as a virtual Scrum Master, this agent integrates multiple tools to streamline sprint planning, issue tracking, research, and collaboration.

This project enables teams to manage their workflow efficiently using Discord as the primary communication platform while seamlessly interacting with external services like Taiga, web search engines, and more. 
Every Discord channel can be mapped to a different Taiga project, and user stories are handled as threads in the Discord channel.



## 2. Features 🚀  

- **⚡ Agile Workflow Automation**: Manage sprint planning 🏁 and issue tracking ❗ directly within Discord.  
- **📂 Message & Channel Organization**: Retrieve historical messages 🏛️, search relevant threads 🧵, and keep track of discussions.  
- **📚 Knowledge Retrieval**: Gather external research 📜 and insights ℹ️ to support decision-making.  
- **🤖 AI-Powered Decision Making**: Utilize AI-driven analysis to break down and solve complex problems collaboratively.  

### 2.1. Discord Management 🗨️  
- **🔗 Seamless Integration**: Acts as a central hub 🏠 for project updates 🔄 and agile workflow discussions.  
- **📩 Automated Task Tracking**: Retrieves and organizes messages related to sprints 🏁, ensuring nothing gets lost.  
- **🔍 Search & Retrieval**: Quickly find relevant messages 📨, posts 📝, and discussions within Discord.  
- **🧭 Channel and Thread Organization**: Lists all channels 📋 and active threads 🧵, making navigation intuitive.  

### 2.2. Taiga Scrum Master 📖  
- **❗ Issue Management**: Track and update sprints 🏁, user stories 📜, and tasks 📋.  
- **📜 User Story Retrieval**: Retrieve detailed information ℹ️, including history and assigned users 👤.  
- **📝 Task Updates**: Modify descriptions, change statuses 🔄, and assign watchers 👀.  
- **✨ Create New User Stories** to enhance team collaboration.  

### 2.3. Web Tools 🌐  
- **🦆🔎 DuckDuckGo** for efficient web searches.  
- **📚 ArXiv** for accessing research papers.  
- **▶️ YouTube & 📖 Wikipedia** for quick information retrieval.  
- **🌍 Web Navigation** to gather additional context.  

### 2.4. [DeepSeek](https://www.deepseek.com/) Reasoning 🧠  
- **🚀 Advanced Problem-Solving** to assist in complex challenges.  
- **🎯 Strategic Analysis** to enhance decision-making.  
- **💭 Abstract Reasoning** for better insights and predictions.  



## 3. Installation and Setup
### 3.1. Python project
 ```bash
# Create conda env
conda create -n autobotcentral python=3.11 -y
conda activate autobotcentral
pip install pip -U
pip install -r requirements.txt 

# Install ollama for deepseeker-agent. Adjust size as needed
# https://ollama.com/download
curl -fsSL https://ollama.com/install.sh | sh
ollama pull deepseek-r1:8b 
```

### 3.2. Discord Bot
Create a Discord Bot and add it to your server. 
For more information, visit the [Discord Developer Portal](https://discord.com/developers/applications/).

### 3.3. Environment Variables
* Create a `.env` file based on the `.env.example` template and fill in the required values.
* Change `config/taiga_discord_maps.yaml` to your needs.



## 4. System
### 4.1. Architecture
The Agent Architecture is Based on Langgraphs Supivisor Agent. For more information, please visit the [Langgraphs Documentation](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/).

### 4.2. Adding Agents and Tools
* Add Agent Node to build_agent_graph.py
* Add Agent Name and description to supervisor_agent.py -> members (names of agents should match)
* For Tools, please refer to the [Langgraphs Documentation](https://python.langchain.com/docs/integrations/tools/) for adding new agents and tools.



## 5. Tracing with LangSmith
* set `LANGCHAIN_TRACING_V2=True` and `LANGCHAIN_API_KEY` (see `.env.example`)
* [Documentation](https://docs.smith.langchain.com/observability/how_to_guides/tracing/trace_with_langgraph)
* [LangSmith](https://smith.langchain.com/)

## 6. Planned Features
* Add Searchable Long Time Memory for specific agents
  * https://github.com/langchain-ai/memory-agent
  * https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/
* Support multiple Discord Server for one bot (currently only one server is supported)




## 7. Contact
If you have any questions, please raise an issue or contact us at [....](....).