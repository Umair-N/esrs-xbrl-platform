# PROJECT OVERVIEW

## ESRS XBRL Platform - NestJS Rewrite

A comprehensive financial data processing and XBRL (eXtensible Business Reporting Language) management platform for European Sustainability Reporting Standard (ESRS) compliance. The platform processes documents (PDF/DOCX), enables XBRL tagging with AI assistance, and exports iXBRL reports.

---

## Tech Stack

### Backend
- **Framework**: NestJS (TypeScript)
- **Base Template**: [prime-nestjs](https://github.com/josephgoksu/prime-nestjs)
- **Database**: PostgreSQL (Supabase)
- **ORM**: TypeORM with migrations
- **Authentication**: JWT (RSA256) with refresh tokens
- **Multi-Tenancy**: Row-Level Security (RLS) with workspace isolation
- **Queue**: Bull + Redis for background jobs
- **Storage**: Google Cloud Storage (production) / Local filesystem (development)
- **AI Integration**: OpenAI/Anthropic API for XBRL concept suggestions
- **PDF Processing**: pdf-parse + pdfjs-dist
- **Validation**: class-validator, class-transformer

### Frontend
- **Framework**: Next.js 15.2.4 with App Router
- **UI Library**: React 19
- **Styling**: TailwindCSS + Radix UI
- **State Management**:
  - Zustand (client state)
  - TanStack React Query (server state)
- **Language**: TypeScript with strict mode
- **Build Tool**: Turbopack

### DevOps
- **Containerization**: Docker
- **Deployment**: Google Cloud Run / App Engine
- **Package Manager**: pnpm (frontend), npm (backend)
- **Version Control**: Git

---

## Architecture Patterns

### 1. Multi-Tenancy (3-Level Hierarchy)

```
Organization (Company)
  └── Workspace (Team/Project)
      └── Resources (Reports, Files, Tags, etc.)
```

**Implementation**:
- PostgreSQL Row-Level Security (RLS) policies
- Middleware sets `app.current_workspace_id` session variable
- All workspace-scoped tables automatically filter by workspace
- UUIDs for all primary keys (distributed scalability)

**Key Tables**:
- `organizations` - Top-level tenant
- `workspaces` - Isolated environments within organization
- `workspace_members` - User access control per workspace

### 2. File Locking (Pessimistic Concurrency Control)

**Not using real-time collaboration**. Instead:
- One user can edit at a time
- Others can view in read-only mode
- 15-minute auto-expire with heartbeat refresh
- Admin force-unlock capability

**Implementation**:
- `report_locks` table with expiry timestamp
- REST API + polling (no WebSocket)
- Frontend heartbeat every 60 seconds
- Cron job cleans expired locks every 5 minutes

### 3. Background Job Processing

**Use Case**: PDF text extraction, image rendering, AI processing

**Implementation**:
- Bull queue with Redis
- Separate worker processes
- Job status tracking
- Retry logic for failures

### 4. Soft Deletes & Audit Logging

- All entities have `deleted_at` timestamp
- `audit_logs` table tracks all CRUD operations
- Compliance-ready for financial regulations

---

## Database Schema (14 Tables)

### Tenant Management
1. **organizations** - Companies/top-level tenants
2. **workspaces** - Isolated environments within organization
3. **workspace_members** - User-workspace access mapping

### User Management
4. **users** - User accounts
5. **refresh_tokens** - JWT token rotation
6. **invitations** - Pending workspace invitations

### File Management
7. **files** - Uploaded documents (PDF/DOCX)
8. **pdf_cache** - Preprocessed PDF data (text, bounding boxes, images)

### Report & Tagging
9. **reports** - XBRL reports
10. **tags** - XBRL concept tags on text selections
11. **canvases** - Persisted editor state (blocks, scroll position)

### XBRL Specific
12. **xbrl_contexts** - Entity, period, dimensions for XBRL facts
13. **taxonomies** - XBRL taxonomy files (ESRS, GRI, SASB)
14. **workspace_taxonomies** - Taxonomy assignments to workspaces

### Collaboration
15. **report_locks** - File locking mechanism

### Audit
16. **audit_logs** - Comprehensive activity tracking

---

## Key Features

### 1. Document Processing
- Upload PDF/DOCX files (70MB max)
- Extract text with word-level bounding boxes
- Render pages to JPEG for canvas display
- Store in `pdf_cache` for instant reload

### 2. AI-Powered XBRL Tagging
- Select text in document
- AI suggests XBRL concepts with confidence scores
- User reviews and approves suggestions
- Tags stored with context (entity, period, dimensions)

### 3. Multi-Taxonomy Support
- ESRS (European Sustainability Reporting Standard)
- GRI (Global Reporting Initiative)
- SASB (Sustainability Accounting Standards Board)
- Admin uploads taxonomy ZIP files
- Taxonomies assigned per workspace

### 4. iXBRL Export
- Generate inline XBRL documents
- Multi-taxonomy namespace support
- Validation against taxonomy schemas
- Download as iXBRL file

### 5. Collaboration & Permissions
- Organization-level user management
- Workspace-level isolation
- Role-based access control (Admin, Editor, Viewer)
- File locking prevents concurrent edits

---

## Project Timeline

**Total Duration**: 26 weeks (13 sprints × 2 weeks)
**Total Effort**: 205 story points
**Recommended Team**: 3-4 developers

### Sprint Breakdown

| Sprint | Duration | Focus Area | Story Points |
|--------|----------|------------|--------------|
| 0 | 2 weeks | Project setup, prime-nestjs config, database init | 13 |
| 1 | 2 weeks | Multi-tenant foundation, RLS setup | 16 |
| 2 | 2 weeks | Authentication, user management | 13 |
| 3 | 2 weeks | Organization & workspace management | 16 |
| 4 | 2 weeks | File upload & storage | 13 |
| 5 | 2 weeks | PDF processing & caching | 21 |
| 6 | 2 weeks | Report & canvas management | 16 |
| 7 | 2 weeks | Tagging system | 16 |
| 8 | 2 weeks | AI integration for concept suggestions | 21 |
| 9 | 2 weeks | Context management | 13 |
| 10 | 2 weeks | Taxonomy management | 16 |
| 11 | 2 weeks | XBRL export engine | 21 |
| 12 | 2 weeks | File locking & collaboration | 16 |
| 13 | 2 weeks | Testing, optimization, deployment | 13 |

---

## Development Workflow

### Backend Development

```bash
# Setup
cd backend
npm install
cp .env.example .env

# Development
npm run start:dev

# Database migrations
npm run migration:generate -- src/database/migrations/MigrationName
npm run migration:run
npm run migration:revert

# Testing
npm run test
npm run test:e2e
npm run test:cov
```

### Frontend Development

```bash
# Setup
pnpm install
cp .env.example .env.local

# Development
pnpm dev

# Build
pnpm build
pnpm start

# Type checking
pnpm typecheck

# Linting
pnpm lint
pnpm lint:fix
```

---

## Environment Variables

### Backend (`backend/.env`)

```env
# Database (Supabase PostgreSQL)
DATABASE_HOST=db.iuoikdmkqmzggspcmggr.supabase.co
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_SSL_MODE=require

# JWT Authentication
JWT_PRIVATE_KEY=<RSA private key>
JWT_PUBLIC_KEY=<RSA public key>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis (for Bull queue)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Storage
STORAGE_BACKEND=local # or 'gcs'
GCS_BUCKET=esrs-xbrl-files
GCS_PROJECT_ID=your-project-id

# AI Services
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://esrs-xbrl-platform.vercel.app

# Environment
NODE_ENV=development
PORT=8000
```

### Frontend (`.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_URL=http://localhost:3000
```

---

## Security Considerations

### Row-Level Security (RLS)

All workspace-scoped tables have RLS policies:

```sql
-- Example RLS policy
CREATE POLICY workspace_isolation ON reports
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

Middleware sets session variable on every request:

```typescript
// Before request processing
await db.query('SET app.current_workspace_id = $1', [workspaceId]);
```

### Authentication Flow

1. User logs in → receives access token (30 min) + refresh token (7 days)
2. Access token stored in httpOnly cookie
3. Refresh token stored in database with rotation
4. Frontend middleware auto-refreshes tokens
5. Logout invalidates refresh token

### File Access Control

- Files scoped to workspace
- URL presigning for temporary access (GCS)
- Virus scanning on upload (optional)
- File size limits enforced

---

## Migration from Python/FastAPI

**Clean Slate Approach** - No data migration from old system.

### Why Clean Slate?

1. **No legacy constraints** - Design optimal schema from scratch
2. **Modern patterns** - UUID keys, soft deletes, RLS
3. **Simpler migration** - No complex ETL pipelines
4. **Fresh start** - Users can re-upload documents if needed

### What's Carried Over?

- Business logic (XBRL generation, tagging workflow)
- Frontend components (with updates for new API)
- Taxonomy files (ESRS, GRI, SASB)
- Design patterns (multi-step tagging, AI recommendations)

---

## Testing Strategy

### Backend Testing

- **Unit Tests**: Service layer logic with mocked dependencies
- **Integration Tests**: API endpoints with test database
- **E2E Tests**: Full workflows (upload → tag → export)
- **Coverage Target**: 80%+ for critical paths

### Frontend Testing

- **Component Tests**: React Testing Library + Vitest
- **Integration Tests**: User flows with MSW
- **E2E Tests**: Playwright for critical paths
- **Coverage Target**: 70%+ for features

---

## Deployment Architecture

### Production Setup

```
User → Vercel (Next.js frontend)
       ↓
Cloud Load Balancer → Cloud Run (NestJS backend)
                      ↓
                  PostgreSQL (Supabase)
                  Redis (Cloud Memorystore)
                  GCS (File storage)
```

### CI/CD Pipeline

1. **GitHub Actions** on push to `dev` or `master`
2. **Linting & Testing** (automated checks)
3. **Docker Build** (backend image)
4. **Deploy to Cloud Run** (backend)
5. **Deploy to Vercel** (frontend)
6. **Run Smoke Tests** (post-deployment validation)

---

## Known Limitations & Future Enhancements

### Current Limitations

1. **No Real-Time Collaboration** - Simple file locking instead
2. **No Automated Tests** - Manual testing required initially
3. **Single Region Deployment** - No multi-region redundancy
4. **Limited File Formats** - PDF and DOCX only

### Future Enhancements

1. **Excel Import** - Upload Excel templates for bulk tagging
2. **Audit Trail UI** - Visual timeline of changes
3. **Advanced Analytics** - Reporting dashboard for compliance metrics
4. **API Rate Limiting** - Throttling for external API calls
5. **Webhook Support** - Notify external systems on events

---

## Success Metrics

### Performance Targets

- PDF upload processing: < 30 seconds for 50-page document
- API response time: < 200ms (p95)
- Database queries: < 100ms (p95)
- Frontend load time: < 2 seconds (LCP)

### Business Metrics

- User onboarding time: < 15 minutes
- Tag creation time: < 10 seconds per tag
- XBRL export success rate: > 99%
- System uptime: > 99.9%

---

## Support & Documentation

### Resources

- **Technical Docs**: See API_ENDPOINTS.md, DATABASE_SCHEMA.md
- **Coding Standards**: See CODING_STANDARDS.md
- **Issue Tracking**: Jira board (13 sprints planned)
- **Repository**: GitHub (branch strategy: `master` → `dev` → feature branches)

### Team Structure

- **1 Tech Lead**: Architecture decisions, code review
- **2-3 Backend Developers**: NestJS, PostgreSQL, AI integration
- **1-2 Frontend Developers**: Next.js, React, TailwindCSS
- **1 DevOps Engineer**: Docker, Cloud Run, CI/CD

---

**Last Updated**: 2025-11-03
**Version**: 1.0
**Status**: Ready for Sprint 0
