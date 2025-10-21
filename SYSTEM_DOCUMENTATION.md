# Market Research AI - Complete System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Backend Architecture](#backend-architecture)
3. [Multi-Agent System](#multi-agent-system)
4. [RAG Pipeline](#rag-pipeline)
5. [API Layer](#api-layer)
6. [Frontend Architecture](#frontend-architecture)
7. [Data Flow](#data-flow)
8. [Deployment](#deployment)

---

## System Overview

### Core Technology Stack
- **Backend**: Python FastAPI + CrewAI + LangChain + ChromaDB
- **Frontend**: React TypeScript + Tailwind CSS + Zustand
- **LLM**: Google Gemini 2.0 with intelligent model routing
- **Vector Database**: ChromaDB with Google embeddings
- **Deployment**: Docker on Render (backend) + Vercel (frontend)

### Key Capabilities
- Multi-agent market research execution
- RAG-enhanced knowledge integration
- Real-time progress tracking
- Professional PDF report generation
- Knowledge base management
- User authentication and session management

---

## Backend Architecture

### Project Structure
```
marketresearch/
├── api/                    # FastAPI application
│   ├── main.py            # Application entry point
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   └── models.py          # Pydantic data models
├── src/marketresearch/    # Core research system
│   ├── crew.py           # CrewAI multi-agent setup
│   ├── config/           # Agent and task configurations
│   ├── tools/            # Custom research tools
│   ├── rag/              # RAG pipeline components
│   ├── prompts/          # Advanced prompt engineering
│   └── utils/            # Utility functions
└── requirements.txt       # Python dependencies
```

### Core Services

#### Research Service (`api/services/research_service.py`)
- **Purpose**: Manages research execution lifecycle
- **Key Methods**:
  - `execute_research()`: Orchestrates multi-agent research workflow
  - `update_research_status()`: Tracks research progress states
  - `update_task_progress()`: Monitors individual agent tasks
  - `get_research()`: Retrieves research results by ID
  - `check_pdf_exists()`: Validates PDF report availability

#### Knowledge Service (`api/services/knowledge_service.py`)
- **Purpose**: Handles document management and RAG operations
- **Key Methods**:
  - `upload_document()`: Processes and stores uploaded files
  - `get_stats()`: Returns knowledge base statistics
  - `get_rag_factory()`: Initializes RAG pipeline

---

## Multi-Agent System

### CrewAI Framework Implementation

#### Agent Definitions (`src/marketresearch/crew.py`)

**1. Digital Intelligence Gatherer**
- **Role**: Primary data collection and competitor analysis
- **Tools**: All research tools + chain tools
- **LLM**: Task-optimized Gemini model for data collection
- **Responsibilities**:
  - Market landscape mapping
  - Competitor intelligence gathering
  - Industry trend identification
  - Data quality validation

**2. Quantitative Insights Specialist**
- **Role**: Analytical processing and pattern recognition
- **Tools**: SWOT analysis, benchmarking, statistical tools
- **LLM**: Analysis-optimized Gemini model
- **Responsibilities**:
  - SWOT analysis generation
  - Competitive benchmarking
  - Statistical analysis
  - Risk assessment

**3. Strategic Communications Expert**
- **Role**: Report generation and strategic recommendations
- **Tools**: Report formatting, visualization tools
- **LLM**: Communication-optimized Gemini model
- **Responsibilities**:
  - Executive summary creation
  - Strategic recommendation formulation
  - Professional report formatting
  - Stakeholder communication optimization

**4. Senior Research Director**
- **Role**: Quality assurance and executive oversight
- **LLM**: Executive-level Gemini model
- **Responsibilities**:
  - Research quality validation
  - Strategic alignment verification
  - Executive-level insights
  - Final report approval

### Task Configuration (`src/marketresearch/config/tasks.yaml`)

**Sequential Task Execution:**
1. **Comprehensive Data Collection Task**
   - Duration: ~30-45 minutes
   - Output: Raw market data and competitor intelligence
   - Dependencies: None (entry point)

2. **Comprehensive Analysis Task**
   - Duration: ~20-30 minutes
   - Output: SWOT analysis and strategic insights
   - Dependencies: Data collection results

3. **Final Comprehensive Report Task**
   - Duration: ~15-20 minutes
   - Output: Professional PDF report
   - Dependencies: All previous task outputs

### Agent Coordination
- **Process**: Sequential execution with context passing
- **Memory**: Custom conversation buffer for context retention
- **Progress Tracking**: Real-time status updates via research service
- **Error Handling**: Graceful failure recovery with detailed logging

---

## RAG Pipeline

### ChromaDB Vector Storage (`src/marketresearch/rag/chroma_store.py`)

**Configuration:**
- **Storage Path**: Environment-configurable location
- **Embedding Model**: Google Gemini embeddings API
- **Collection Management**: Automatic collection creation and management
- **Persistence**: Disk-based storage for data retention

**Key Methods:**
- `add_documents()`: Processes and stores document chunks
- `similarity_search()`: Retrieves relevant context for queries
- `get_stats()`: Returns collection statistics and document counts

### Google Embeddings Integration (`src/marketresearch/rag/google_embeddings.py`)

**Implementation:**
- **Model**: Google Generative AI embeddings
- **Dimension**: 768-dimensional vectors
- **Batch Processing**: Efficient handling of multiple documents
- **Error Handling**: Robust API error management

### RAG Chain Factory (`src/marketresearch/rag_chain_factory.py`)

**Components:**
- **Document Loader**: Multi-format file processing (PDF, TXT, MD)
- **Text Splitter**: Intelligent chunking for optimal retrieval
- **Vector Store**: ChromaDB integration with Google embeddings
- **Retrieval Chain**: LangChain-based question-answering system

**Research Enhancement:**
- **Context Injection**: Automatic relevant document retrieval
- **Query Augmentation**: Enhanced prompts with contextual information
- **Source Attribution**: Tracking of information sources
- **Quality Scoring**: Relevance scoring for retrieved content

---

## API Layer

### FastAPI Application (`api/main.py`)

**Configuration:**
- **CORS**: Configured for frontend domains (localhost + production)
- **Middleware**: Request/response processing and error handling
- **Startup Events**: Service initialization and health checks
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### Authentication System (`api/auth.py`)

**Implementation:**
- **Method**: Simple token-based authentication for development
- **JWT Support**: Ready for production JWT implementation
- **User Profiles**: Basic user management with ID and metadata
- **Security**: Token validation on protected endpoints

### API Endpoints

#### Research Routes (`api/routes/research.py`)

**POST /research/start**
- **Purpose**: Initiates new research session
- **Input**: Research topic and detailed request
- **Output**: Research ID and initial progress structure
- **Process**: Creates background task for multi-agent execution

**GET /research/{research_id}/status**
- **Purpose**: Real-time progress monitoring
- **Output**: Current research status, agent progress, completion percentage
- **Polling**: Frontend polls this endpoint for live updates

**GET /research/{research_id}/result**
- **Purpose**: Retrieves completed research results
- **Output**: Full research text, completion timestamp, PDF availability
- **Validation**: Ensures research is completed before access

**GET /research/{research_id}/preview-pdf**
- **Purpose**: In-browser PDF preview
- **Output**: PDF file with inline content disposition
- **Usage**: Embedded in frontend iframe for preview

**GET /research/{research_id}/download-pdf**
- **Purpose**: PDF file download
- **Output**: PDF file with attachment disposition
- **Features**: Proper filename and content type headers

#### Knowledge Routes (`api/routes/knowledge.py`)

**POST /knowledge/upload**
- **Purpose**: Document upload for RAG enhancement
- **Input**: Multipart file upload (PDF, TXT, MD)
- **Process**: File validation, processing, vector storage
- **Output**: Upload confirmation and processing status

**GET /knowledge/stats**
- **Purpose**: Knowledge base statistics
- **Output**: Document counts, categories, last update timestamp
- **Usage**: Dashboard analytics and system monitoring

### Data Models (`api/models.py`)

**Core Models:**
- `ResearchRequest`: Input validation for research initiation
- `ResearchResponse`: Complete research session data structure
- `ResearchProgress`: Real-time progress tracking information
- `TaskProgress`: Individual agent task status and metadata
- `UserProfile`: User authentication and profile data
- `KnowledgeStats`: Knowledge base metrics and statistics

---

## Frontend Architecture

### React TypeScript Application

**Project Structure:**
```
frontend/src/
├── components/           # Reusable UI components
│   ├── ui/              # Base UI components
│   └── research/        # Research-specific components
├── pages/               # Main application pages
├── store/               # Zustand state management
├── hooks/               # Custom React hooks
└── types/               # TypeScript type definitions
```

### State Management (`src/store/`)

#### Research Store (`useResearchStore.ts`)
- **Purpose**: Manages research sessions and results
- **Features**:
  - Research initiation and progress tracking
  - Result storage with localStorage persistence
  - History management and analytics integration
  - Real-time status polling

#### Analytics Store (`useAnalyticsStore.ts`)
- **Purpose**: Tracks user behavior and system metrics
- **Features**:
  - Research completion statistics
  - Download tracking
  - Usage pattern analysis
  - Performance metrics

### Key Components

#### Research Dashboard (`src/pages/ResearchPage.tsx`)
- **Purpose**: Main research interface
- **Features**:
  - Research topic input and validation
  - Real-time progress visualization
  - Agent status monitoring
  - Error handling and user feedback

#### Progress Dashboard (`src/components/research/ProgressDashboard.tsx`)
- **Purpose**: Live research progress tracking
- **Features**:
  - Agent activity visualization
  - Task completion indicators
  - Progress percentage display
  - Estimated completion time

#### Reports Management (`src/pages/ReportsPage.tsx`)
- **Purpose**: Research results management
- **Features**:
  - Report listing and organization
  - PDF preview and download
  - Sharing capabilities
  - Analytics integration

#### PDF Preview Modal (`src/components/ui/PDFPreviewModal.tsx`)
- **Purpose**: In-browser PDF viewing
- **Features**:
  - Embedded PDF display
  - Download functionality
  - Responsive design
  - Modal overlay with controls

### Custom Hooks

#### useAlert (`src/hooks/useAlert.ts`)
- **Purpose**: Centralized alert management
- **Features**:
  - Custom alert components
  - Multiple alert types (success, error, info)
  - Auto-dismiss functionality
  - Branded design integration

---

## Data Flow

### Research Execution Flow

1. **Initiation**:
   - User submits research request via frontend
   - API validates input and creates research session
   - Background task initiated for multi-agent execution

2. **Multi-Agent Processing**:
   - CrewAI orchestrates sequential agent execution
   - Each agent accesses RAG-enhanced knowledge base
   - Real-time progress updates sent to research service
   - Context passed between agents for coherent analysis

3. **Progress Monitoring**:
   - Frontend polls status endpoint every 2 seconds
   - Progress dashboard updates with agent activities
   - Task completion tracked with timestamps and outputs

4. **Result Generation**:
   - Final agent generates comprehensive markdown report
   - PDF conversion using WeasyPrint with professional styling
   - Results stored in research service with metadata

5. **User Access**:
   - Completed research available via result endpoint
   - PDF preview and download functionality
   - Analytics tracking for usage metrics

### RAG Enhancement Flow

1. **Document Upload**:
   - User uploads documents via knowledge interface
   - Files validated and processed by knowledge service
   - Text extraction and chunking for optimal retrieval

2. **Vector Storage**:
   - Document chunks converted to embeddings via Google API
   - Vectors stored in ChromaDB with metadata
   - Collection statistics updated for dashboard

3. **Research Integration**:
   - Agent queries trigger similarity search in vector store
   - Relevant document chunks retrieved and ranked
   - Context injected into agent prompts for enhanced accuracy

4. **Quality Assurance**:
   - Source attribution maintained throughout process
   - Relevance scoring ensures high-quality context
   - Error handling for missing or corrupted documents

---

## Deployment

### Backend Deployment (Render)

**Configuration:**
- **Platform**: Render cloud platform
- **Container**: Docker-based deployment
- **Environment**: Production environment variables
- **Scaling**: Auto-scaling based on demand
- **Monitoring**: Built-in health checks and logging

**Key Files:**
- `Dockerfile`: Container configuration
- `render.yaml`: Deployment specification
- `.env.production`: Production environment variables

### Frontend Deployment (Vercel)

**Configuration:**
- **Platform**: Vercel edge network
- **Build**: Optimized React production build
- **Environment**: Production API endpoints
- **CDN**: Global content delivery network
- **SSL**: Automatic HTTPS certificate management

### Environment Configuration

**Backend Variables:**
- `GEMINI_API_KEY`: Google Gemini API authentication
- `CHROMA_DB_PATH`: Vector database storage location
- `FRONTEND_URL`: CORS configuration for frontend domain
- `JWT_SECRET`: Authentication token signing (future use)

**Frontend Variables:**
- `REACT_APP_API_URL`: Backend API endpoint
- `REACT_APP_ENVIRONMENT`: Deployment environment identifier

### Production Considerations

**Performance Optimization:**
- Research result caching to minimize API calls
- Vector database persistence for faster retrieval
- Optimized PDF generation with efficient styling
- Frontend code splitting and lazy loading

**Security Measures:**
- CORS configuration for trusted domains
- Input validation and sanitization
- Rate limiting for API endpoints
- Secure file upload handling

**Monitoring and Logging:**
- Comprehensive error logging throughout system
- Performance metrics tracking
- User analytics and usage patterns
- System health monitoring and alerts
