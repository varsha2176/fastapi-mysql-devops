from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
import os
import time

app = FastAPI(title="FastAPI MySQL DevOps Demo")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Create database connection with retry logic"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "db"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "rootpassword"),
                database=os.getenv("MYSQL_DATABASE", "fastapidb"),
                port=int(os.getenv("MYSQL_PORT", "3306"))
            )
            if connection.is_connected():
                return connection
        except Error as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    
    raise HTTPException(status_code=500, detail="Database connection failed after retries")

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "FastAPI + MySQL DevOps Project",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    """Detailed health check with database status"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        connection.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "api": "running"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/db/tables")
def get_tables():
    """Get all tables from database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return {
            "status": "success",
            "tables": [table[0] for table in tables],
            "count": len(tables)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db/users")
def get_users():
    """Get all users from demo table"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return {
            "status": "success",
            "users": users,
            "count": len(users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/db/users")
def create_user(name: str, email: str):
    """Create a new user"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {
            "status": "success",
            "message": "User created successfully",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)