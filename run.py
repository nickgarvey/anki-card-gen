import asyncio
import click
import csv
import io
from anki_generator import AnkiOpenAIClient, Cards


def cards_to_csv(cards: Cards, file: io.IOBase):
    writer = csv.writer(file, delimiter=";")
    for card in cards.cards:
        writer.writerow([card.question, card.answer])


async def main_async(prompt: str, output_file: io.TextIOBase):
    with open("secrets/openai_api_key.txt", "r") as f:
        api_key = f.read().strip()
    client = AnkiOpenAIClient(api_key)
    cards = await client.gen_questions_and_answers(prompt)
    cards_to_csv(cards, output_file)


@click.command()
@click.option(
    "-p",
    "--prompt",
    help="The prompt to generate questions and answers for.",
    prompt=True,
)
@click.option(
    "-o",
    "--output-file",
    help="Output file. Defaults to stdout",
    type=click.File("w"),
    default="-",
)
def main(prompt: str, output_file: io.TextIOBase):
    asyncio.run(main_async(prompt, output_file))


if __name__ == "__main__":
    main()
