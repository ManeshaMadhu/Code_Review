# Import required libraries
import os
from groq import Groq

# Set your Groq API key
os.environ["GROQ_API_KEY"] = KEY

# Initialize Groq client
import re

def generate(code_text):
    client = Groq()
    responses = []
    prompts = [
        f"Provide a concise, 3-4 word description for the following code:\n{code_text}",
        f"Find errors in the following code and explain:\n{code_text}",
        f"Enhance the following code to make it more robust and readable:\n{code_text}",
        f"Optimize the following code for performance and clarity:\n{code_text}"
    ]

    for index, i in enumerate(prompts):
        if i.strip():
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": i}],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )

            response_content = ""
            for chunk in completion:
                response_content += chunk.choices[0].delta.content or ""

            response_text = response_content.strip()

            if index == 0:
                # Extract content inside quotes using regex
                match = re.search(r'\"(.+?)\"', response_text)
                code_name = match.group(1).strip() if match else response_text
                responses.append(code_name)
            else:
                responses.append(response_text)

    return responses

