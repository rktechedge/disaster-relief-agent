# Disaster Relief Information Assistant

A Multi-Agent AI System (Planner → Worker → Evaluator) that provides verified
safety instructions and helpline information for disasters (flood, earthquake,
cyclone, fire). This repo is prepared for the Kaggle 'Agents for Good' track.

## Quick start

1. Install requirements:

```
pip install -r project/requirements.txt
```

2. Run demo:

```
python project/run_demo.py
```

3. Quick test in Python:

```python
from project.main_agent import run_agent
print(run_agent("There is flooding in New York"))
```

## Structure

See `project/` directory for agents, tools, data, and core modules.

## Deploy

Use `project/app.py` as a minimal entrypoint for deployment to Hugging Face Spaces
by wrapping it in a Gradio or FastAPI app.

## License

This project is provided under the MIT License. See LICENSE.txt.
