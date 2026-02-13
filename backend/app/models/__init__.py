from datetime import datetime
from typing import Optional


class Task:
    """Task model for follow-up activities"""
    
    def __init__(self, id: Optional[int] = None, customer_id: Optional[int] = None,
                 title: str = '', description: str = '', due_date: Optional[datetime] = None,
                 assigned_to: str = '', status: str = 'pending', priority: str = 'medium',
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.customer_id = customer_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_to = assigned_to
        self.status = status  # pending, in_progress, completed, cancelled
        self.priority = priority  # low, medium, high, urgent
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_row(row):
        """Create Task object from database row"""
        return Task(
            id=row.id,
            customer_id=row.customer_id,
            title=row.title,
            description=row.description,
            due_date=row.due_date,
            assigned_to=row.assigned_to,
            status=row.status,
            priority=row.priority,
            created_at=row.created_at,
            updated_at=row.updated_at
        )


class KPI:
    """KPI model for tracking key performance indicators"""
    
    def __init__(self, id: Optional[int] = None, name: str = '', description: str = '',
                 calculation_method: str = '', target_value: float = 0.0,
                 current_value: float = 0.0, period: str = 'monthly',
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.description = description
        self.calculation_method = calculation_method
        self.target_value = target_value
        self.current_value = current_value
        self.period = period  # daily, weekly, monthly, quarterly, yearly
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert KPI to dictionary"""
        performance = (self.current_value / self.target_value * 100) if self.target_value > 0 else 0
        status = 'green' if performance >= 100 else ('yellow' if performance >= 80 else 'red')
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'calculation_method': self.calculation_method,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'period': self.period,
            'performance_percentage': round(performance, 2),
            'status': status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_row(row):
        """Create KPI object from database row"""
        return KPI(
            id=row.id,
            name=row.name,
            description=row.description,
            calculation_method=row.calculation_method,
            target_value=float(row.target_value),
            current_value=float(row.current_value),
            period=row.period,
            created_at=row.created_at,
            updated_at=row.updated_at
        )


class Target:
    """Target model for tracking goals"""
    
    def __init__(self, id: Optional[int] = None, name: str = '', description: str = '',
                 target_type: str = '', target_value: float = 0.0, current_value: float = 0.0,
                 start_date: Optional[datetime] = None, end_date: Optional[datetime] = None,
                 status: str = 'active', created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.description = description
        self.target_type = target_type  # revenue, units, customers, tasks, etc.
        self.target_value = target_value
        self.current_value = current_value
        self.start_date = start_date
        self.end_date = end_date
        self.status = status  # active, completed, cancelled, at_risk
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convert target to dictionary"""
        progress = (self.current_value / self.target_value * 100) if self.target_value > 0 else 0
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'target_type': self.target_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'progress_percentage': round(progress, 2),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_row(row):
        """Create Target object from database row"""
        return Target(
            id=row.id,
            name=row.name,
            description=row.description,
            target_type=row.target_type,
            target_value=float(row.target_value),
            current_value=float(row.current_value),
            start_date=row.start_date,
            end_date=row.end_date,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at
        )


class Note:
    """Note model for customer notes"""
    
    def __init__(self, id: Optional[int] = None, customer_id: Optional[int] = None,
                 note_text: str = '', created_by: str = '',
                 created_at: Optional[datetime] = None):
        self.id = id
        self.customer_id = customer_id
        self.note_text = note_text
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """Convert note to dictionary"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'note_text': self.note_text,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def from_row(row):
        """Create Note object from database row"""
        return Note(
            id=row.id,
            customer_id=row.customer_id,
            note_text=row.note_text,
            created_by=row.created_by,
            created_at=row.created_at
        )
