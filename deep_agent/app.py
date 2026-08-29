from config import Config
from agent.supervisor import Supervisor

def main():
    config = Config()
    supervisor = Supervisor(config)
    print(f"Welcome to {config.AGENT_NAME}")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in config.EXIT_COMMANDS:
            print("Goodbye!")
            break
        response = supervisor.handle(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()

