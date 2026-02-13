from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@task_bp.route('', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    try:
        status = request.args.get('status')
        assigned_to = request.args.get('assigned_to')
        
        tasks = TaskService.get_all_tasks(status=status, assigned_to=assigned_to)
        return jsonify({'success': True, 'data': tasks}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID"""
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        return jsonify({'success': True, 'data': task}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        
        task_id = TaskService.create_task(data)
        task = TaskService.get_task_by_id(task_id)
        
        return jsonify({'success': True, 'data': task}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    try:
        data = request.get_json()
        
        existing_task = TaskService.get_task_by_id(task_id)
        if not existing_task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        TaskService.update_task(task_id, data)
        task = TaskService.get_task_by_id(task_id)
        
        return jsonify({'success': True, 'data': task}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        existing_task = TaskService.get_task_by_id(task_id)
        if not existing_task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        TaskService.delete_task(task_id)
        
        return jsonify({'success': True, 'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
