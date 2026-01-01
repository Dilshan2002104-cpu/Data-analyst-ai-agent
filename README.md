# 🤖 Data Analyst AI Agent

An intelligent, multi-agent AI platform that transforms how you interact with data. Ask questions in natural language and get instant insights from CSV files and SQL databases, complete with visualizations and professional PDF reports—all powered by Google's Vertex AI Gemini 2.0.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Java](https://img.shields.io/badge/Java-21+-orange.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![React](https://img.shields.io/badge/React-18-61dafb.svg)

## ✨ Key Features

### 🧠 Multi-Agent Architecture (4 Specialized Agents)
- **Orchestrator Agent**: Intelligently routes queries to the right specialist
- **CSV Analyst Agent**: Analyzes flat files with Pandas
- **SQL Agent**: Generates and executes SQL queries for MySQL/PostgreSQL
- **Report Writer Agent**: Compiles insights into professional PDF reports ⭐ NEW

### 💬 Natural Language Interface
- Ask questions in plain English—no SQL knowledge required
- Get AI-generated insights and explanations
- Automatic chart generation (Bar, Line, Pie, Area)
- One-click PDF report generation with charts and data tables

### 📊 Data Visualization
- Interactive charts powered by Recharts
- Automatic chart type selection based on query intent
- Support for time-series, categorical, and comparative visualizations
- High-quality chart embedding in PDF reports

### 💾 Multi-Source Data Analysis
- **CSV/Excel Files**: Upload and analyze spreadsheets
- **SQL Databases**: Connect to MySQL and PostgreSQL databases
- **Unified Queries**: Ask questions across multiple data sources
- **Persistent Connections**: Database connections saved to Firestore

### 🔐 Enterprise-Grade Security
- Firebase Authentication with email/password
- Account-level data isolation
- Firestore persistence for chat history and connections
- Secure credential management
- SQL injection prevention

### 🎨 Modern UI/UX
- Clean, responsive design with TailwindCSS
- Real-time chat interface
- File upload with drag-and-drop
- Database connection management
- Professional report download cards

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 5173)              │
│  • Authentication UI  • Chat Interface  • Data Management   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  Spring Backend (Port 8080)                 │
│  • Firebase Auth  • Firestore DB  • REST API  • Storage     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              Python AI Service (Port 5000)                  │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ Orchestrator │───▶│  CSV Agent   │    │  SQL Agent   │ │
│  │    Agent     │    │              │    │              │ │
│  └──────┬───────┘    └──────────────┘    └──────────────┘ │
│         │                                                  │
│         └──────────────────┐                               │
│                            ▼                               │
│                  ┌──────────────────────┐                  │
│                  │  Report Writer Agent │ ⭐ NEW           │
│                  │  (PDF Generation)    │                  │
│                  └──────────────────────┘                  │
│                            │                               │
│                            ▼                               │
│                  ┌──────────────────────┐                  │
│                  │   Vertex AI Gemini   │                  │
│                  │   (Gemini 2.0 Flash) │                  │
│                  └──────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Java 21+** (for Spring Backend)
- **Python 3.11+** (for AI Service)
- **Node.js 18+** (for React Frontend)
- **Maven** (for Spring Backend)
- **Google Cloud Project** with Vertex AI API enabled
- **Firebase Project** with Authentication, Firestore, and Storage

### 1. Clone the Repository

```bash
git clone https://github.com/Dilshan2002104-cpu/Data-analyst-ai-agent.git
cd data-analyst-ai-agent
```

### 2. Setup Credentials

Create a `credentials/` directory in the project root:

```bash
mkdir credentials
```

Place your service account keys:
- `credentials/firebase-admin-key.json` - Firebase Admin SDK key
- `credentials/vertex-ai-key.json` - Vertex AI service account key

**⚠️ IMPORTANT**: Never commit these files! They're already in `.gitignore`.

### 3. Start Spring Backend

```bash
cd spring-backend

# Configure application (edit src/main/resources/application.yml)
# Set your Firebase credentials path and project ID

# Run the application
./mvnw spring-boot:run
```

Backend runs on `http://localhost:8080`

### 4. Start Python AI Service

```bash
cd python-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable for Vertex AI credentials
# Windows:
set GOOGLE_APPLICATION_CREDENTIALS=..\credentials\vertex-ai-key.json
# macOS/Linux:
export GOOGLE_APPLICATION_CREDENTIALS=../credentials/vertex-ai-key.json

# Run the application
python app.py
```

AI Service runs on `http://localhost:5000`

### 5. Start React Frontend

```bash
cd react-frontend

# Install dependencies
npm install

# Create .env file with your Firebase config
cat > .env << EOF
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_API_BASE_URL=http://localhost:8080
EOF

# Run the application
npm run dev
```

Frontend runs on `http://localhost:5173`

## 📖 Usage Guide

### Connecting to a Database

1. Navigate to **Connect DB** in the sidebar
2. Fill in your database credentials:
   - Database Type (MySQL/PostgreSQL)
   - Host, Port, Database Name
   - Username, Password
3. Click **Test Connection** to verify
4. Click **Save & Connect** to persist the connection

### Uploading CSV Files

1. Navigate to **Dashboard**
2. Click **Upload CSV** or drag and drop a file
3. Wait for processing to complete
4. The dataset will appear in your data sources

### Asking Questions

1. Navigate to **Chat** (Unified Chat)
2. Type your question in natural language
3. The AI will automatically:
   - Detect which data source to use
   - Generate appropriate queries (SQL or Pandas code)
   - Execute the query
   - Analyze results
   - Generate visualizations if requested
   - Create PDF reports if requested

### Example Queries

#### For SQL Databases:
```
"Show me a bar chart of total sales by region"
"What are the top 10 customers by revenue?"
"Show me monthly revenue trends as a line chart"
"Compare product categories with a pie chart"
"Analyze sales by region and generate a report" ⭐ NEW
```

#### For CSV Files:
```
"What's the average value in the sales column?"
"Show me the distribution of ages"
"Find correlations between price and quantity"
"Summarize the key statistics"
```

#### Advanced Analysis:
```
"Analyze customer purchasing patterns by region and show which regions have the highest average order value"
"Compare sales performance between January and February. Which products drove the growth?"
"Provide a comprehensive business intelligence summary with charts and generate a PDF report"
```

## 🛠️ Technology Stack

### Backend (Spring Boot)
- **Spring Boot 3.4.1** - Application framework
- **Firebase Admin SDK** - Authentication & Firestore
- **Google Cloud Storage** - File storage
- **WebClient** - Reactive HTTP client
- **Maven** - Build tool

### AI Service (Python)
- **Flask** - Web framework
- **Vertex AI SDK** - Google's AI platform
- **Gemini 2.0 Flash** - Large language model
- **ChromaDB** - Vector database for semantic search
- **Pandas** - Data manipulation
- **SQLAlchemy** - SQL toolkit
- **PyMySQL/psycopg2** - Database drivers
- **ReportLab** - PDF generation ⭐ NEW
- **Matplotlib** - Chart rendering for PDFs ⭐ NEW

### Frontend (React)
- **React 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Utility-first CSS
- **Firebase SDK** - Client authentication
- **Recharts** - Chart library
- **React Router** - Navigation
- **Lucide React** - Icons

## 📁 Project Structure

```
data-analyst-ai-agent/
├── credentials/                    # Service account keys (gitignored)
│   ├── firebase-admin-key.json
│   └── vertex-ai-key.json
│
├── spring-backend/                 # Spring Boot REST API
│   ├── src/main/java/com/dataanalyst/backend/
│   │   ├── config/                # Configuration classes
│   │   ├── controller/            # REST controllers
│   │   ├── dto/                   # Data transfer objects
│   │   ├── model/                 # Domain models
│   │   └── service/               # Business logic
│   ├── src/main/resources/
│   │   └── application.yml        # Application config
│   └── pom.xml
│
├── python-backend/                 # Python AI Service
│   ├── routes/                    # Flask routes
│   │   ├── csv.py                # CSV upload/query endpoints
│   │   ├── sql.py                # SQL connection/query endpoints
│   │   ├── unified.py            # Unified query endpoint
│   │   └── reports.py            # Report generation endpoints ⭐ NEW
│   ├── services/                  # Business logic
│   │   ├── agent.py              # CSV Analyst Agent
│   │   ├── sql_agent.py          # SQL Agent
│   │   ├── orchestrator.py       # Orchestrator Agent
│   │   ├── report_writer_agent.py # Report Writer Agent ⭐ NEW
│   │   ├── vertex_ai_service.py  # Vertex AI integration
│   │   ├── chromadb_service.py   # Vector database
│   │   ├── firestore_service.py  # Firestore integration
│   │   └── context_manager.py    # User context management
│   ├── reports/                   # Generated PDF reports ⭐ NEW
│   ├── app.py                     # Flask application
│   └── requirements.txt
│
├── react-frontend/                 # React SPA
│   ├── src/
│   │   ├── components/            # Reusable components
│   │   ├── contexts/              # React contexts
│   │   ├── pages/                 # Page components
│   │   ├── config/                # Configuration
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── MULTI_AGENT_ARCHITECTURE.md    # Architecture documentation
├── test_database_mysql.sql        # Sample test database
└── README.md
```

## 🎯 Multi-Agent System

### How It Works

The system uses an **Orchestrator Pattern** where a central agent coordinates specialist agents:

1. **User Query** → Orchestrator Agent
2. **Orchestrator** analyzes the query and determines:
   - Which data source(s) to use (CSV, SQL, or both)
   - Which specialist agent(s) to invoke
   - Whether to generate a PDF report
3. **Specialist Agents** execute their tasks:
   - **CSV Agent**: Generates Python/Pandas code
   - **SQL Agent**: Generates SQL queries
   - **Report Writer**: Compiles PDF reports ⭐ NEW
4. **Results** are analyzed and formatted
5. **Response** includes insights, visualizations, and optional PDF download

### Agent Capabilities

#### Orchestrator Agent
- Natural language understanding
- Source detection and routing
- Multi-source query coordination
- Report generation detection ⭐ NEW

#### CSV Analyst Agent
- Pandas code generation
- Statistical analysis
- Data cleaning and transformation

#### SQL Agent
- SQL query generation (MySQL/PostgreSQL)
- Schema understanding
- Join optimization
- Date formatting (database-specific)

#### Report Writer Agent ⭐ NEW
- Professional PDF generation with ReportLab
- Chart embedding via Matplotlib
- Data table formatting with pagination
- Executive summary sections
- Automatic report generation on user request

## 📄 PDF Report Features ⭐ NEW

Generated reports include:

### Title Page
- Report title
- User query
- Generation date and time
- Data source information

### Executive Summary
- AI-generated insights
- Key findings
- Statistical highlights

### Detailed Analysis
- Original query
- Data source details
- Record count

### Visualizations
- Charts embedded as high-quality images
- Proper scaling and formatting
- Support for bar, line, pie, and area charts

### Data Tables
- First 20 rows of results
- Professional table styling
- Column headers
- Pagination note if data is truncated

### Footer
- Page numbers
- "Generated by Data Analyst AI Agent" branding

## 🔒 Security Best Practices

1. **Credentials**: Never commit service account keys
2. **Environment Variables**: Use `.env` files for configuration
3. **Firebase Rules**: Implement proper Firestore security rules
4. **SQL Injection**: All queries are validated and parameterized
5. **CORS**: Configure allowed origins properly
6. **Authentication**: All API endpoints require valid Firebase tokens

## 🧪 Testing

### Test Database Setup

A sample MySQL database is provided in `test_database_mysql.sql`:

```bash
mysql -u root -p < test_database_mysql.sql
```

This creates a `sales_test_db` with sample data for testing.

### Example Test Queries

```
"Show me total revenue by region"
"What are the top selling products?"
"Show me monthly sales trends"
"Which customers have the highest order values?"
"Analyze sales by region and generate a professional report"
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: "429 Quota Exceeded" error
- **Solution**: Wait 1-2 minutes between requests. Vertex AI has rate limits.

**Issue**: Charts not rendering
- **Solution**: Ensure the Python backend has been restarted after code changes.

**Issue**: SQL queries failing with date formatting errors
- **Solution**: Restart Python backend to apply MySQL-specific date formatting.

**Issue**: "Connection not found" error
- **Solution**: The connection was saved in Firestore but Python backend needs restart to sync.

**Issue**: PDF report not downloading
- **Solution**: Check `python-backend/reports/` directory or access directly via `/api/reports/download/<filename>`

## 📝 API Documentation

### Spring Backend Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

#### Datasets
- `POST /api/datasets/upload` - Upload CSV file
- `GET /api/datasets/{userId}` - Get user's datasets

#### SQL Connections
- `POST /api/connections` - Save SQL connection
- `GET /api/connections/{userId}` - Get user's connections
- `DELETE /api/connections/{connectionId}` - Delete connection

#### Chat
- `POST /api/chat` - Save chat message
- `GET /api/chat/{datasetId}` - Get chat history

### Python AI Service Endpoints

#### CSV Operations
- `POST /api/csv/upload` - Process CSV file
- `POST /api/csv/query` - Query CSV data

#### SQL Operations
- `POST /api/sql/test-connection` - Test database connection
- `POST /api/sql/connect` - Create database connection
- `POST /api/sql/query` - Execute SQL query
- `GET /api/sql/sources/{userId}` - Get data sources

#### Unified Interface
- `POST /api/unified/query` - Unified query endpoint (auto-routes)

#### Reports ⭐ NEW
- `POST /api/reports/generate` - Generate PDF report
- `GET /api/reports/download/<filename>` - Download specific report
- `GET /api/reports/list` - List all available reports

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud Vertex AI for the Gemini 2.0 model
- Firebase for authentication and storage
- The open-source community for amazing tools and libraries

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using AI-powered development**

⭐ Star this repo if you find it useful!
