# API Documentation

This document provides detailed information about the CRM API endpoints.

## Base URL

```
http://localhost:5000/api
```

## Response Format

All API responses follow this format:

**Success Response:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## Tasks API

### Get All Tasks

Get a list of all tasks with optional filtering.

**Endpoint:** `GET /api/tasks`

**Query Parameters:**
- `status` (optional): Filter by status (pending, in_progress, completed, cancelled)
- `assigned_to` (optional): Filter by assignee name

**Example Request:**
```bash
curl http://localhost:5000/api/tasks?status=pending
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "customer_id": 123,
      "title": "Follow up on proposal",
      "description": "Contact customer about submitted proposal",
      "due_date": "2024-02-15T00:00:00",
      "assigned_to": "John Smith",
      "status": "pending",
      "priority": "high",
      "created_at": "2024-02-01T10:00:00",
      "updated_at": "2024-02-01T10:00:00"
    }
  ]
}
```

### Get Task by ID

**Endpoint:** `GET /api/tasks/:id`

**Example Request:**
```bash
curl http://localhost:5000/api/tasks/1
```

### Create Task

**Endpoint:** `POST /api/tasks`

**Request Body:**
```json
{
  "customer_id": 123,
  "title": "Follow up call",
  "description": "Discuss product features",
  "due_date": "2024-02-20",
  "assigned_to": "Jane Doe",
  "status": "pending",
  "priority": "medium"
}
```

**Required Fields:**
- `title`

**Optional Fields:**
- `customer_id`, `description`, `due_date`, `assigned_to`, `status`, `priority`

### Update Task

**Endpoint:** `PUT /api/tasks/:id`

**Request Body:** Same as Create Task

### Delete Task

**Endpoint:** `DELETE /api/tasks/:id`

---

## KPIs API

### Get All KPIs

**Endpoint:** `GET /api/kpis`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Monthly Sales Revenue",
      "description": "Total sales revenue for the current month",
      "calculation_method": "SUM(sales.amount)",
      "target_value": 100000.00,
      "current_value": 75000.00,
      "period": "monthly",
      "performance_percentage": 75.00,
      "status": "yellow",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-02-01T00:00:00"
    }
  ]
}
```

**Status Values:**
- `green`: Performance >= 100%
- `yellow`: Performance >= 80%
- `red`: Performance < 80%

### Get KPI by ID

**Endpoint:** `GET /api/kpis/:id`

### Create KPI

**Endpoint:** `POST /api/kpis`

**Request Body:**
```json
{
  "name": "Customer Acquisition",
  "description": "Number of new customers this month",
  "calculation_method": "COUNT(new_customers)",
  "target_value": 50,
  "current_value": 35,
  "period": "monthly"
}
```

**Required Fields:**
- `name`

**Period Options:**
- `daily`, `weekly`, `monthly`, `quarterly`, `yearly`

### Update KPI

**Endpoint:** `PUT /api/kpis/:id`

### Delete KPI

**Endpoint:** `DELETE /api/kpis/:id`

---

## Targets API

### Get All Targets

**Endpoint:** `GET /api/targets`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Q1 2024 Revenue Target",
      "description": "Revenue goal for first quarter",
      "target_type": "revenue",
      "target_value": 300000.00,
      "current_value": 180000.00,
      "start_date": "2024-01-01T00:00:00",
      "end_date": "2024-03-31T00:00:00",
      "status": "active",
      "progress_percentage": 60.00,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-02-01T00:00:00"
    }
  ]
}
```

### Get Target by ID

**Endpoint:** `GET /api/targets/:id`

### Create Target

**Endpoint:** `POST /api/targets`

**Request Body:**
```json
{
  "name": "Q2 Revenue Target",
  "description": "Revenue goal for Q2",
  "target_type": "revenue",
  "target_value": 350000,
  "current_value": 0,
  "start_date": "2024-04-01",
  "end_date": "2024-06-30",
  "status": "active"
}
```

**Required Fields:**
- `name`, `target_type`, `target_value`

**Target Type Options:**
- `revenue`, `units`, `customers`, `tasks`, `other`

**Status Options:**
- `active`, `completed`, `cancelled`, `at_risk`

### Update Target

**Endpoint:** `PUT /api/targets/:id`

### Delete Target

**Endpoint:** `DELETE /api/targets/:id`

---

## ERP Data API

### Get Customers

Get customers from the ERP database (read-only).

**Endpoint:** `GET /api/erp/customers`

**Query Parameters:**
- `limit` (optional, default: 100): Maximum number of results
- `offset` (optional, default: 0): Offset for pagination
- `search` (optional): Search term for name or email

**Example Request:**
```bash
curl http://localhost:5000/api/erp/customers?search=acme&limit=50
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Acme Corporation",
      "email": "contact@acme.com",
      "phone": "555-0100",
      "address": "123 Main St",
      "city": "New York",
      "country": "USA"
    }
  ]
}
```

### Get Customer by ID

**Endpoint:** `GET /api/erp/customers/:id`

### Get Sales Data

Get sales transactions from the ERP database.

**Endpoint:** `GET /api/erp/sales`

**Query Parameters:**
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `customer_id` (optional): Filter by customer ID

**Example Request:**
```bash
curl "http://localhost:5000/api/erp/sales?start_date=2024-01-01&end_date=2024-01-31"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "customer_id": 123,
      "sale_date": "2024-01-15T00:00:00",
      "amount": 5000.00,
      "product": "Product A",
      "quantity": 10
    }
  ]
}
```

### Get Sales Summary

Get aggregated sales data by period.

**Endpoint:** `GET /api/erp/sales/summary`

**Query Parameters:**
- `period` (optional, default: monthly): Aggregation period (daily, monthly, yearly)

**Example Request:**
```bash
curl http://localhost:5000/api/erp/sales/summary?period=monthly
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "period": "2024-01",
      "transaction_count": 45,
      "total_amount": 125000.00,
      "avg_amount": 2777.78
    },
    {
      "period": "2024-02",
      "transaction_count": 52,
      "total_amount": 142000.00,
      "avg_amount": 2730.77
    }
  ]
}
```

---

## Health Check

### Check API Health

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "message": "CRM API is running"
}
```

---

## Error Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request (invalid input)
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting using Flask-Limiter.

## Authentication

Currently, no authentication is required. For production use, implement authentication using:
- JWT tokens
- OAuth 2.0
- API keys

## CORS

CORS is enabled for the origins specified in the `CORS_ORIGINS` environment variable. By default:
- `http://localhost:3000`
- `http://localhost:5173`

## Notes for ERP Integration

The ERP endpoints assume specific table and column names. If your ERP database has different schema, you'll need to update the queries in `backend/app/services/erp_service.py`.

**Expected ERP Tables:**

**Customers Table:**
- `CustomerID` (INT)
- `CustomerName` (NVARCHAR)
- `Email` (NVARCHAR)
- `Phone` (NVARCHAR)
- `Address` (NVARCHAR)
- `City` (NVARCHAR)
- `Country` (NVARCHAR)

**Sales Table:**
- `SaleID` (INT)
- `CustomerID` (INT)
- `SaleDate` (DATETIME)
- `TotalAmount` (DECIMAL)
- `ProductName` (NVARCHAR)
- `Quantity` (INT)

## Testing the API

You can test the API using:

**cURL:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","priority":"high"}'
```

**Postman:**
Import the endpoints and test interactively.

**Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/kpis')
data = response.json()
print(data)
```

**JavaScript:**
```javascript
fetch('http://localhost:5000/api/targets')
  .then(response => response.json())
  .then(data => console.log(data));
```
