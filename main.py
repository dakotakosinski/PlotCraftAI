from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)
openai_api_key = os.environ.get("openaiApiKey")
assistant_id = "asst_Ujp73GXjXTV2JgzqrCXDqdKW"
client = OpenAI(api_key='')
plotCraftAI = client.beta.assistants.retrieve(assistant_id)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/story_form')
def story_form():
    return render_template('story_form.html')

@app.route('/madlibs_form')
def madlibs_form():
    return render_template('madlibs_form.html')

@app.route("/generate_story", methods=["POST"])
def generate_story():
    prompt = request.form.get('prompt')
    word_cap = request.form.get('word_cap')
    genre = request.form.get('genre')
    protagonist = request.form.get('protagonist')
    brainrot = request.form.get('brainrot')

    my_thread = client.beta.threads.create()
    my_message = client.beta.threads.messages.create(
        thread_id=my_thread.id,
        role='user',
        content=f"the prompt: {prompt} the protagonist: {protagonist}, the: {genre} the word cap: {word_cap}, Brainrot Mode: {brainrot}"
    )
    my_run = client.beta.threads.runs.create(
        thread_id=my_thread.id,
        assistant_id=plotCraftAI.id
    )
    while my_run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )
        if keep_retrieving_run.status in ['queued', 'in_progress']:
            continue
        else:
            print(f"Run Status: {keep_retrieving_run.status}")
            break

    if keep_retrieving_run.status == "completed":
        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread.id
        )
        response = all_messages.data[0].content[0].text.value
        return render_template('story_result.html', story=response.strip())
    return "Story generation failed."

@app.route('/generate_madlibs', methods=['POST'])
def generate_madlibs():
    genre = request.form.get('genre')
    my_thread = client.beta.threads.create()
    my_message = client.beta.threads.messages.create(
        thread_id=my_thread.id,
        role='user',
        content=f"the Genere for the Madlib is {genre}"
    )
    my_run = client.beta.threads.runs.create(
        thread_id=my_thread.id,
        assistant_id=plotCraftAI.id
    )
    while my_run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )
        if keep_retrieving_run.status in ['queued', 'in_progress']:
            continue
        else:
            print(f"Run Status: {keep_retrieving_run.status}")
            break

    if keep_retrieving_run.status == "completed":
        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread.id
        )
        response = all_messages.data[0].content[0].text.value
        return render_template('madlibs_story.html', story=response.strip())
    return "Story generation failed."


if __name__ == '__main__':
    app.run(debug=True)
