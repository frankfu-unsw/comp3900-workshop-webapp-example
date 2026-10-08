import React from 'react'

function TaskAdd({ lastTaskTitle, setLastTitle, addTask }) {
    return (
        <div id="addTask">
            <input type="text" placeholder="Task title" value={lastTaskTitle} onChange={(e) => setLastTitle(e.target.value)} />
            <button onClick={() => addTask(lastTaskTitle)}>Add task</button>
        </div>
    )
}

export default TaskAdd