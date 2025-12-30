# System Architecture: Data Analyst AI Agent 🏗️

This diagram illustrates the complete flow of the application as it is currently implemented.

```mermaid
graph TD
    subgraph Frontend [React Frontend 💻]
        UI[User Interface]
        Chart[Chart Renderer 📊]
        Auth[Firebase Auth 🔐]
    end

    subgraph Backend_Java [Spring Boot Backend 🍃]
        API_Gateway[API Controller]
        Sec[Security Filter]
        Service_FB[Firebase Service]
    end

    subgraph Backend_Python [Python AI Service 🐍]
        Flask[Flask API]
        RAG[RAG Processor]
        Chroma[(ChromaDB 📚)]
    end

    subgraph Cloud_Services [Cloud Services ☁️]
        Google[Vertex AI (Gemini) 🧠]
        Firebase[Firebase Storage 📁]
        Firestore[Firestore DB 🗄️]
    end

    %% Flows
    UI -->|1. Login/Auth| Auth
    UI -->|2. Upload CSV| API_Gateway
    API_Gateway -->|3. Store Metadata| Firestore
    API_Gateway -->|4. Store File| Firebase
    
    API_Gateway -->|5. Trigger Processing| Flask
    Flask -->|6. Download File| Firebase
    Flask -->|7. Generate Embeddings| Google
    Flask -->|8. Store Vectors| Chroma

    UI -->|9. Ask Question| API_Gateway
    API_Gateway -->|10. Forward Query| Flask
    Flask -->|11. Search Context| Chroma
    Flask -->|12. Generate Answer + JSON| Google
    Flask -->|13. Return Response| API_Gateway
    API_Gateway -->|14. Return Response| UI
    
    UI -->|15. Render Text & Chart| Chart
```

## Component Roles
1.  **React Frontend**: Handles UI, Auth, and visualizing Charts.
2.  **Spring Boot**: The "Gatekeeper". Manages users, permissions, and file flows.
3.  **Python Service**: The "Brain". Handles Vector Search (Chroma) and AI Generation (Gemini).
4.  **ChromaDB**: The "Memory". Stores vector embeddings of your data.
5.  **Vertex AI**: The "Intelligence". Generates the answers and chart configurations.
