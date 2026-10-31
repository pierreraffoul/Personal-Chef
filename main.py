from config import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage

from system_prompt import systemprompt

from ipywidgets import FileUpload

load_dotenv()


agent = create_agent(
    model=init_chat_model(model="deepseek-v4.1-flash-1017", model_provider="openrouter",),
    system_prompt=systemprompt,
    checkpointer=InMemorySaver(),
)





def main():
    """ Logique métier """

    while True:

        config = {"configurable" : {"thread_id" : "conversation-1"}}

        input_user = input("Entrez un message : ")
        if input_user.lower() in ("quit", "exit", "q"):
            break
        

        response = agent.invoke(
            {"messages" : [HumanMessage(content = input_user)]},
            config=config
        )
        print(f"Chef : {response["messages"][-1].content}")






if __name__ == "__main__":
    main()
