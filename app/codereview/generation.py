# Import required libraries
import os
from groq import Groq

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "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"

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



# g = generate("""
# class SignUp(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField(max_length=200)
#     password = models.CharField(max_length=100)
#     ROLE_CHOICES = [
#         ("I'm a Student", 'Student'),
#         ("I'm a Teacher", 'Teacher'),
#         ("I'm a Proffesional", 'Proffesional'),
#     ]
#     role = models.CharField(max_length=255, choices=ROLE_CHOICES, null=True, blank=True)

#     def __str__(self):
#         return self.name
# """)
# print(g[0])
# print()
# print()
# print(g[1])
# print()
# print()
# print(g[2])