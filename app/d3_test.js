import React, { useState } from "react";
import { render } from "react-dom";

/*const container = document.getElementById('app');*/

const TODOS = ["Manger", "Travailler", "Prendre le métro"];

function TodoListItem({ title, onDrop }) {
  return (
    <li>
      {title}
      <button onClick={() => onDrop(title)}>-</button>
    </li>
  );
}

function TodoList({ items, onDrop }) {
  return (
    <ul>
      {items.map((item) => (
        <TodoListItem key={item} title={item} onDrop={onDrop} />
      ))}
    </ul>
  );
}

function LastAddedItem({ item }) {
  if (!item) return <p>Quedalle</p>;

  return <p>Le dernier element à avoir été ajouté: {item}</p>;
}

function Application() {
  const [text, setText] = useState("");
  const [todos, setTodos] = useState(TODOS.slice());
  const [lastAddedItem, setLastAddItem] = useState(null);

  const onButtonClick = () => {
    setTodos(todos.concat(text));
    setText("");
    setLastAddItem(text);
  };

  const dropTodo = (todo) => {
    setTodos(todos.filter((t) => t !== todo));
  };

  return (
    <div>
      <h1>Super Application</h1>
      <TodoList items={todos} onDrop={dropTodo} />
      <input
        type="test"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={onButtonClick}>Ajouter</button>
      <LastAddedItem item={lastAddedItem} />
    </div>
  );
}

// Application > TodoList > [TodoListItem]
//             > LastAddedItem

/*render(<Application />, container);

console.log('one');

setTimeout(() => {
  console.log('two');

  setTimeout(() => {
    console.log('four');

    setTimeout(() => {
      console.log('five');

      setTimeout(() => {
        console.log('six');
      }, 100);
    }, 500);
  }, 100);
}, 1000);

console.log('three');*/
