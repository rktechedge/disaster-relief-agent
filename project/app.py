def create_app():
    from project.main_agent import run_agent
    return lambda x: run_agent(x)

if __name__ == "__main__":
    print(create_app()("Test input from app.py"))
