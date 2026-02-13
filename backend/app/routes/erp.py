from flask import Blueprint, request, jsonify
from app.services.erp_service import ERPService

erp_bp = Blueprint('erp', __name__, url_prefix='/api/erp')


@erp_bp.route('/customers', methods=['GET'])
def get_customers():
    """Get customers from ERP database"""
    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        search = request.args.get('search')
        
        customers = ERPService.get_customers(limit=limit, offset=offset, search=search)
        return jsonify({'success': True, 'data': customers}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@erp_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a single customer from ERP database"""
    try:
        customer = ERPService.get_customer_by_id(customer_id)
        if not customer:
            return jsonify({'success': False, 'error': 'Customer not found'}), 404
        
        return jsonify({'success': True, 'data': customer}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@erp_bp.route('/sales', methods=['GET'])
def get_sales():
    """Get sales data from ERP database"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        customer_id = request.args.get('customer_id')
        
        sales = ERPService.get_sales_data(
            start_date=start_date,
            end_date=end_date,
            customer_id=customer_id
        )
        return jsonify({'success': True, 'data': sales}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@erp_bp.route('/sales/summary', methods=['GET'])
def get_sales_summary():
    """Get sales summary/aggregates from ERP"""
    try:
        period = request.args.get('period', 'monthly')
        
        summary = ERPService.get_sales_summary(period=period)
        return jsonify({'success': True, 'data': summary}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
