from flask import Flask, render_template, request, session, redirect, url_for
import os
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session key

openai_api_key = os.environ.get("openaiApiKey")
client = OpenAI(api_key='')
assistant_id = "asst_Ujp73GXjXTV2JgzqrCXDqdKW"
plotCraftAI = client.beta.assistants.retrieve(assistant_id)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/madlibs_form')
def madlibs_form():
    return render_template('madlibs_form.html')

@app.route('/generate_madlibs', methods=['POST'])
def generate_madlibs():
    genre = request.form.get('genre')
    my_thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=my_thread.id,
        role='user',
        content=f"The genre for the Madlib is {genre}"
    )
    my_run = client.beta.threads.runs.create(
        thread_id=my_thread.id,
        assistant_id=plotCraftAI.id
    )

    while my_run.status in ["queued", "in_progress"]:
        my_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )

    if my_run.status == "completed":
        all_messages = client.beta.threads.messages.list(thread_id=my_thread.id)
        response = all_messages.data[-1].content[0].text.value
        # Replace placeholders with HTML span tags for user input
        response = response.replace("____", "<span class='blank'>____</span>")
        session['story_template'] = response
        return redirect(url_for('fill_madlibs'))
    return "Story generation failed."

@app.route('/fill_madlibs', methods=['GET', 'POST'])
def fill_madlibs():
    if request.method == 'POST':
        filled_story = request.form['filled_story']
        return render_template('madlibs_result.html', story=filled_story)
    return render_template('madlibs_story.html', story=session.get('story_template'))

@app.route('/submit_madlibs', methods=['POST'])
def submit_madlibs():
    filled_story = request.json.get('filled_story')
    return jsonify(success=True, story=filled_story)

if __name__ == '__main__':
    app.run(debug=True)
