# Simple command line TODO app
import datetime
from pathlib import Path

import click
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class TodoModel(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    done = Column(Boolean, nullable=False)


class Datastore:

    # Add a new todo item based on the individual fields.
    def add(self, description, due_date, done):
        with self.Session() as s:
            todo = TodoModel(description=description, due_date=due_date, done=done)
            s.add(todo)
            s.commit()
            return todo

    # Get all todo items, optionally filtered by done status.
    def get_all(self, done=None):
        with self.Session() as s:
            if done is None:
                return s.query(TodoModel).all()
            else:
                return s.query(TodoModel).filter(TodoModel.done == done).all()

    # Get a single todo item by ID.
    def get(self, id):
        with self.Session() as s:
            return s.query(TodoModel).filter(TodoModel.id == id).first()

    # Update a todo item by ID.
    def update(self, id, description=None, due_date=None, done=None):
        with self.Session() as s:
            todo = s.query(TodoModel).filter(TodoModel.id == id).first()
            todo.description = description or todo.description
            todo.due_date = due_date or todo.due_date
            if done is not None:
                todo.done = done
            s.commit()
            return todo

    # Delete a todo item by ID.
    def delete(self, id):
        with self.Session() as s:
            s.delete(s.query(TodoModel).filter(TodoModel.id == id).first())
            s.commit()

@click.group()
@click.pass_context
def console(ctx):
    ctx.obj = Datastore()

@console.command()
@click.option('--desc', prompt=True)
@click.option('--due', prompt=True, type=click.DateTime(), default=lambda: datetime.datetime.now() + datetime.timedelta(days=1))
@click.option('--done', default=False)
@click.pass_context
def add(ctx, desc, due, done):
    ctx.obj.add(desc, due, done)

@console.command()
@click.option('--done', default=None)
@click.pass_context
def listing(ctx, done):
    for todo in ctx.obj.get_all(done):
        print(str(todo))

@console.command()
@click.option('--id', prompt=True, type=int)
@click.option('--desc', default=None)
@click.option('--due', default=None, type=click.DateTime())
@click.option('--done', default=None)
@click.pass_context
def update(ctx, id, desc, due, done):
    ctx.obj.update(id, desc, due, done)

@console.command()
@click.option('--id', prompt=True, type=int)
@click.pass_context
def delete(ctx, id):
    ctx.obj.delete(id)

@console.command()
@click.option('--id', prompt=True, type=int)
@click.pass_context
def done(ctx, id):
    ctx.obj.update(id, done=True)

@console.command()
@click.option('--id', prompt=True, type=int)
@click.pass_context
def undone(ctx, id):
    ctx.obj.update(id, done=False)

if __name__ == '__main__':
    print('Welcome to the TODO CLI!')
    console()