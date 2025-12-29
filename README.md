# Data Analyst AI Agent

An AI-powered data analytics platform that allows users to upload datasets and query them using natural language, powered by Google's Vertex AI Gemini 2.0 Flash.

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │ (Port 5173)
│  - Authentication│
│  - File Upload  │
│  - Chat UI      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Spring Backend  │ (Port 8080)
│  - Firebase Auth│
│  - Firestore DB │
│  - File Storage │
│  - API Gateway  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Python AI       │◄────►│  Vertex AI   │
│  - Flask API    │      │  Gemini 2.0  │
│  - ChromaDB     │      └──────────────┘
│  - Data Process │
└─────────────────┘
```

## 🚀 Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **Multi-format Support**: Upload CSV, Excel files
- **AI-Powered Insights**: Powered by Vertex AI Gemini 2.0 Flash
- **Semantic Search**: ChromaDB for intelligent data retrieval
- **Chat History**: Persistent conversation history
- **Secure Authentication**: Firebase Authentication
- **Cloud Storage**: Firebase Storage for datasets

## 📋 Prerequisites

- **Java 21+** (for Spring Backend)
- **Python 3.11+** (for AI Service)
- **Node.js 18+** (for React Frontend)
- **Maven** (for Spring Backend)
- **Google Cloud Project** with Vertex AI enabled
- **Firebase Project** with Authentication, Firestore, and Storage enabled

## 🔧 Setup Instructions

### 1. Credentials Setup

**IMPORTANT**: Never commit credentials to version control!

Place your service account keys in the `credentials/` directory:
- `credentials/firebase-admin-key.json` - Firebase Admin SDK key
- `credentials/vertex-ai-key.json` - Vertex AI service account key

### 2. Spring Backend Setup

```bash
cd spring-backend

# Create .env file
cat > .env << EOF
FIREBASE_CREDENTIALS_PATH=../credentials/firebase-admin-key.json
GCP_PROJECT_ID=data-analyst-ai-agent-c0808
PYTHON_SERVICE_URL=http://localhost:5000
EOF

# Run the application
./mvnw spring-boot:run
```

Backend will start on `http://localhost:8080`

### 3. Python AI Service Setup

```bash
cd python-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GOOGLE_APPLICATION_CREDENTIALS=../credentials/vertex-ai-key.json
GCP_PROJECT_ID=data-analyst-ai-agent-c0808
GCP_LOCATION=us-central1
CHROMADB_PERSIST_DIR=./chromadb_data
EOF

# Run the application
python app.py
```

AI Service will start on `http://localhost:5000`

### 4. React Frontend Setup

```bash
cd react-frontend

# Install dependencies
npm install

# Create .env file
cat > .env << EOF
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=data-analyst-ai-agent-c0808.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=data-analyst-ai-agent-c0808
VITE_FIREBASE_STORAGE_BUCKET=data-analyst-ai-agent-c0808.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_API_BASE_URL=http://localhost:8080
EOF

# Run the application
npm run dev
```

Frontend will start on `http://localhost:5173`

## 🎯 Usage

1. **Sign Up/Login**: Create an account or login with existing credentials
2. **Upload Dataset**: Upload a CSV or Excel file
3. **Ask Questions**: Type natural language questions about your data
4. **View Insights**: Get AI-generated insights and visualizations

### Example Queries

- "What are the top 5 products by revenue?"
- "Show me sales trends over the last 6 months"
- "Which region has the highest growth rate?"
- "Summarize the key insights from this dataset"

## 🛠️ Tech Stack

### Backend
- **Spring Boot 3.4.1** - REST API framework
- **Firebase Admin SDK** - Authentication & Database
- **Google Cloud Storage** - File storage
- **WebClient** - HTTP client for Python service

### AI Service
- **Flask** - Python web framework
- **Vertex AI** - Google's AI platform (Gemini 2.0 Flash)
- **ChromaDB** - Vector database for embeddings
- **Pandas** - Data processing

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Firebase SDK** - Authentication
- **Axios** - HTTP client
- **Recharts** - Data visualization

## 📁 Project Structure

```
data-analyst-ai-agent/
├── credentials/              # Service account keys (gitignored)
├── spring-backend/          # Spring Boot backend
│   ├── src/main/java/
│   └── pom.xml
├── python-backend/          # Python AI service
│   ├── services/
│   ├── routes/
│   ├── app.py
│   └── requirements.txt
├── react-frontend/          # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔒 Security Notes

1. **Never commit credentials** - Always use environment variables
2. **Rotate keys regularly** - Especially if accidentally exposed
3. **Use Firebase Security Rules** - Restrict access to user's own data
4. **Enable CORS properly** - Only allow trusted origins
5. **Validate all inputs** - Both frontend and backend

## 🧪 Testing

### Spring Backend
```bash
cd spring-backend
./mvnw test
```

### Python Service
```bash
cd python-backend
pytest tests/
```

### Frontend
```bash
cd react-frontend
npm test
```

## 📝 License

MIT License - feel free to use for personal or commercial projects

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues or questions, please open a GitHub issue.
