import mysql.connector as mysql

def connect_db():
    return mysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='todo_db'
    )

def create_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(255) NOT NULL,
            status ENUM('Complete', 'Incomplete') DEFAULT 'Incomplete'
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def view_tasks():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, task, status 
        FROM todos 
        ORDER BY FIELD(status, 'Incomplete', 'Complete'), id
    """)
    tasks = cursor.fetchall()
    
    if not tasks:
        print("\nNo tasks found!")
    else:
        print("\n{:<5} {:<40} {:<10}".format('ID', 'TASK', 'STATUS'))
        print("-" * 60)
        for task in tasks:
            print("{:<5} {:<40} {:<10}".format(task[0], task[1], task[2]))
    
    cursor.close()
    connection.close()

def insert_task():
    task = input("\nEnter task to add: ").strip()
    if not task:
        print("Task cannot be empty!")
        return
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    connection.commit()
    print(f"Task '{task}' added successfully!")
    cursor.close()
    connection.close()

def update_task():
    view_tasks()
    try:
        task_id = int(input("\nEnter task ID to update: "))
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = %s", (task_id,))
    if not cursor.fetchone():
        print("Task ID not found!")
        return
    print("\n1. Update task content")
    print("2. Toggle task status")
    choice = input("Choose update option (1/2): ")
    if choice == '1':
        new_task = input("Enter new task content: ").strip()
        if not new_task:
            print("Task cannot be empty!")
            return
        cursor.execute("UPDATE todos SET task = %s WHERE id = %s", (new_task, task_id))
        print("Task content updated!")
    elif choice == '2':
        cursor.execute("UPDATE todos SET status = IF(status='Complete', 'Incomplete', 'Complete') WHERE id = %s", (task_id,))
        print("Task status toggled!")
    else:
        print("Invalid choice!")
        return
    connection.commit()
    cursor.close()
    connection.close()

def delete_task():
    view_tasks()
    try:
        task_id = int(input("\nEnter task ID to delete: "))
    except ValueError:
        print("Invalid ID! Please enter a number.")
        return
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = %s", (task_id,))
    if not cursor.fetchone():
        print("Task ID not found!")
        return
    confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ").lower()
    if confirm == 'y':
        cursor.execute("DELETE FROM todos WHERE id = %s", (task_id,))
        connection.commit()
        print("Task deleted successfully!")
    else:
        print("Deletion canceled.")
    cursor.close()
    connection.close()

create_table()
while True:
    print("\nTodo List Manager")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")
    choice = input("\nEnter your choice (1-5): ")
    if choice == '1':
        view_tasks()
    elif choice == '2':
        insert_task()
    elif choice == '3':
        update_task()
    elif choice == '4':
        delete_task()
    elif choice == '5':
        print("Goodbye!")
        break
    else:
        print("Invalid choice! Please enter 1-5.")
