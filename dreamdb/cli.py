from datetime import datetime
from pathlib import Path

import typer
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from dreamdb.db import Dream, db


def res_cb(res: any) -> None:
    db.close()


app = typer.Typer(result_callback=res_cb)


@app.callback()
def cb() -> None:
    db.connect()


@app.command()
def setup() -> None:
    db.create_tables([Dream])


@app.command()
def add(filename: Path) -> None:
    with open(filename, "r") as f:
        data = f.read()
        f.close()
    data = data.split("\n")

    rating = int(data[0].strip())
    desc = data[1].strip()
    date = datetime.today()

    dream = Dream(rating=rating, desc=desc, date=date)
    dream.save()


@app.command()
def remove(id: int) -> None:
    dream: Dream = Dream.get(Dream.id == id)
    dream.delete_instance()


@app.command()
def list() -> None:
    table = Table("ID", "Date", "Rating", "Description", title="Dreams")

    for dream in Dream.select():
        table.add_row(
            str(dream.id),
            dream.date.strftime("%d/%m/%Y"),
            str(dream.rating),
            dream.desc,
        )
    print(table)


@app.command()
def read(id: int) -> None:
    dream: Dream = Dream.get(Dream.id == id)
    print(
        Panel(
            "Date   : "
            + dream.date.strftime("%d/%m/%Y")
            + "\nRating : "
            + str(dream.rating),
            title="Info",
        )
    )
    print(Panel(Markdown(dream.desc), title="Description"))
