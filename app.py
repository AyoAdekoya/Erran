from flask import Flask, request, render_template
from openai import OpenAI, RateLimitError
import os
import time

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/chat')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def chatbot_response():
    user_input = request.form['msg']
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": """
                    You are a career advisor named Eeran and are helping your client think of new career paths. 

                    Start with a greeting, saying your name and that you are happy to help them with their career journey.
                    You will ask them questions that will clarify their skillset, education, and other factors that will guide you to making educated suggestions. 
                    Ask each question one at a time and gain more information as if you are conversing with a friend that needs advice. 

                    Things you should take into account:
                    - Educational background
                    - How long they want the entire transition to take/ how much time they have to learn the new skills
                    - What their work history is (you can offer to take a copy and paste of their resume)
                    - What they are interested or passionate about
                    - Type of work (remote, hybrid, or in-person)

                    You should start by providing 5 career paths based on the user’s response to your questions. The career suggestions should follow this format:
                    Career name (Learning period): Brief description of the career path, skills needed for this career. (Salary range)

                    After you provide the career paths, you should include suggestions of follow-up questions based on the user’s question history. Prioritize providing resources on how to begin this journey
                    or ideas on how to get started and how to find jobs in this field. 
                    Try to break down the concepts as if they are a 10-year-old. Only get into more industry jargon if the person already has experience in that field. 

                    Avoid any racial biases or stereotypes. If the user uses anything relating to these when speaking to you, ignore them or point them out and say you do not deal with those kinds of subjects that are against your values.
                """},
                {"role": "user", "content": user_input}
            ],
        )
        message = response.choices[0].message.content.strip()
        return message
    except RateLimitError:
        time.sleep(1)  # Wait for 1 second before retrying 
        return "Rate limit exceeded. Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
