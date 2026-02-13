from config.database import DatabaseConfig
from datetime import datetime
import pyodbc


class TaskService:
    """Service for task-related database operations"""
    
    @staticmethod
    def get_all_tasks(status=None, assigned_to=None):
        """Get all tasks with optional filtering"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM tasks WHERE 1=1"
            params = []
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            if assigned_to:
                query += " AND assigned_to = ?"
                params.append(assigned_to)
            
            query += " ORDER BY due_date ASC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            tasks = []
            for row in rows:
                tasks.append({
                    'id': row.id,
                    'customer_id': row.customer_id,
                    'title': row.title,
                    'description': row.description,
                    'due_date': row.due_date.isoformat() if row.due_date else None,
                    'assigned_to': row.assigned_to,
                    'status': row.status,
                    'priority': row.priority,
                    'created_at': row.created_at.isoformat() if row.created_at else None,
                    'updated_at': row.updated_at.isoformat() if row.updated_at else None
                })
            
            conn.close()
            return tasks
        except Exception as e:
            print(f"Error getting tasks: {e}")
            raise
    
    @staticmethod
    def get_task_by_id(task_id):
        """Get a single task by ID"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return None
            
            task = {
                'id': row.id,
                'customer_id': row.customer_id,
                'title': row.title,
                'description': row.description,
                'due_date': row.due_date.isoformat() if row.due_date else None,
                'assigned_to': row.assigned_to,
                'status': row.status,
                'priority': row.priority,
                'created_at': row.created_at.isoformat() if row.created_at else None,
                'updated_at': row.updated_at.isoformat() if row.updated_at else None
            }
            
            conn.close()
            return task
        except Exception as e:
            print(f"Error getting task: {e}")
            raise
    
    @staticmethod
    def create_task(task_data):
        """Create a new task"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO tasks 
                (customer_id, title, description, due_date, assigned_to, status, priority, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            now = datetime.now()
            cursor.execute(query, (
                task_data.get('customer_id'),
                task_data.get('title'),
                task_data.get('description', ''),
                task_data.get('due_date'),
                task_data.get('assigned_to', ''),
                task_data.get('status', 'pending'),
                task_data.get('priority', 'medium'),
                now,
                now
            ))
            
            conn.commit()
            task_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
            conn.close()
            
            return task_id
        except Exception as e:
            print(f"Error creating task: {e}")
            raise
    
    @staticmethod
    def update_task(task_id, task_data):
        """Update an existing task"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE tasks 
                SET customer_id = ?, title = ?, description = ?, due_date = ?, 
                    assigned_to = ?, status = ?, priority = ?, updated_at = ?
                WHERE id = ?
            """
            
            cursor.execute(query, (
                task_data.get('customer_id'),
                task_data.get('title'),
                task_data.get('description'),
                task_data.get('due_date'),
                task_data.get('assigned_to'),
                task_data.get('status'),
                task_data.get('priority'),
                datetime.now(),
                task_id
            ))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            raise
    
    @staticmethod
    def delete_task(task_id):
        """Delete a task"""
        try:
            conn = DatabaseConfig.get_crm_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            raise
