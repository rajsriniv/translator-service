import openai
import os

api_key = os.environ('OPENAI_APIKEY')

def translate_text(text, source_lang, target_lang):
    client = openai.OpenAI(api_key=api_key)
    model_prompt = f"Translate the following {source_lang} text to fluent {target_lang}"
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": model_prompt},
        {"role": "user", "content": text}
    ]
    )
    #print(response["choices"][0]["message"]["content"])
    return response.choices[0].message.content
