# ========================================
# METHOD 1: Built-in HTTP Server (Python 3)
# ========================================

# Simple one-liner to serve current directory:
# python -m http.server 8000

# For more control, create a custom server:
import http.server
import socketserver
from pathlib import Path


def simple_file_server(port=8000):
    """Simple file server using built-in modules"""
    handler = http.server.SimpleHTTPRequestHandler

    # Serve from current directory
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving files at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


# ========================================
# METHOD 2: Custom HTTP Server
# ========================================

import http.server
import json
import urllib.parse
from datetime import datetime


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_home_page()
        elif self.path == '/api/time':
            self.send_json({'current_time': datetime.now().isoformat()})
        elif self.path == '/api/status':
            self.send_json({'status': 'running', 'server': 'Custom Python Server'})
        elif self.path.startswith('/hello/'):
            name = self.path.split('/')[-1]
            self.send_json({'message': f'Hello, {name}!'})
        else:
            self.send_404()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/echo':
            # Read POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                response = {'echo': data, 'timestamp': datetime.now().isoformat()}
                self.send_json(response)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
        else:
            self.send_404()

    def send_home_page(self):
        """Send HTML home page"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Custom Python Server</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .endpoint { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
                code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>🐍 Custom Python Web Server</h1>
            <p>Server is running! Try these endpoints:</p>

            <div class="endpoint">
                <strong>GET /api/time</strong> - Get current server time
            </div>
            <div class="endpoint">
                <strong>GET /api/status</strong> - Get server status
            </div>
            <div class="endpoint">
                <strong>GET /hello/YourName</strong> - Get personal greeting
            </div>
            <div class="endpoint">
                <strong>POST /api/echo</strong> - Echo back JSON data
            </div>

            <h3>Test with curl:</h3>
            <code>curl http://localhost:8000/api/time</code><br><br>
            <code>curl -X POST -H "Content-Type: application/json" -d '{"test": "hello"}' http://localhost:8000/api/echo</code>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def send_json(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_404(self):
        """Send 404 error"""
        self.send_error(404, "Page not found")


def custom_server(port=8000):
    """Run custom HTTP server"""
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Custom server running at http://localhost:{port}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


# ========================================
# METHOD 3: Flask Web Server
# ========================================

# First install Flask: pip install flask

def create_flask_app():
    """Create a Flask web application"""
    try:
        from flask import Flask, jsonify, request, render_template_string

        app = Flask(__name__)

        # Store some data in memory
        todos = [
            {'id': 1, 'task': 'Learn Python', 'completed': True},
            {'id': 2, 'task': 'Build a web server', 'completed': False}
        ]

        @app.route('/')
        def home():
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Flask Server</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                    .todo { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 8px; }
                    .completed { background: #d4edda; }
                    button { padding: 8px 16px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
                    .btn-primary { background: #007bff; color: white; }
                    .btn-success { background: #28a745; color: white; }
                </style>
            </head>
            <body>
                <h1>🚀 Flask Web Server</h1>
                <h2>Todo List</h2>
                <div id="todos"></div>

                <h3>Add New Todo</h3>
                <input type="text" id="newTodo" placeholder="Enter task...">
                <button class="btn-primary" onclick="addTodo()">Add</button>

                <script>
                    async function loadTodos() {
                        const response = await fetch('/api/todos');
                        const todos = await response.json();
                        const container = document.getElementById('todos');
                        container.innerHTML = todos.map(todo => 
                            `<div class="todo ${todo.completed ? 'completed' : ''}">
                                <strong>${todo.task}</strong>
                                <button class="btn-success" onclick="toggleTodo(${todo.id})">
                                    ${todo.completed ? 'Undo' : 'Complete'}
                                </button>
                            </div>`
                        ).join('');
                    }

                    async function addTodo() {
                        const task = document.getElementById('newTodo').value;
                        if (!task) return;

                        await fetch('/api/todos', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({task: task})
                        });

                        document.getElementById('newTodo').value = '';
                        loadTodos();
                    }

                    async function toggleTodo(id) {
                        await fetch(`/api/todos/${id}/toggle`, {method: 'POST'});
                        loadTodos();
                    }

                    loadTodos();
                </script>
            </body>
            </html>
            """
            return render_template_string(html_template)

        @app.route('/api/todos', methods=['GET'])
        def get_todos():
            return jsonify(todos)

        @app.route('/api/todos', methods=['POST'])
        def add_todo():
            data = request.get_json()
            new_todo = {
                'id': max([t['id'] for t in todos]) + 1 if todos else 1,
                'task': data['task'],
                'completed': False
            }
            todos.append(new_todo)
            return jsonify(new_todo)

        @app.route('/api/todos/<int:todo_id>/toggle', methods=['POST'])
        def toggle_todo(todo_id):
            todo = next((t for t in todos if t['id'] == todo_id), None)
            if todo:
                todo['completed'] = not todo['completed']
                return jsonify(todo)
            return jsonify({'error': 'Todo not found'}), 404

        return app

    except ImportError:
        print("Flask not installed. Install with: pip install flask")
        return None


def run_flask_server():
    """Run Flask server"""
    app = create_flask_app()
    if app:
        print("Flask server starting at http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)


# ========================================
# METHOD 4: FastAPI Server (Modern, Fast)
# ========================================

def create_fastapi_app():
    """Create a FastAPI application"""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.responses import HTMLResponse
        from pydantic import BaseModel
        import uvicorn

        app = FastAPI(title="FastAPI Server", version="1.0.0")

        # Data models
        class TodoCreate(BaseModel):
            task: str

        class Todo(BaseModel):
            id: int
            task: str
            completed: bool

        # In-memory storage
        todos_db = [
            Todo(id=1, task="Learn FastAPI", completed=False),
            Todo(id=2, task="Build amazing APIs", completed=False)
        ]

        @app.get("/", response_class=HTMLResponse)
        def home():
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>FastAPI Server</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                    .card { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #007bff; }
                </style>
            </head>
            <body>
                <h1>⚡ FastAPI Web Server</h1>
                <div class="card">
                    <h3>Interactive API Documentation</h3>
                    <p>Visit <a href="/docs">/docs</a> for Swagger UI</p>
                    <p>Visit <a href="/redoc">/redoc</a> for ReDoc</p>
                </div>
                <div class="card">
                    <h3>Available Endpoints</h3>
                    <ul>
                        <li>GET /api/todos - List all todos</li>
                        <li>POST /api/todos - Create new todo</li>
                        <li>GET /api/todos/{id} - Get specific todo</li>
                        <li>DELETE /api/todos/{id} - Delete todo</li>
                    </ul>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content)

        @app.get("/api/todos", response_model=list[Todo])
        def get_todos():
            return todos_db

        @app.post("/api/todos", response_model=Todo)
        def create_todo(todo: TodoCreate):
            new_id = max([t.id for t in todos_db]) + 1 if todos_db else 1
            new_todo = Todo(id=new_id, task=todo.task, completed=False)
            todos_db.append(new_todo)
            return new_todo

        @app.get("/api/todos/{todo_id}", response_model=Todo)
        def get_todo(todo_id: int):
            todo = next((t for t in todos_db if t.id == todo_id), None)
            if not todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return todo

        @app.delete("/api/todos/{todo_id}")
        def delete_todo(todo_id: int):
            global todos_db
            todos_db = [t for t in todos_db if t.id != todo_id]
            return {"message": "Todo deleted"}

        return app

    except ImportError:
        print("FastAPI not installed. Install with: pip install fastapi uvicorn")
        return None


def run_fastapi_server():
    """Run FastAPI server"""
    app = create_fastapi_app()
    if app:
        import uvicorn
        print("FastAPI server starting at http://localhost:8000")
        print("API docs available at http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000)


# ========================================
# MAIN MENU
# ========================================

def main():
    """Main menu to choose server type"""
    print("🐍 Python Web Server Examples")
    print("=" * 40)
    print("1. Simple File Server (built-in)")
    print("2. Custom HTTP Server")
    print("3. Flask Web Server (install flask)")
    print("4. FastAPI Server (install fastapi uvicorn)")
    print("5. Exit")

    while True:
        try:
            choice = input("\nChoose a server type (1-5): ").strip()

            if choice == '1':
                simple_file_server()
                break
            elif choice == '2':
                custom_server()
                break
            elif choice == '3':
                run_flask_server()
                break
            elif choice == '4':
                run_fastapi_server()
                break
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()