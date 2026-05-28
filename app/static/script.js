const socket = io();

// Listen for real-time task updates from the server
socket.on('task_update', function(data) {
    console.log(data.message);
    
    // Fetch updated task list and re-render dynamically
    fetch('/api/tasks')
        .then(response => response.json())
        .then(tasks => {
            const tasksContainer = document.getElementById('tasks');
            tasksContainer.innerHTML = ''; // Clear old list
            
            tasks.forEach(task => {
                const taskDiv = document.createElement('div');
                
                // Apply dynamic lowercase priority classes for color borders
                taskDiv.className = `task priority-${task.priority.toLowerCase()}`;
                
                // 🚀 UPDATE: Render matching layout wrapper including title and delete button matching index.html
                taskDiv.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <h2>${task.title}</h2>
                        <button class="delete-btn" onclick="deleteTask(${task.id})">&times;</button>
                    </div>
                    <p class="desc">${task.description}</p>
                    <div class="task-tags">
                        <span class="badge priority">${task.priority}</span>
                        <span class="badge status-${task.status.toLowerCase()}">${task.status}</span>
                    </div>
                `;
                tasksContainer.appendChild(taskDiv);
            });
            
            // Forces page reload to keep top analytics numbers synchronized
            window.location.reload();
        });
});

// Handle new task submission asynchronously
document.getElementById('taskForm')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const taskData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        priority: document.getElementById('priority').value,
        status: document.getElementById('status').value
    };

    fetch('/api/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(taskData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        // Clear the form fields
        document.getElementById('title').value = '';
        document.getElementById('description').value = '';
    });
});

// 🚀 ADDED: Asynchronous API call to delete tasks by ID
function deleteTask(taskId) {
    if (confirm("Are you sure you want to delete this task?")) {
        fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            // The back-end will emit 'task_update' over WebSocket, triggering the reload automatically
        })
        .catch(err => console.error("Error deleting task:", err));
    }
}


