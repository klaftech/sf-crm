from config.database import DatabaseConfig


def safe_get_attr(row, attr, default=''):
    """Safely get attribute from database row with default value"""
    return getattr(row, attr, default) if hasattr(row, attr) else default


class ERPService:
    """Service for ERP-related data access (read-only)"""
    
    @staticmethod
    def get_customers(limit=100, offset=0, search=None):
        """Get customers from ERP database"""
        try:
            conn = DatabaseConfig.get_erp_connection()
            cursor = conn.cursor()
            
            # Note: This is a sample query structure. 
            # Adjust table and column names based on actual ERP schema
            query = """
                SELECT TOP (?) 
                    CustomerID as id,
                    CustomerName as name,
                    Email as email,
                    Phone as phone,
                    Address as address,
                    City as city,
                    Country as country
                FROM Customers
                WHERE 1=1
            """
            
            params = [limit]
            
            if search:
                query += " AND (CustomerName LIKE ? OR Email LIKE ?)"
                search_param = f"%{search}%"
                params.extend([search_param, search_param])
            
            query += " ORDER BY CustomerName"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            customers = []
            for row in rows:
                customers.append({
                    'id': safe_get_attr(row, 'id', None),
                    'name': safe_get_attr(row, 'name'),
                    'email': safe_get_attr(row, 'email'),
                    'phone': safe_get_attr(row, 'phone'),
                    'address': safe_get_attr(row, 'address'),
                    'city': safe_get_attr(row, 'city'),
                    'country': safe_get_attr(row, 'country')
                })
            
            conn.close()
            return customers
        except Exception as e:
            print(f"Error getting customers from ERP: {e}")
            # Return empty list if table doesn't exist or connection fails
            return []
    
    @staticmethod
    def get_customer_by_id(customer_id):
        """Get a single customer from ERP database"""
        try:
            conn = DatabaseConfig.get_erp_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    CustomerID as id,
                    CustomerName as name,
                    Email as email,
                    Phone as phone,
                    Address as address,
                    City as city,
                    Country as country,
                    CreatedDate as created_date
                FROM Customers
                WHERE CustomerID = ?
            """
            
            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return None
            
            created_date = safe_get_attr(row, 'created_date', None)
            customer = {
                'id': safe_get_attr(row, 'id', None),
                'name': safe_get_attr(row, 'name'),
                'email': safe_get_attr(row, 'email'),
                'phone': safe_get_attr(row, 'phone'),
                'address': safe_get_attr(row, 'address'),
                'city': safe_get_attr(row, 'city'),
                'country': safe_get_attr(row, 'country'),
                'created_date': created_date.isoformat() if created_date else None
            }
            
            conn.close()
            return customer
        except Exception as e:
            print(f"Error getting customer from ERP: {e}")
            return None
    
    @staticmethod
    def get_sales_data(start_date=None, end_date=None, customer_id=None):
        """Get sales data from ERP database"""
        try:
            conn = DatabaseConfig.get_erp_connection()
            cursor = conn.cursor()
            
            # Note: Adjust based on actual ERP schema
            query = """
                SELECT 
                    SaleID as id,
                    CustomerID as customer_id,
                    SaleDate as sale_date,
                    TotalAmount as amount,
                    ProductName as product,
                    Quantity as quantity
                FROM Sales
                WHERE 1=1
            """
            
            params = []
            
            if start_date:
                query += " AND SaleDate >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND SaleDate <= ?"
                params.append(end_date)
            
            if customer_id:
                query += " AND CustomerID = ?"
                params.append(customer_id)
            
            query += " ORDER BY SaleDate DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            sales = []
            for row in rows:
                sale_date = safe_get_attr(row, 'sale_date', None)
                amount = safe_get_attr(row, 'amount', 0)
                quantity = safe_get_attr(row, 'quantity', 0)
                
                sales.append({
                    'id': safe_get_attr(row, 'id', None),
                    'customer_id': safe_get_attr(row, 'customer_id', None),
                    'sale_date': sale_date.isoformat() if sale_date else None,
                    'amount': float(amount) if amount else 0,
                    'product': safe_get_attr(row, 'product'),
                    'quantity': int(quantity) if quantity else 0
                })
            
            conn.close()
            return sales
        except Exception as e:
            print(f"Error getting sales data from ERP: {e}")
            return []
    
    @staticmethod
    def get_sales_summary(period='monthly'):
        """Get sales summary/aggregates from ERP"""
        try:
            conn = DatabaseConfig.get_erp_connection()
            cursor = conn.cursor()
            
            # Aggregate sales by period
            if period == 'daily':
                date_format = "CAST(SaleDate AS DATE)"
            elif period == 'monthly':
                date_format = "FORMAT(SaleDate, 'yyyy-MM')"
            elif period == 'yearly':
                date_format = "YEAR(SaleDate)"
            else:
                date_format = "FORMAT(SaleDate, 'yyyy-MM')"
            
            query = f"""
                SELECT 
                    {date_format} as period,
                    COUNT(*) as transaction_count,
                    SUM(TotalAmount) as total_amount,
                    AVG(TotalAmount) as avg_amount
                FROM Sales
                WHERE SaleDate >= DATEADD(YEAR, -1, GETDATE())
                GROUP BY {date_format}
                ORDER BY period DESC
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            summary = []
            for row in rows:
                period = safe_get_attr(row, 'period', '')
                transaction_count = safe_get_attr(row, 'transaction_count', 0)
                total_amount = safe_get_attr(row, 'total_amount', 0)
                avg_amount = safe_get_attr(row, 'avg_amount', 0)
                
                summary.append({
                    'period': str(period),
                    'transaction_count': int(transaction_count) if transaction_count else 0,
                    'total_amount': float(total_amount) if total_amount else 0,
                    'avg_amount': float(avg_amount) if avg_amount else 0
                })
            
            conn.close()
            return summary
        except Exception as e:
            print(f"Error getting sales summary from ERP: {e}")
            return []
