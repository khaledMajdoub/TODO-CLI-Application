import click


@click.group()
def mycommand():
    pass


@click.command()
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(name):
    click.echo(f"Hello {name}!")


PRIORITIES = {
    "o": "optional",
    "l": "low",
    "n": "normal",
    "h": "high",
}


@click.command()
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="n")
@click.argument("todofile", type=click.Path(exists=False), required=False)
@click.option("-n", "--name", prompt="Your name")
@click.option("-d", "--description", prompt="description", help="The person to greet.")
def add_todo(name, description, priority, todofile):
    filename = todofile if todofile is not None else "todo.txt"
    with open(filename, "a") as f:
        f.write(f"{name}: {description} [priority: {PRIORITIES[priority]}")


@click.command()
@click.argument("idx", type=int, required=1)
def delete_todo(idx):
    with open("todo.txt", "r") as f:
        todo_list = f.read().splitlines()
        todo_list.pop(idx)
    with open("todo.txt", "w") as f:
        f.write("\n".join(todo_list))
        f.write("\n")


@click.command()
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), default="n")
@click.argument("todofile", type=click.Path(exists=True), required=False)
def list_todos(priority, todofile):
    filename = todofile if todofile is not None else "todo.txt"
    with open(filename, "r") as f:
        todo_list = f.read().splitlines()
    if priority is None:
        for idx, todo in enumerate(todo_list):
            print(f"{idx} - {todo}")
    else:
        for idx, todo in enumerate(todo_list):
            if f"[priority: {PRIORITIES[priority]}" in todo:
                print(f"{idx} - {todo}")


mycommand.add_command(hello)
mycommand.add_command(add_todo)
mycommand.add_command(delete_todo)
mycommand.add_command(list_todos)


if __name__ == "__main__":
    mycommand()
