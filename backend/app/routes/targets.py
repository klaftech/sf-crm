from flask import Blueprint, request, jsonify
from app.services.target_service import TargetService

target_bp = Blueprint('targets', __name__, url_prefix='/api/targets')


@target_bp.route('', methods=['GET'])
def get_targets():
    """Get all targets"""
    try:
        targets = TargetService.get_all_targets()
        return jsonify({'success': True, 'data': targets}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@target_bp.route('/<int:target_id>', methods=['GET'])
def get_target(target_id):
    """Get a single target by ID"""
    try:
        target = TargetService.get_target_by_id(target_id)
        if not target:
            return jsonify({'success': False, 'error': 'Target not found'}), 404
        
        return jsonify({'success': True, 'data': target}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@target_bp.route('', methods=['POST'])
def create_target():
    """Create a new target"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'success': False, 'error': 'Name is required'}), 400
        
        target_id = TargetService.create_target(data)
        target = TargetService.get_target_by_id(target_id)
        
        return jsonify({'success': True, 'data': target}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@target_bp.route('/<int:target_id>', methods=['PUT'])
def update_target(target_id):
    """Update an existing target"""
    try:
        data = request.get_json()
        
        existing_target = TargetService.get_target_by_id(target_id)
        if not existing_target:
            return jsonify({'success': False, 'error': 'Target not found'}), 404
        
        TargetService.update_target(target_id, data)
        target = TargetService.get_target_by_id(target_id)
        
        return jsonify({'success': True, 'data': target}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@target_bp.route('/<int:target_id>', methods=['DELETE'])
def delete_target(target_id):
    """Delete a target"""
    try:
        existing_target = TargetService.get_target_by_id(target_id)
        if not existing_target:
            return jsonify({'success': False, 'error': 'Target not found'}), 404
        
        TargetService.delete_target(target_id)
        
        return jsonify({'success': True, 'message': 'Target deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
