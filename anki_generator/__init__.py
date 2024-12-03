import openai
from pydantic import BaseModel

SYSTEM_MESSAGE = """
    You generate Anki Cards for self study.
    The cards all have a question and an answer.

    Both fields, the question and answer, can use basic HTML. Use it
    to format your answers.

    Generate 20 cards per query.

    Make sure previous Q&A don't implicitly depend on previous Q&A.

    e.g. this is wrong, because the second answer implicitly assumes a binary heap when there was none:

    Which <b>traversal method</b> does a binary heap rely on?
    A binary heap does not rely on traditional tree traversal methods like in-order, pre-order, or post-order traversal. Instead, it maintains the heap property regardless of the specific order of traversal.

    What is the <b>height of a heap</b> with <em>n</em> elements?
    The <b>height of a heap</b> with <em>n</em> elements is <code>O(log n)</code> because it is a complete binary tree, and its height is logarithmic to the number of nodes.

"""

class CardFields(BaseModel):
    question: str
    answer: str

class Cards(BaseModel):
    cards: list[CardFields]


class AnkiOpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = openai.Client(api_key=api_key)

    async def gen_questions_and_answers(self, prompt: str) -> Cards:
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
            response_format=Cards,
        )
        return response.choices[0].message.parsed
