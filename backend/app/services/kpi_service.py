from config.database import DatabaseConfig
from datetime import datetime


class KPIService:
    """Service for KPI-related database operations"""
    
    @staticmethod
    def get_all_kpis():
        """Get all KPIs"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM kpis ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            kpis = []
            for row in rows:
                performance = (float(row.current_value) / float(row.target_value) * 100) if float(row.target_value) > 0 else 0
                status = 'green' if performance >= 100 else ('yellow' if performance >= 80 else 'red')
                
                kpis.append({
                    'id': row.id,
                    'name': row.name,
                    'description': row.description,
                    'calculation_method': row.calculation_method,
                    'target_value': float(row.target_value),
                    'current_value': float(row.current_value),
                    'period': row.period,
                    'performance_percentage': round(performance, 2),
                    'status': status,
                    'created_at': row.created_at.isoformat() if row.created_at else None,
                    'updated_at': row.updated_at.isoformat() if row.updated_at else None
                })
            
            conn.close()
            return kpis
        except Exception as e:
            print(f"Error getting KPIs: {e}")
            raise
    
    @staticmethod
    def get_kpi_by_id(kpi_id):
        """Get a single KPI by ID"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM kpis WHERE id = ?", (kpi_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return None
            
            performance = (float(row.current_value) / float(row.target_value) * 100) if float(row.target_value) > 0 else 0
            status = 'green' if performance >= 100 else ('yellow' if performance >= 80 else 'red')
            
            kpi = {
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'calculation_method': row.calculation_method,
                'target_value': float(row.target_value),
                'current_value': float(row.current_value),
                'period': row.period,
                'performance_percentage': round(performance, 2),
                'status': status,
                'created_at': row.created_at.isoformat() if row.created_at else None,
                'updated_at': row.updated_at.isoformat() if row.updated_at else None
            }
            
            conn.close()
            return kpi
        except Exception as e:
            print(f"Error getting KPI: {e}")
            raise
    
    @staticmethod
    def create_kpi(kpi_data):
        """Create a new KPI"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO kpis 
                (name, description, calculation_method, target_value, current_value, period, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            now = datetime.now()
            cursor.execute(query, (
                kpi_data.get('name'),
                kpi_data.get('description', ''),
                kpi_data.get('calculation_method', ''),
                kpi_data.get('target_value', 0),
                kpi_data.get('current_value', 0),
                kpi_data.get('period', 'monthly'),
                now,
                now
            ))
            
            conn.commit()
            kpi_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            conn.close()
            
            return kpi_id
        except Exception as e:
            print(f"Error creating KPI: {e}")
            raise
    
    @staticmethod
    def update_kpi(kpi_id, kpi_data):
        """Update an existing KPI"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE kpis 
                SET name = ?, description = ?, calculation_method = ?, 
                    target_value = ?, current_value = ?, period = ?, updated_at = ?
                WHERE id = ?
            """
            
            cursor.execute(query, (
                kpi_data.get('name'),
                kpi_data.get('description'),
                kpi_data.get('calculation_method'),
                kpi_data.get('target_value'),
                kpi_data.get('current_value'),
                kpi_data.get('period'),
                datetime.now(),
                kpi_id
            ))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error updating KPI: {e}")
            raise
    
    @staticmethod
    def delete_kpi(kpi_id):
        """Delete a KPI"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM kpis WHERE id = ?", (kpi_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error deleting KPI: {e}")
            raise
