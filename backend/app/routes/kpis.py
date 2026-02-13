from flask import Blueprint, request, jsonify
from app.services.kpi_service import KPIService

kpi_bp = Blueprint('kpis', __name__, url_prefix='/api/kpis')


@kpi_bp.route('', methods=['GET'])
def get_kpis():
    """Get all KPIs"""
    try:
        kpis = KPIService.get_all_kpis()
        return jsonify({'success': True, 'data': kpis}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@kpi_bp.route('/<int:kpi_id>', methods=['GET'])
def get_kpi(kpi_id):
    """Get a single KPI by ID"""
    try:
        kpi = KPIService.get_kpi_by_id(kpi_id)
        if not kpi:
            return jsonify({'success': False, 'error': 'KPI not found'}), 404
        
        return jsonify({'success': True, 'data': kpi}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@kpi_bp.route('', methods=['POST'])
def create_kpi():
    """Create a new KPI"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'success': False, 'error': 'Name is required'}), 400
        
        kpi_id = KPIService.create_kpi(data)
        kpi = KPIService.get_kpi_by_id(kpi_id)
        
        return jsonify({'success': True, 'data': kpi}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@kpi_bp.route('/<int:kpi_id>', methods=['PUT'])
def update_kpi(kpi_id):
    """Update an existing KPI"""
    try:
        data = request.get_json()
        
        existing_kpi = KPIService.get_kpi_by_id(kpi_id)
        if not existing_kpi:
            return jsonify({'success': False, 'error': 'KPI not found'}), 404
        
        KPIService.update_kpi(kpi_id, data)
        kpi = KPIService.get_kpi_by_id(kpi_id)
        
        return jsonify({'success': True, 'data': kpi}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@kpi_bp.route('/<int:kpi_id>', methods=['DELETE'])
def delete_kpi(kpi_id):
    """Delete a KPI"""
    try:
        existing_kpi = KPIService.get_kpi_by_id(kpi_id)
        if not existing_kpi:
            return jsonify({'success': False, 'error': 'KPI not found'}), 404
        
        KPIService.delete_kpi(kpi_id)
        
        return jsonify({'success': True, 'message': 'KPI deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
