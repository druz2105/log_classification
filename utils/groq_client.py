from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq()


def get_groq_client(prompt):
    return groq_client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
    )
