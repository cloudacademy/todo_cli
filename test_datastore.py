from datetime import datetime, timedelta
from pathlib import Path
import pytest

from app import Datastore


@pytest.fixture
def datastore():
    # Create a temporary database file for testing.
    file_path = 'test_db/todo.db'
    datastore = Datastore(file_path)
    yield datastore
    # Clean up the temporary database file.
    Path(file_path).unlink()


def test_add(datastore):
    # Add a new todo item.
    desc = 'Test todo item'
    due_date = datetime.now() + timedelta(days=1)
    done = False
    todo = datastore.add(desc, due_date, done)

    # Verify that the todo item was added correctly.
    assert todo.id == 1
    assert todo.description == desc
    assert todo.due_date == due_date
    assert todo.done == done


def test_get_all(datastore):
    # Add some test todo items.
    todo1 = datastore.add('Test todo item 1', datetime.now() + timedelta(days=1), False)
    todo2 = datastore.add('Test todo item 2', datetime.now() + timedelta(days=2), True)
    todo3 = datastore.add('Test todo item 3', datetime.now() + timedelta(days=3), False)

    # Get all todo items.
    todos = datastore.get_all()

    # Verify that all todo items were returned.
    assert len(todos) == 3
    assert todos[0] == todo1
    assert todos[1] == todo2
    assert todos[2] == todo3

    # Get only done todo items.
    todos = datastore.get_all(done=True)

    # Verify that only the done todo item was returned.
    assert len(todos) == 1
    assert todos[0] == todo2


def test_get(datastore):
    # Add a test todo item.
    todo = datastore.add('Test todo item', datetime.now() + timedelta(days=1), False)

    # Get the todo item by ID.
    todo_id = todo.id
    retrieved_todo = datastore.get(todo_id)

    # Verify that the correct todo item was returned.
    assert retrieved_todo == todo


def test_update(datastore):
    # Add a test todo item.
    todo = datastore.add('Test todo item', datetime.now() + timedelta(days=1), False)

    # Update the todo item.
    new_desc = 'Updated todo item'
    new_due_date = datetime.now() + timedelta(days=2)
    new_done = True
    datastore.update(todo.id, new_desc, new_due_date, new_done)

    # Get the updated todo item.
    updated_todo = datastore.get(todo.id)

    # Verify that the todo item was updated correctly.
    assert updated_todo.description == new_desc
    assert updated_todo.due_date == new_due_date
    assert updated_todo.done == new_done


def test_delete(datastore):
    # Add a test todo item.
    todo = datastore.add('Test todo item', datetime.now() + timedelta(days=1), False)

    # Delete the todo item.
    datastore.delete(todo.id)

    # Verify that the todo item was deleted.
    assert datastore.get(todo.id) is None
