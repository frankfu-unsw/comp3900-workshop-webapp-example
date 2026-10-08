import { useEffect, useState } from "react";
import "./App.css";

import AddTask from "./components/tasks/TaskAdd";
import TaskList from "./components/tasks/TaskList";

function App() {
  const TASKS_URL = "http://localhost:8000/api/tasks";

  const [tasks, setTasks] = useState([]);
  const [lastTaskTitle, setLastTitle] = useState("");

  const getTasks = async () => {
    const res = await fetch(TASKS_URL);
    const data = await res.json();
    setTasks(data);
  };

  const updateTaskCompletion = async (id) => {
    const t = tasks.find((tk) => tk.id == id);
    const res = await fetch(`${TASKS_URL}/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: t.id, completed: !t.completed, title: t.title }),
    });
    if (res.ok) {
      getTasks();
    }
  };

  const addTask = async (title) => {
    const res = await fetch(TASKS_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
        completed: false,
        id: Date.now(),
      }),
    });

    getTasks();
  };

  const deleteTask = async (id) => {
    const res = await fetch(`${TASKS_URL}/${id}`, {
      method: "DELETE",
    });
    getTasks();
  }

  useEffect(() => {
    getTasks();
  }, []);

  return (
    <>
      <h2>Task list manager</h2>

      <AddTask lastTaskTitle={lastTaskTitle} setLastTitle={setLastTitle} addTask={addTask} />
      <TaskList tasks={tasks} updateTaskCompletion={updateTaskCompletion} deleteTask={deleteTask} />

    </>
  );
}

export default App;
