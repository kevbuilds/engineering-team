# Engineering Team - AI-Powered Software Development Crew

An autonomous AI engineering team built with [CrewAI](https://crewai.com) that designs, develops, tests, and delivers complete software applications. Watch as AI agents collaborate like a real software development team!

## 🎯 What This Does

This project demonstrates a multi-agent AI system that works together to build software applications from requirements. The team includes:

- **Engineering Lead** - Creates detailed technical designs from requirements
- **Backend Engineer** - Implements Python modules based on the design
- **Frontend Engineer** - Builds Gradio UIs to demonstrate the functionality
- **Test Engineer** - Writes comprehensive unit tests

The agents work sequentially, each building on the previous agent's work, to deliver a complete, tested application with a working UI.

## 🚀 Demo Output

The example included builds a **Trading Account Management System** with:
- Account creation and management
- Deposit/withdrawal functionality  
- Stock trading (buy/sell shares for AAPL, TSLA, GOOGL)
- Portfolio tracking with profit/loss calculations
- Transaction history
- Interactive Gradio web interface

All generated files are in the `output/` directory:
- `accounts.py` - Complete backend implementation
- `app.py` - Gradio UI application
- `test_accounts.py` - Unit tests
- `accounts.py_design.md` - Technical design document

## 📋 Prerequisites

- Python >=3.10 <3.13
- OpenAI API key
- [UV](https://docs.astral.sh/uv/) package manager (optional but recommended)

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/kevbuilds/engineering-team.git
cd engineering-team
```

2. **Install UV (optional)**
```bash
pip install uv
```

3. **Install dependencies**
```bash
# Using UV
crewai install

# Or using pip
pip install crewai crewai-tools gradio
```

4. **Set up your API key**

Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎮 Usage

### Run the Engineering Team

```bash
# Using CrewAI CLI
crewai run

# Or run directly with Python
cd /path/to/engineering-team
source /path/to/venv/bin/activate
PYTHONPATH=src:$PYTHONPATH python -m engineering_team.main
```

The team will work through four sequential tasks:
1. 📐 **Design** - Engineering lead creates technical design
2. 💻 **Backend** - Backend engineer writes the code
3. 🎨 **Frontend** - Frontend engineer builds the UI
4. ✅ **Testing** - Test engineer creates unit tests

### Run the Generated Application

After the crew completes, run the generated Gradio app:

```bash
cd output
python app.py
```

Then open http://127.0.0.1:7860 in your browser to interact with the application!

## 📁 Project Structure

```
engineering-team/
├── src/
│   └── engineering_team/
│       ├── config/
│       │   ├── agents.yaml      # Agent definitions
│       │   └── tasks.yaml       # Task definitions
│       ├── tools/               # Custom tools
│       ├── crew.py             # Crew configuration
│       └── main.py             # Entry point
├── output/                     # Generated files
├── knowledge/                  # Agent knowledge base
├── .gitignore
├── pyproject.toml
└── README.md
```

## ⚙️ Customization

### Modify Requirements

Edit `src/engineering_team/main.py` to change what the team builds:

```python
requirements = """
Your custom application requirements here...
"""
module_name = "your_module.py"
class_name = "YourMainClass"
```

### Configure Agents

Edit `src/engineering_team/config/agents.yaml` to customize agent roles, goals, and backstories.

### Adjust Tasks

Edit `src/engineering_team/config/tasks.yaml` to modify the workflow and outputs.

### Code Execution Settings

The crew is configured to work without Docker. If you have Docker installed and want safer code execution:

In `src/engineering_team/crew.py`, change:
```python
allow_code_execution=False
```
to:
```python
allow_code_execution=True
code_execution_mode="safe"  # Uses Docker
```

## 🎓 Learn More

- [CrewAI Documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [Join CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with [CrewAI](https://crewai.com) - enabling AI agents to work together as a crew.

---

**Note**: This is a demonstration project showing how AI agents can collaborate on software development tasks. The generated code should be reviewed and tested before production use.
