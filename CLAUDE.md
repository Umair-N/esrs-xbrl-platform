# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ESRS XBRL Platform - A comprehensive financial data processing and XBRL (eXtensible Business Reporting Language) management platform for European Sustainability Reporting Standard (ESRS) compliance. The platform processes documents (PDF/DOCX), enables XBRL tagging with AI assistance, and exports iXBRL reports.

**Tech Stack:**

- **Frontend:** Next.js 15.2.4 + React 19 + TypeScript, TailwindCSS, Radix UI, TanStack React Query, Zustand
- **Backend:** FastAPI (Python), PostgreSQL (Supabase), SQLAlchemy, Alembic
- **Package Manager:** pnpm
- **Deployment:** Docker, Google Cloud Run/App Engine

## Common Commands

### Frontend Development

```bash
# Development with Turbopack
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Linting
pnpm lint
pnpm lint:fix

# Type checking
pnpm typecheck
```

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server (from backend directory)
uvicorn main:app --reload --port 8000

# Run with specific host/port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Database migrations (from backend directory)
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Check migration history
alembic current
alembic history
```

### Docker

```bash
# Build backend image
docker build -t esrs-xbrl-backend ./backend

# Run backend container
docker run -p 8000:8000 --env-file backend/config.env esrs-xbrl-backend
```

## Architecture Overview

### Critical Architecture Patterns

#### 1. **Frontend State Management Strategy**

The application uses a **multi-layer state management approach**:

- **Zustand Stores** (`/store`): Global client-side state
  - `tagging-store.ts`: Manages pending concept selections from AI recommendations and selected context ID
  - `taxonomy-store.ts`: Manages taxonomy-related state

- **TanStack React Query**: Server state management with caching
  - Used throughout `/features` for API calls
  - Automatically handles background sync, cache invalidation, and error states

- **Component Local State**: React hooks for UI-specific state

**Key Pattern:** When AI recommender suggests a tag, it sets `pendingConcept` in `tagging-store`, which the tagging panel reads to preselect the concept. This cross-component communication pattern is critical for the recommendation workflow.

#### 2. **Backend Layered Architecture**

Follows a strict **4-layer pattern** (top to bottom):

```
Endpoints (/api/v1/endpoints) → Services (/services) → CRUD (/crud) → Models (/models)
```

- **Endpoints**: Route handlers, request validation (Pydantic schemas)
- **Services**: Business logic, orchestration, external API calls
- **CRUD**: Database operations, query building
- **Models**: SQLAlchemy ORM definitions

**Critical Rule:** Never call CRUD directly from endpoints. Always go through services. This separation allows business logic to be testable and reusable.

#### 3. **Database Connection Management**

The platform uses **dual database managers** (critical for understanding connection issues):

- **`core/config.py`**: `DatabaseManager` class with ThreadedConnectionPool (newer, used in `main.py` lifespan)
- **`database/connection.py`**: `DatabaseConnection` singleton with SimpleConnectionPool (legacy, used by CRUD operations)

**Important:** Both point to **Supabase PostgreSQL**. The commented-out Neon configuration is disabled. SSL mode is `require` with channel binding set to `prefer`.

**Connection Pattern:**

```python
# In services/CRUD operations
from database.connection import db_manager
conn = db_manager.get_connection()
try:
    # operations
finally:
    db_manager.return_connection(conn)
```

#### 4. **XBRL Generation Pipeline** (`lib/xbrl.ts`)

The **core XBRL export functionality** is in a single 1,260-line file:

**Multi-Taxonomy Support:**

- Hardcoded taxonomy configurations: ESRS, GRI, SASB
- Each taxonomy has: namespaces, schemaRefs, conceptValidation, unitMapping, contextRules
- `TAXONOMY_CONFIGS` object at top of file controls all taxonomy-specific behavior

**iXBRL Generation Flow:**

1. `generateiXBRLDocument()`: Entry point, assembles namespaces/contexts/units
2. `planTagPlacements()`: Maps tags to text positions (handles overlaps by creation time)
3. `generateEnhancediXBRLTag()`: Creates `<ix:nonFraction>` or `<ix:nonNumeric>` elements
4. `parseConceptNameWithTaxonomy()`: Converts internal concept IDs to XBRL namespaced names (e.g., `esrs_e1_ghgEmissions` → `esrs-e1:ghgEmissions`)

**Key Design Decision:** Tags without valid placement in text are rendered in "unplaced-tags" section at bottom. Tag placement uses `startIndex`/`endIndex` first, falls back to text search, prioritizes by creation time.

#### 5. **Canvas State Persistence**

Editor sessions are saved to the database via:

- **Endpoint**: `/api/v1/reports/canvas` (POST/GET)
- **Model**: `Canvas` (`backend/models/canvas.py`)
- **Purpose**: Stores entire editor state including blocks, tags, scroll position

**Critical for resuming work:** When users return to a report, the frontend fetches the canvas state and restores the exact editing session.

#### 6. **AI Recommendation Workflow**

1. User selects text in editor
2. Frontend calls recommender service (`/features/recommender`)
3. AI returns concept suggestions with confidence scores
4. User selects suggestion → stored in `tagging-store.setPendingConcept()`
5. Tagging panel (`components/editor/tagging-panel.tsx`) reads pending concept
6. User selects context → tag committed to report
7. Optional: Feedback sent back to AI (stored as `feedbackId` in store)

#### 7. **File Processing Architecture**

- **Upload**: `/api/v1/endpoints/files.py` validates file type/size (70MB max)
- **PDF Processing**: Dual library approach (PyPDF2 + PyMuPDF in `services/pdf_cache_service.py`)
- **Canvas Rendering**: Frontend uses HTML5 Canvas (`components/editor/pdf-editor.tsx`) for efficient rendering
- **Storage**:
  - **Local**: `uploads/` directory (development)
  - **GCS**: Google Cloud Storage (production, when `STORAGE_BACKEND=gcs`)

**Storage Backend Detection:** Controlled by `core/config.py` `is_gcp_deployment` property and `STORAGE_BACKEND` setting.

#### 8. **Taxonomy Management**

- **Upload**: Admin uploads ZIP taxonomy files via `/api/v1/taxonomy-admin`
- **Storage**: GCS (production) or local filesystem (development)
- **Assignment**: Taxonomies assigned to users via `UserTaxonomy` junction table
- **Frontend**: 5.5MB `lib/esrs_outline.json` contains ESRS taxonomy structure for browsing

**Critical:** Taxonomy files are preprocessed and cached. Changes require re-upload and activation.

#### 9. **Context Management**

Contexts define the entity, period, and dimensions for XBRL facts:

- **Model**: `XBRLContext` (`backend/models/context.py`)
- **Types**: `instant` (point in time) or `duration` (date range)
- **Auto-suggestion**: AI suggests optimal contexts based on data patterns
- **Selected Context**: Stored in `tagging-store.selectedContextId` for reuse

#### 10. **Authentication & Middleware**

- **JWT-based auth**: 30-min access tokens, 7-day refresh tokens
- **Auto-refresh middleware** (`main.py` lines 82-116): Automatically refreshes tokens via cookies
- **Cookie security**: Production uses `SameSite=none` + `secure=true` (HTTPS), dev uses `SameSite=lax` + `secure=false`
- **Role-based access**: User roles stored in `User` model, checked via dependencies

## Environment Configuration

### Frontend (`.env` in root)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_URL=http://localhost:3000
```

### Backend (`backend/config.env`)

Critical settings:

```bash
# Supabase PostgreSQL (active)
SUPABASE_HOST=db.iuoikdmkqmzggspcmggr.supabase.co
SUPABASE_DATABASE=postgres
SUPABASE_USER=<your_user>
SUPABASE_PASSWORD=<your_password>
SUPABASE_PORT=5432

# Security
SECRET_KEY=<generate-secure-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Storage (development: local, production: gcs)
STORAGE_BACKEND=local
GCS_BUCKET=<bucket-name>

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://esrs-xbrl-platform.vercel.app

# Environment detection
ENVIRONMENT=development  # or "production"
GOOGLE_CLOUD_PROJECT=<project-id>  # for GCP deployment
```

## Critical File Locations

### Core Business Logic

- **XBRL Generation**: `lib/xbrl.ts` (1,260 lines, multi-taxonomy support)
- **API Client**: `lib/api-client.ts` (Axios configuration)
- **Taxonomy Data**: `lib/esrs_outline.json` (5.5MB taxonomy structure)
- **Tagging Store**: `store/tagging-store.ts` (recommendation workflow coordination)

### Backend Services

- **Report Service**: `backend/services/report_service.py` (report processing)
- **PDF Cache Service**: `backend/services/pdf_cache_service.py` (PDF preprocessing)
- **Taxonomy Service**: `backend/services/taxonomy_service.py` (taxonomy CRUD with GCS/local adapter)
- **Auth Service**: `backend/services/auth_service.py` (JWT creation/validation)

### Key Endpoints

- **API Router**: `backend/api/v1/api.py` (route aggregation)
- **Auth**: `backend/api/v1/endpoints/auth.py`
- **Reports**: `backend/api/v1/endpoints/reports.py`
- **Canvas**: `backend/api/v1/endpoints/canvas.py`
- **Contexts**: `backend/api/v1/endpoints/context.py`
- **Taxonomy**: `backend/api/v1/endpoints/taxonomy.py` + `taxonomy_admin.py`

### Frontend Components

- **PDF Editor**: `components/editor/pdf-editor.tsx` (canvas-based rendering)
- **Tagging Panel**: `components/editor/tagging-panel.tsx` (concept selection UI)
- **Tagged Facts List**: `components/editor/tagged-facts-list.tsx` (shows all tags)
- **Export**: `components/editor/export.tsx` (iXBRL export UI)

## Database Schema Key Points

### Core Models (`backend/models/`)

- **User**: Authentication, roles, company, designation, platform access
- **Report**: Title, file reference, user ownership, created/updated timestamps
- **ReportBlock**: Content sections with tags
- **Canvas**: Persisted editor state (blocks, tags, scroll position)
- **XBRLContext**: Entity, period (instant/duration), dimensions
- **Taxonomy** + **UserTaxonomy**: Taxonomy files and user assignments
- **RefreshToken**: Token rotation for security

### Important Relationships

- User → Reports (one-to-many)
- Report → ReportBlocks (one-to-many)
- Report → Canvas (one-to-one, nullable)
- User → UserTaxonomy → Taxonomy (many-to-many)
- User → RefreshToken (one-to-many)

## Development Workflow Notes

### Adding New XBRL Taxonomy

1. Add taxonomy config to `TAXONOMY_CONFIGS` in `lib/xbrl.ts`
2. Define namespaces, schemaRefs, conceptValidation, unitMapping
3. Update `getSupportedTaxonomies()` return value
4. Test with `generateOptimizediXBRLDocument()`

### Adding New API Endpoint

1. Create Pydantic schema in `backend/schemas/`
2. Add service method in `backend/services/`
3. Add CRUD operations in `backend/crud/`
4. Create endpoint in `backend/api/v1/endpoints/`
5. Register router in `backend/api/v1/api.py`

### Database Migrations

```bash
# Auto-generate migration from model changes
cd backend
alembic revision --autogenerate -m "description"

# Review migration file in alembic/versions/
# Edit if needed (Alembic doesn't catch everything)

# Apply migration
alembic upgrade head
```

### Debugging Connection Issues

- Check both `DatabaseManager` instances (core/config.py and database/connection.py)
- Verify Supabase credentials in `config.env`
- Check SSL settings (`PGSSLMODE=require`, `PGCHANNELBINDING=prefer`)
- Test connection: `db_manager.is_connection_alive()`
- Review logs in `backend/logs/app.log`

### Canvas State Issues

- Canvas auto-saves on changes (debounced)
- Backend endpoint: POST `/api/v1/reports/canvas`
- Model: `Canvas` has `canvas_data` JSONB field
- If session not loading, check backend logs for JSON parsing errors

## Branch Strategy

- **Main branch**: `master` (production)
- **Development branch**: `dev` (active development)
- **Feature branches**: Create from `dev`, merge back to `dev`

## Known Limitations & Legacy Code

1. **Dual Database Managers**: Two connection pool implementations exist. Consolidation would improve maintainability.
2. **Neon References**: Commented-out Neon database config in `core/config.py` and `database/connection.py` (lines 24-30). Can be removed.
3. **XBRL.ts Complexity**: 1,260-line file handles all taxonomy logic. Consider splitting into taxonomy-specific modules.
4. **Editor Session Model**: `backend/models/editor_session.py` marked as deprecated. Use `Canvas` model instead.
5. **No Automated Tests**: Project lacks unit/integration tests. Manual testing required.

## Recent Development Focus (from git log)

- PDF tagging and highlighting improvements
- Canvas-based rendering for performance optimization
- iXBRL export workflow simplification
- Bug fixes for text highlighting during tag addition
