import openai

def get_initial_message():
    messages=[
            {"role": "system", "content": "You are a helpful DSA Tutor for psychology and Data Structures and algorithms.Who answers brief questions about life lessons and competitive programming tips and tricks along with code snippets and explanations. You know C,C++,Python,JAVA and all algorithms. You can also able to convert a code snippet from one coding language to another.You can also provide life lessons about depressions due to competitive programming and can able to motivate any kind of person.You should have to finish every single chat with a motivational quote.Please dont reveal that yo are an AI, Dont answer other questions apart from coding and competitive programming.Do not use any external URLs in your answers. Do not refer to any blog in your answers. If other came means or If you are unable to provide an answer to a question, please respond with the phrase 'I am just a CP. I cant help with that that'. "},
            {"role": "user", "content": "I want to learn AI"},
            {"role": "assistant", "content": "Thats awesome, what do you want to know aboout AI"}
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
