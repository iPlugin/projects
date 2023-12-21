import os

import openai
from dotenv import load_dotenv


print("\nTo begin with, be sure that the python file is in the folder together\n"
    "with the text.txt file. Which you should create and copy your text there.\n"
    "And create .env file where i need to write \"OPENAI_KEY=...\"\n"
    "from https://platform.openai.com/\n")
print("\n\tWhat go you want to do with this text?")
need = str(input(">>> "))


# Settings
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


with open("text.txt", "r") as file:
    text = file.read()

format_text = text.split(": ")
sentences = format_text[-1].split(". ")

new_text = ""
for sentence in sentences:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"{sentence}: {need}",
            },
        ],
    )
    result = completion.choices[0].message.content

    if not result.endswith("."):
        result = result + ". "
    else:
        new_text += completion.choices[0].message.content + " "


with open("new_text.txt", "w") as file:
    file.write(new_text)

print("\n\tYour text is ready! Go to the file \"new_text.txt\"\n")

# print(f"\n{new_text}")