from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

my_endpoint = "https://clinicexpert.services.ai.azure.com/api/projects/cliniexpert"

project_client = AIProjectClient(
    endpoint=my_endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "Agent457CliniExpert"
my_version = "2"

openai_client = project_client.get_openai_client()

def chat():
    print("Chat with your agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            response = openai_client.responses.create(
                input=[{"role": "user", "content": user_input}],
                extra_body={
                    "agent_reference": {
                        "name": my_agent,
                        "version": my_version,
                        "type": "agent_reference",
                    }
                },
            )

            print("Agent:", response.output_text)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    chat()