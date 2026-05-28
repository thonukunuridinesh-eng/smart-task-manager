from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db, socketio
from .analytics import generate_analytics

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    analytics = generate_analytics(tasks)

    return render_template(
        'index.html',
        tasks=tasks,
        analytics=analytics
    )

@main.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    data = []

    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status
        })

    return jsonify(data)

@main.route('/api/tasks', methods=['POST'])
@login_required
def add_task():

    data = request.json

    task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        status=data['status'],
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    socketio.emit('task_update', {'message': 'Task Added'})

    return jsonify({"message": "Task Added"})


@main.route('/api/tasks/<int:id>', methods=['PUT'])
@login_required
def update_task(id):

    task = Task.query.get(id)

    data = request.json

    task.title = data['title']
    task.description = data['description']
    task.priority = data['priority']
    task.status = data['status']

    db.session.commit()

    socketio.emit('task_update', {'message': 'Task Updated'})

    return jsonify({"message": "Task Updated"})


@main.route('/api/tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):

    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    socketio.emit('task_update', {'message': 'Task Deleted'})

    return jsonify({"message": "Task Deleted"})