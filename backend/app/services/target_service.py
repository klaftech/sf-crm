from config.database import DatabaseConfig
from datetime import datetime


class TargetService:
    """Service for target-related database operations"""
    
    @staticmethod
    def get_all_targets():
        """Get all targets"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM targets ORDER BY end_date DESC")
            rows = cursor.fetchall()
            
            targets = []
            for row in rows:
                progress = (float(row.current_value) / float(row.target_value) * 100) if float(row.target_value) > 0 else 0
                
                targets.append({
                    'id': row.id,
                    'name': row.name,
                    'description': row.description,
                    'target_type': row.target_type,
                    'target_value': float(row.target_value),
                    'current_value': float(row.current_value),
                    'start_date': row.start_date.isoformat() if row.start_date else None,
                    'end_date': row.end_date.isoformat() if row.end_date else None,
                    'status': row.status,
                    'progress_percentage': round(progress, 2),
                    'created_at': row.created_at.isoformat() if row.created_at else None,
                    'updated_at': row.updated_at.isoformat() if row.updated_at else None
                })
            
            conn.close()
            return targets
        except Exception as e:
            print(f"Error getting targets: {e}")
            raise
    
    @staticmethod
    def get_target_by_id(target_id):
        """Get a single target by ID"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM targets WHERE id = ?", (target_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return None
            
            progress = (float(row.current_value) / float(row.target_value) * 100) if float(row.target_value) > 0 else 0
            
            target = {
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'target_type': row.target_type,
                'target_value': float(row.target_value),
                'current_value': float(row.current_value),
                'start_date': row.start_date.isoformat() if row.start_date else None,
                'end_date': row.end_date.isoformat() if row.end_date else None,
                'status': row.status,
                'progress_percentage': round(progress, 2),
                'created_at': row.created_at.isoformat() if row.created_at else None,
                'updated_at': row.updated_at.isoformat() if row.updated_at else None
            }
            
            conn.close()
            return target
        except Exception as e:
            print(f"Error getting target: {e}")
            raise
    
    @staticmethod
    def create_target(target_data):
        """Create a new target"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO targets 
                (name, description, target_type, target_value, current_value, start_date, end_date, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            now = datetime.now()
            cursor.execute(query, (
                target_data.get('name'),
                target_data.get('description', ''),
                target_data.get('target_type'),
                target_data.get('target_value'),
                target_data.get('current_value', 0),
                target_data.get('start_date'),
                target_data.get('end_date'),
                target_data.get('status', 'active'),
                now,
                now
            ))
            
            conn.commit()
            target_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            conn.close()
            
            return target_id
        except Exception as e:
            print(f"Error creating target: {e}")
            raise
    
    @staticmethod
    def update_target(target_id, target_data):
        """Update an existing target"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE targets 
                SET name = ?, description = ?, target_type = ?, 
                    target_value = ?, current_value = ?, start_date = ?, 
                    end_date = ?, status = ?, updated_at = ?
                WHERE id = ?
            """
            
            cursor.execute(query, (
                target_data.get('name'),
                target_data.get('description'),
                target_data.get('target_type'),
                target_data.get('target_value'),
                target_data.get('current_value'),
                target_data.get('start_date'),
                target_data.get('end_date'),
                target_data.get('status'),
                datetime.now(),
                target_id
            ))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error updating target: {e}")
            raise
    
    @staticmethod
    def delete_target(target_id):
        """Delete a target"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM targets WHERE id = ?", (target_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error deleting target: {e}")
            raise
