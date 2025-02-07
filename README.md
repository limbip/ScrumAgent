# Scrum Agent

![Shikenso Logo](https://shikenso.com/assets2/img/ShikensoAnalytics_Thumbnail.png)

<div align="center">
  <a href="https://shikenso.com/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://img.shields.io/badge/Homepage-Shikenso-blue" />
  </a>
  <a href="https://de.linkedin.com/company/shikenso-gmbh" target="_blank" style="margin: 2px;">
    <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Shikenso-7289da?logo=linkedin&logoColor=white&color=7289da" />
  </a>
  <a href="./LICENSE" target="_blank" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-GPL-f5de53?&color=f5de53" />
  </a>
</div>

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
    - [Discord Management](#discord-management)
    - [Taiga Scrum Master](#taiga-scrum-master)
    - [Web Tools](#web-tools)
    - [DeepSeek Reasoning](#deepseek-reasoning)
3. [Installation and Setup](#installation-and-setup)
    - [Python Project Setup](#python-project-setup)
    - [Discord Bot Setup](#discord-bot-setup)
    - [Environment Variables](#environment-variables)
4. [System Architecture](#system-architecture)
    - [Overview](#architecture-overview)
    - [Adding Agents and Tools](#adding-agents-and-tools)
5. [Tracing with LangSmith](#tracing-with-langsmith)
6. [Planned Features](#planned-features)
7. [Contact](#contact)

---

## 1. Introduction

**Scrum Agent** is an open-source, AI-powered supervisor designed to enhance agile project management within Discord communities. Acting as a virtual Scrum Master, this agent integrates multiple tools to streamline sprint planning, issue tracking, research, and team collaboration.

By mapping individual Discord channels to corresponding Taiga projects, Scrum Agent facilitates seamless user story management through threaded discussions—ensuring efficient workflow management and improved project oversight.

---

## 2. Features

Scrum Agent offers a range of capabilities to support agile project management:

### Discord Management

- **Seamless Integration:**  
  Acts as a central hub for project updates and agile workflow discussions.
  
- **Automated Task Tracking:**  
  Retrieves and organizes sprint-related messages to ensure no detail is overlooked.
  
- **Efficient Search & Retrieval:**  
  Enables quick access to relevant messages, posts, and threads.
  
- **Channel and Thread Organization:**  
  Provides a structured list of channels and active threads for easy navigation.

### Taiga Scrum Master

- **Issue Management:**  
  Track and update sprints, user stories, and tasks efficiently.
  
- **User Story Details:**  
  Retrieve comprehensive information, including history and assigned users.
  
- **Task Updates:**  
  Modify descriptions, update statuses, and assign watchers as needed.
  
- **User Story Creation:**  
  Enhance team collaboration by creating new user stories directly.

### Web Tools

- **DuckDuckGo:**  
  Perform efficient web searches.
  
- **ArXiv:**  
  Access a wide range of research papers.
  
- **YouTube & Wikipedia:**  
  Retrieve information quickly for research or reference.
  
- **Web Navigation:**  
  Gather additional context and relevant data.

### DeepSeek Reasoning

- **Advanced Problem-Solving:**  
  Leverage AI-driven insights to address complex challenges.
  
- **Strategic Analysis:**  
  Enhance decision-making with robust analytical tools.
  
- **Abstract Reasoning:**  
  Gain predictive insights and better understand abstract concepts.

---

## 3. Installation and Setup

### Python Project Setup

1. **Create and activate a Conda environment:**

   ```bash
   conda create -n scrumagent python=3.11 -y
   conda activate scrumagent
   ```

2. **Upgrade pip and install dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Install Ollama for DeepSeek Agent:**

   Download and install [Ollama](https://ollama.com/download) (adjust size as needed):

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull deepseek-r1:8b
   ```

### Discord Bot Setup

#### 1. Create Your Discord Bot
- **Access the Developer Portal:**  
  Visit the [Discord Developer Portal](https://discord.com/developers/applications) and sign in with your Discord account.
- **Create a New Application:**  
  Click **"New Application"**, give your bot a name, and create the application.

#### 2. Configure OAuth2 Settings
- **Navigate to the OAuth2 Tab:**  
  Once your application is created, click on the **OAuth2** tab.
- **Enable the Bot Option:**  
  In the OAuth2 settings, activate the **"bot"** option.
- **Set Bot Permissions:**  
  Under the **OAuth2 Bot Permissions** section, ensure that the following permissions are enabled:
  - **View Channels**
  - **Send Messages**
  - **Create Public Threads**
  - **Create Private Threads**
  - **Send Messages in Threads**
  - **Read Message History**
  - **Add Reactions**

#### 3. Add the Bot to Your Server
- **Generate the OAuth2 URL:**  
  After configuring the permissions, generate the OAuth2 URL.
- **Invite the Bot:**  
  Use the generated URL to invite the bot to your Discord server, and follow the on-screen instructions to complete the process.

### Environment Variables and Mapping

1. **Set Up Environment Variables:**
   - Copy the file `.env.example` and rename it to `.env`.
   - Open the new `.env` file and fill in the required details.

2. **Customize the Mapping:**
   - Copy `config/taiga_discord_maps.yaml.example` and rename it to `config/taiga_discord_maps.yaml`.
   - Edit this file as needed to match your project settings.
   
---

## 4. System Architecture

### Architecture Overview

Scrum Agent is built on the [Langgraphs Supervisor Agent](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/), which allows for flexible integration of multiple agents and tools. For more technical details, please refer to the Langgraphs documentation.

#### Architecture Diagram

![Multi-Agent Architecture](assets/multi_agent_graph.png)  
*Figure: Architecture diagram of Scrum Agent's multi-agent setup.*

### Adding Agents and Tools

- **Adding Agents:**  
  Insert new agent nodes in `build_agent_graph.py`.

- **Supervisor Configuration:**  
  Update `supervisor_agent.py` with the agent's name and description. Ensure that the names are consistent.

- **Tool Integration:**  
  Follow the [Langgraphs Documentation](https://python.langchain.com/docs/integrations/tools/) for guidance on adding and integrating additional tools.

---

## 5. Tracing with LangSmith

To enable tracing with LangSmith, follow these steps:

1. **Set Environment Variables:**
   - Add the following to your `.env` file:
     ```bash
     LANGCHAIN_TRACING_V2=True
     LANGCHAIN_API_KEY=your_api_key_here
     ```
   - Replace `your_api_key_here` with your actual API key (refer to `.env.example` for guidance).

2. **Learn More:**
   - [Tracing Documentation](https://docs.smith.langchain.com/observability/how_to_guides/tracing/trace_with_langgraph)
   - [LangSmith Website](https://smith.langchain.com/)

This configuration allows you to monitor and trace your application's activity using LangSmith.
---

## 6. Planned Features

- **Enhanced Long-Term Memory:**  
  Integration of searchable long-term memory for specific agents.  
  References:
  - [Memory Agent Repository](https://github.com/langchain-ai/memory-agent)
  - [Long Term Memory Documentation](https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/)
  
- **Multi-Server Support:**  
  Expanding bot capabilities to support multiple Discord servers (currently limited to one).

---

## 7. Contact

For inquiries, support, or contributions, please open an issue or contact us at .

---