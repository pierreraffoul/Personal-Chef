from config import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from system_prompt import systemprompt

load_dotenv()

model = init_chat_model(
    model="deepseek-v4.1-flash-1017",
    model_provider="openrouter",
)

agent = create_agent(
    model=model,
    system_prompt=systemprompt
)





def main():
    print("Hello worlds !")


if __name__ == "__main__":
    main()
