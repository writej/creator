import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
#api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def generateCopyTitle(prompt1):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            #{"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            #{"role": "user", "content": "Generate copy title on: {}.".format(prompt1)}
            {"role": "user", "content": "Generate attention-grabbing headline for: {}.".format(prompt1)}
      ]

    )
    return response.choices[0].message.content


def generateCopyText(prompt2):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
          #{"role": "user", "content": "Generate copy title on: {}.".format(prompt2)}
          {"role": "user", "content": "As a copywriter adept at crafting product page copy that turns prospects into customers, please help me construct an engaging copy for: {}. This should include a brief product description, and a list of 7 bullet points highlighting the key features or benefits. The overall objective is to present my product in a way to make a purchase. It must have the form of a promotional copy of up to 150 words.".format(prompt2)}
      ]
    )
    return response.choices[0].message.content