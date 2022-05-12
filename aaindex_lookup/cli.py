import sys
import click
import json

from aaindex_lookup.scrape import scrape_parse


@click.command()
@click.argument("database_number", type=int)
@click.option("--pretty/--no-pretty", default=True)
def main(database_number: int, pretty: bool):
    result = scrape_parse(index=database_number, progress=True)
    indent = 4 if pretty else None
    json.dump(result, sys.stdout, indent=indent, default=lambda obj: obj.dict())
