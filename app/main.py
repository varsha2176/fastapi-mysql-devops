from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import mysql.connector
from mysql.connector import Error
import time
import os
from typing import Optional

app = FastAPI(title="FastAPI Admin Panel API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Configuration
DB_CONFIG = {
    'host': 'db',
    'user': 'root',
    'password': 'rootpassword',
    'database': 'testdb'
}

def get_db_connection():
    """Create database connection with retry logic"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise HTTPException(status_code=500, detail="Database connection failed")

# ==================== BASIC ENDPOINTS ====================

@app.get("/")
def read_root():
    return {
        "message": "FastAPI Admin Panel - Running Successfully",
        "status": "healthy",
        "admin_panel": "/admin",
        "api_docs": "/docs"
    }

@app.get("/health")
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "message": "All systems operational"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# ==================== ADMIN PANEL ROUTE ====================

@app.get("/admin")
def admin_panel():
    """Serve admin panel HTML"""
    admin_path = "/app/admin/index.html"
    
    # Check if file exists
    if not os.path.exists(admin_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Admin panel not found at {admin_path}. Please ensure admin/index.html exists."
        )
    
    return FileResponse(admin_path)

# Mount static files AFTER defining routes
if os.path.exists("/app/admin"):
    app.mount("/static", StaticFiles(directory="/app/admin"), name="static")

# ==================== USER MANAGEMENT API ====================

@app.get("/api/users")
def get_all_users():
    """Get all users"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        # Convert datetime objects to strings
        for user in users:
            if user.get('created_at'):
                user['created_at'] = str(user['created_at'])
            if user.get('updated_at'):
                user['updated_at'] = str(user['updated_at'])
        
        cursor.close()
        conn.close()
        
        return JSONResponse(content={
            "success": True,
            "data": users,
            "count": len(users)
        })
    except Exception as e:
        print(f"Error in get_all_users: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    """Get single user by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user:
            if user.get('created_at'):
                user['created_at'] = str(user['created_at'])
            if user.get('updated_at'):
                user['updated_at'] = str(user['updated_at'])
        
        cursor.close()
        conn.close()
        
        if not user:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found"}
            )
        
        return JSONResponse(content={"success": True, "data": user})
    except Exception as e:
        print(f"Error in get_user: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/users")
def create_user(
    name: str = Query(..., description="User name"),
    email: str = Query(..., description="User email"),
    role: str = Query(default="user", description="User role"),
    status: str = Query(default="active", description="User status")
):
    """Create new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO users (name, email, role, status) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, role, status))
        conn.commit()
        
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return JSONResponse(content={
            "success": True,
            "message": "User created successfully",
            "user_id": user_id
        })
    except mysql.connector.IntegrityError as e:
        print(f"Integrity error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Email already exists"}
        )
    except Exception as e:
        print(f"Error in create_user: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.put("/api/users/{user_id}")
def update_user(
    user_id: int,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """Update user information"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        if email:
            updates.append("email = %s")
            params.append(email)
        if role:
            updates.append("role = %s")
            params.append(role)
        if status:
            updates.append("status = %s")
            params.append(status)
        
        if not updates:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "No fields to update"}
            )
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found"}
            )
        
        cursor.close()
        conn.close()
        
        return JSONResponse(content={
            "success": True,
            "message": "User updated successfully"
        })
    except Exception as e:
        print(f"Error in update_user: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    """Delete user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "User not found"}
            )
        
        cursor.close()
        conn.close()
        
        return JSONResponse(content={
            "success": True,
            "message": "User deleted successfully"
        })
    except Exception as e:
        print(f"Error in delete_user: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

# ==================== STATISTICS API ====================

@app.get("/api/stats")
def get_statistics():
    """Get dashboard statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Total users
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total = cursor.fetchone()['total']
        
        # Active users
        cursor.execute("SELECT COUNT(*) as active FROM users WHERE status = 'active'")
        active = cursor.fetchone()['active']
        
        # Users by role
        cursor.execute("""
            SELECT role, COUNT(*) as count 
            FROM users 
            GROUP BY role
        """)
        by_role = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return JSONResponse(content={
            "success": True,
            "data": {
                "total_users": total,
                "active_users": active,
                "inactive_users": total - active,
                "by_role": by_role
            }
        })
    except Exception as e:
        print(f"Error in get_statistics: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

# ==================== LEGACY ENDPOINTS (for backward compatibility) ====================

@app.get("/db/users")
def get_users_legacy():
    """Legacy endpoint - redirects to /api/users"""
    return get_all_users()

@app.get("/db/tables")
def get_tables():
    """Get all database tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        return {"tables": tables, "count": len(tables)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))