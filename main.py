from flask import Flask
from openai import OpenAI
import os

app = Flask(__name__)
openai_api_key = os.environ.get("openaiApiKey")
assistant_id = "asst_Ujp73GXjXTV2JgzqrCXDqdKW"
client = OpenAI(api_key='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')
plotCraftAI = client.beta.assistants.retrieve(assistant_id)


@app.route("/Story/<prompt>/<word_cap>/<genre>")
def generate_story(prompt, word_cap, genre):
    my_thread = client.beta.threads.create()
    my_message = client.beta.threads.messages.create(
        thread_id= my_thread.id,
        role= 'user',
        content= prompt + genre + word_cap
    )
    my_run = client.beta.threads.runs.create(
        thread_id= my_thread.id,
        assistant_id= plotCraftAI.id
    )
    while my_run.status == "queued" or  my_run.status == "in_progress":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id= my_thread.id,
            run_id= my_run.id
        )
        if keep_retrieving_run.status in ['queued', 'in_progress']:
            pass
        else:
            print(f"Run Status: {keep_retrieving_run.status}")
            break
    
    if keep_retrieving_run.status == "completed":
        print("\n")

        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread.id
        )
        print(f"Assistant: {all_messages.data[0].content[0].text.value}")
        response = all_messages.data[0].content[0].text.value
        resp = response.strip()
        return resp
    return "failed"




if __name__ == '__main__':
    app.run(debug=True)