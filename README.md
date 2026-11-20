# OpsBoard — DevOps Operations Dashboard

A modern, dark-themed task management dashboard built with **Python Flask** to organize and track real-world DevOps engineering activities.

OpsBoard provides a centralized workspace for managing tasks related to AWS, Jenkins, Docker, Kubernetes, Linux, CI/CD, Terraform, and infrastructure monitoring.

The project also serves as a practical application for learning and implementing DevOps workflows, including Docker containerization, Jenkins CI/CD automation, and AWS deployment.

## Dashboard Preview

A dark-themed dashboard featuring task statistics, completion progress, priority indicators, category filters, and task management capabilities.

## Features

### Task Management
- Create, edit, and delete tasks.
- Update task status: To Do, In Progress, and Completed.
- Assign priorities: Low, Medium, High, and Critical.
- Organize tasks by engineering categories.
- Set due dates and track overdue tasks.
- Add descriptions and task details.

### Dashboard & Analytics
- Total task count.
- In-progress and completed task statistics.
- Overdue task tracking.
- Overall task completion percentage.
- Visual progress indicators.

### Search & Filtering
- Search tasks by title or description.
- Filter by task status.
- Filter by engineering category.
- Filter by priority.

### Backend & API
- RESTful API endpoints.
- SQLite database integration.
- Automatic database initialization.
- Sample DevOps tasks seeded on first launch.
- Application and database health-check endpoint.

### User Interface
- Modern dark-themed interface.
- Responsive dashboard layout.
- Sidebar navigation.
- Interactive task management.
- Status and priority indicators.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| API | REST |
| Containerization | Docker |
| Version Control | Git, GitHub |
| CI/CD (Planned) | Jenkins |
| Cloud Deployment (Planned) | AWS |

## Application Architecture

```text
             User / Browser
                    |
                    v
          Flask Web Application
                    |
          +---------+---------+
          |                   |
          v                   v
     HTML / CSS / JS      REST API
                              |
                              v
                         Flask Backend
                              |
                              v
                         SQLite Database
```

## Project Structure

```text
OpsBoard/
│
├── app.py
│
├── templates/
│   └── index.html
│
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
└── tasks.db
```

**Note:** `tasks.db` is generated automatically when the application starts. It should not be committed to GitHub.

## Getting Started

### Prerequisites

Make sure the following tools are installed:

- Python 3.10 or later
- Git
- Docker (optional, for containerized execution)

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/OpsBoard.git

cd OpsBoard
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -m venv .venv

.\\.venv\\Scripts\\Activate.ps1
```

**Linux:**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Application

```bash
python app.py
```

Open the application in your browser:

http://localhost:5000

The SQLite database will be initialized automatically, with sample DevOps tasks populated on the first launch.

## Docker Deployment

OpsBoard can also be packaged and executed as a Docker container.

### 1. Build the Docker Image

```bash
docker build -t opsboard .
```

### 2. Run the Container

```bash
docker run -d \
  --name opsboard \
  -p 5000:5000 \
  -e DATABASE_PATH=/app/data/tasks.db \
  -v opsboard-data:/app/data \
  opsboard
```

### 3. Verify the Container

```bash
docker ps

docker logs opsboard
```

Open:

http://localhost:5000

### 4. Verify Application Health

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "application": "devops-operations-dashboard",
  "database": "connected",
  "status": "healthy"
}
```

The Docker named volume ensures that task data persists even when the container is removed and recreated.

## REST API Documentation

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application and database health |
| GET | `/api/tasks` | Retrieve all tasks |
| GET | `/api/stats` | Retrieve dashboard statistics |
| POST | `/api/tasks` | Create a new task |
| PATCH | `/api/tasks/<id>` | Update an existing task |
| DELETE | `/api/tasks/<id>` | Delete a task |

### Supported Query Parameters

The task listing endpoint supports:

- `status` — Filter by task status.
- `category` — Filter by engineering category.
- `search` — Search task titles and descriptions.

Example:

```bash
curl "http://localhost:5000/api/tasks?status=in_progress&category=AWS"
```

### Create a Task

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Deploy application on AWS ECS",
    "description": "Deploy the containerized application using ECS Fargate",
    "category": "AWS",
    "priority": "high",
    "due_date": "2026-12-15"
  }'
```

### Update Task Status

```bash
curl -X PATCH http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## Database

OpsBoard uses SQLite for lightweight and persistent task storage.

The database is automatically initialized with the following task attributes:

- Task ID
- Title
- Description
- Category
- Priority
- Status
- Due date
- Creation timestamp
- Last updated timestamp

Task information is retained across application restarts.

## DevOps Implementation Roadmap

The project is designed to evolve into a complete CI/CD and AWS deployment exercise.

| Phase | Planned Implementation |
|---|----------------------------|
| 1 | Application development and local testing |
| 2 | GitHub repository and branching strategy |
| 3 | Docker image creation and container testing |
| 4 | Jenkins installation and configuration |
| 5 | Jenkins declarative CI/CD pipeline |
| 6 | Automated testing and Docker image publishing |
| 7 | AWS ECR integration |
| 8 | Application deployment on AWS ECS |
| 9 | Infrastructure provisioning using Terraform |
| 10 | CloudWatch monitoring and logging |
| 11 | Deployment failure handling and rollback |

## Learning Objectives

Through this project, the goal is to gain practical experience with:

- Building and managing a Python web application.
- Working with REST APIs and databases.
- Writing Dockerfiles and managing containers.
- Configuring Jenkins pipelines.
- Automating application builds and deployments.
- Integrating Jenkins with GitHub and AWS.
- Managing container images using Amazon ECR.
- Deploying applications on AWS.
- Monitoring application health and troubleshooting deployment failures.

## Future Enhancements

- PostgreSQL database integration.
- User authentication and role-based access control.
- Automated unit and integration testing.
- Jenkins CI/CD pipeline implementation.
- AWS ECS deployment with Terraform.
- CloudWatch dashboards and alarms.
- Application logging and monitoring.
- Automated deployment rollback.

## Author

**Sohan Gurav**

