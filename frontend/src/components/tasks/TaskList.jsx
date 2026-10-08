import React from 'react'

function TaskList({ tasks, updateTaskCompletion, deleteTask }) {
    return (
        <div id="taskList">
            {tasks.map((t) => (
                <div key={t.id}>
                    <span style={{ textDecoration: t.completed ? "line-through" : "none" }}>{t.title}</span>
                    <button onClick={() => updateTaskCompletion(t.id)}>{t.completed ? "mark incomplete" : "mark complete"}</button>
                    <button onClick={() => deleteTask(t.id)}>Delete</button>
                </div>
            ))}
        </div>
    )
}

export default TaskList