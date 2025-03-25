# Workshop IA #1

## 📚 Table of Contents

- [Workshop IA #1](#workshop-ia-1)
  - [📚 Table of Contents](#-table-of-contents)
  - [📝 Description](#-description)
  - [🌟 Features](#-features)
  - [🛠️ Technologies](#️-technologies)
  - [🚀 Installation](#-installation)
  - [▶️ Usage](#️-usage)
  - [👩‍💻 Development](#-development)
  - [License](#license)

---

## 📝 Description

**Workshop IA #1** is a project by **Brest Social Engines (BSE)** that provides resources for an introductory workshop on AI engineering. The project demonstrates how to build a basic conversational agent using LangGraph and LangChain, and serves as a foundation for understanding more complex AI systems.

---

## 🌟 Features

- Simple conversational agent using LangGraph
- Interactive Jupyter notebook for testing
- Streaming API integration for real-time responses
- Foundational concepts of graph-based AI workflows

---

## 🛠️ Technologies

- **Language**: Python 3.11
- **Frameworks**: LangChain & LangGraph
- **Models**: OpenAI / Azure OpenaI GPT models
- **Development Tools**: Jupyter Notebooks
- **Dependency Management**: Poetry
- **Environment**: API keys configured in a `.env` file

---

## 🚀 Installation

To install and configure Workshop IA #1 locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/BSE-dev/workshop-ia-1.git
    cd workshop-ia-1
    ```

2. Install the dependencies with Poetry:
    ```bash
    poetry install --no-root --with dev
    ```

3. Configure the API keys:
    - Copy the `.env.template` file to `.env` in the project root:
      ```bash
      cp .env.template .env
      ```
    - Add your API keys to the `.env` file (you can use either OpenAI or Azure OpenAI):
      ```
      OPENAI_API_KEY=your_openai_api_key_here
      # Or for Azure OpenAI:
      AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
      AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
      ```

---

## ▶️ Usage

To use the workshop resources, follow these steps:

1. Use one terminal to run the LangGraph server locally:
    ```bash
    poetry run langgraph dev
    ```

2. Open the langgraph_demo notebook using the Jupyter VS Code extension, and connect
   Poetry kernel

3. Alternatively, you can run it in Jupyter by activating the Poetry environment:
    ```bash
    poetry shell
    ```
    
    Then adding the environnement to Jupyter:
    ```bash
    poetry env list
    # note the venv name and use it in:
    python -m ipykernel install --user --name=poetry_venv_name --display-name "Python (workshop-ia-1-env)"
    ```

    And running the notebook:
    ```bash
    jupyter notebook langgraph_demo.ipynb
    ```

4. Execute the cells in the notebook to interact with the conversational agent.

---

## 👩‍💻 Development

For developers wishing to extend or modify the workshop materials:

1. The project structure is simple:
   - `conv_agent.py`: Contains the definition of the conversational agent
   - `langgraph_demo.ipynb`: Jupyter notebook for testing the agent
   - `pyproject.toml`: Project dependencies and configuration

2. To modify the agent's behavior, edit the system prompt in `conv_agent.py`

3. To test your changes, run the Jupyter notebook and interact with the agent
   
4. You may run LangGraph Server in debug mode to attach a debugger to it:
    ```bash
    poetry run langgraph dev --debug-port 5678
    ```

5. If you are using VS Code as an IDE, you may then attach its debugger to your
   Graph using the launcher in .vscode/launch.json

6. You may want to define a LangSmith API key in your .env file if you want to use
   LangSmith for tracing/debugging, or LangGraph Studio for agent debugging:
    ```
    LANGSMITH_API_KEY=your_langsmith_api_key_here
    LANGSMITH_TRACING=true
    LANGSMITH_PROJECT=your_langsmith_project
    ```

---

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
