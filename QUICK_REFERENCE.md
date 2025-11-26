# QUICK REFERENCE CARD

Essential information for ESRS XBRL Platform development at a glance.

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Total User Stories** | 58 |
| **Total Story Points** | 205 |
| **Sprints** | 13 (Sprint 0 - Sprint 13) |
| **Duration** | 26 weeks (6.5 months) |
| **Avg Points/Sprint** | 15.8 |
| **Team Size** | 3-4 developers |

---

## 🗂️ Files in This Package

| File | Purpose | Size |
|------|---------|------|
| **jira-import.csv** | Import all 58 stories to Jira | Main file |
| **JIRA_SETUP.md** | Complete setup guide | 12 KB |
| **SPRINT_BOARDS.md** | Sprint-by-sprint breakdown | 15 KB |
| **JIRA_MATERIALS_README.md** | Overview & quick start | 8 KB |
| **PROJECT_OVERVIEW.md** | Tech stack & architecture | 15 KB |
| **DATABASE_SCHEMA.md** | 14-table database schema | 28 KB |
| **API_ENDPOINTS.md** | All REST endpoints | 22 KB |
| **CODING_STANDARDS.md** | Code patterns & best practices | 20 KB |
| **CUSTOM_INSTRUCTIONS.md** | ChatGPT Project setup | 10 KB |

---

## 🚀 Import Steps (5 Minutes)

```
1. Create Jira Project (Scrum template)
   └─> Name: "ESRS XBRL Platform"
   └─> Key: "ESRS"

2. Import CSV
   └─> Project Settings → Import → CSV
   └─> Upload: jira-import.csv
   └─> Map columns → Begin Import

3. Create Sprints
   └─> Backlog → Create Sprint (×14)
   └─> Name: "Sprint 0", "Sprint 1", ... "Sprint 13"
   └─> Drag issues into sprints

4. Configure Board
   └─> Board Settings → Columns
   └─> Add: To Do, In Progress, Review, Testing, Done

5. Start Sprint 0
   └─> Select Sprint 0 → Start Sprint
   └─> Set dates (2 weeks) → Start
```

---

## 📅 Sprint Timeline

| Sprint | Weeks | Points | Focus |
|--------|-------|--------|-------|
| **0** | 1-2 | 13 | Setup, database |
| **1** | 3-4 | 16 | Multi-tenancy, RLS |
| **2** | 5-6 | 13 | Auth, JWT |
| **3** | 7-8 | 16 | Workspaces, invites |
| **4** | 9-10 | 13 | Files, GCS |
| **5** | 11-12 | 21 | PDF processing |
| **6** | 13-14 | 16 | Reports, canvas |
| **7** | 15-16 | 16 | Tagging |
| **8** | 17-18 | 21 | AI integration |
| **9** | 19-20 | 13 | XBRL contexts |
| **10** | 21-22 | 16 | Taxonomies |
| **11** | 23-24 | 21 | XBRL export |
| **12** | 25-26 | 16 | File locking |
| **13** | 27-28 | 13 | Testing, deploy |

---

## 🗄️ Database Tables (14)

**Tenant Management** (3):
- `organizations` - Top-level tenants
- `workspaces` - Isolated environments
- `workspace_members` - User access

**User Management** (3):
- `users` - User accounts
- `refresh_tokens` - JWT tokens
- `invitations` - Pending invites

**File Management** (2):
- `files` - Uploaded documents
- `pdf_cache` - Preprocessed PDF data

**Report & Tagging** (3):
- `reports` - XBRL reports
- `tags` - XBRL concept tags
- `canvases` - Editor state

**XBRL** (2):
- `xbrl_contexts` - Entity, period, dimensions
- `taxonomies` - ESRS, GRI, SASB taxonomies

**Other** (1):
- `report_locks` - File locking

---

## 🔑 Key Technologies

| Layer | Technology |
|-------|-----------|
| **Backend** | NestJS, TypeScript |
| **Database** | PostgreSQL (Supabase) |
| **ORM** | TypeORM |
| **Auth** | JWT (RSA256) |
| **Queue** | Bull + Redis |
| **Storage** | Google Cloud Storage |
| **AI** | OpenAI/Anthropic API |
| **PDF** | pdf-parse, pdfjs-dist |
| **Frontend** | Next.js 15, React 19 |
| **State** | Zustand, React Query |
| **Styling** | TailwindCSS, Radix UI |
| **Deploy** | Docker, Cloud Run |

---

## 🎯 Sprint 0 Quick Start

**Goal**: Complete project setup in 2 weeks

**Tasks** (13 points):
1. Clone prime-nestjs (3 pts)
2. Setup Supabase PostgreSQL (5 pts)
3. Create database migrations (3 pts)
4. Docker configuration (2 pts)
5. CI/CD pipeline (0 pts)

**Day 1 Checklist**:
- [ ] Clone: `git clone https://github.com/josephgoksu/prime-nestjs.git backend`
- [ ] Install: `cd backend && npm install`
- [ ] Create Supabase project
- [ ] Configure `.env` with database credentials
- [ ] Test connection: `npm run start:dev`

**Week 1 Goal**: Database running, all 14 tables created
**Week 2 Goal**: Docker working, CI/CD passing

---

## 🏷️ Issue Labels

**By Feature**:
`multi-tenancy` `auth` `files` `pdf` `reports` `tagging` `ai` `xbrl` `taxonomy` `locking`

**By Type**:
`setup` `testing` `performance` `deployment`

**By Layer**:
`backend` `frontend` `database` `cloud`

---

## 📝 Common JQL Queries

```jql
# My current sprint work
assignee = currentUser() AND sprint in openSprints()

# All backend tasks not done
component = Backend AND status != Done

# High priority unassigned
priority = High AND assignee is EMPTY

# This sprint's completed work
sprint in openSprints() AND status = Done

# Blocked issues
status = Blocked

# Issues without story points
"Story Points" is EMPTY AND type in (Story, Task)
```

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| **Prime NestJS** | https://github.com/josephgoksu/prime-nestjs |
| **NestJS Docs** | https://docs.nestjs.com/ |
| **TypeORM Docs** | https://typeorm.io/ |
| **Supabase** | https://supabase.com/ |
| **XBRL Spec** | https://www.xbrl.org/ |
| **ESRS Standards** | https://www.efrag.org/ |

---

## 🔧 Essential Commands

### Backend (NestJS)

```bash
# Install dependencies
npm install

# Start dev server
npm run start:dev

# Generate migration
npm run migration:generate -- src/database/migrations/MigrationName

# Run migrations
npm run migration:run

# Run tests
npm run test

# Build for production
npm run build
```

### Frontend (Next.js)

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Build for production
pnpm build

# Type check
pnpm typecheck

# Lint
pnpm lint
```

### Docker

```bash
# Build backend image
docker build -t esrs-xbrl-backend ./backend

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all containers
docker-compose down
```

---

## 📊 Story Point Guide

| Points | Effort | Time | Complexity |
|--------|--------|------|------------|
| **1** | Trivial | 30m-1h | Copy-paste, config |
| **2** | Simple | 2-4h | Basic CRUD |
| **3** | Moderate | 1 day | Entity + endpoints |
| **5** | Complex | 2-3 days | Multiple entities |
| **8** | Very complex | 1 week | Complex logic |
| **13** | Needs breakdown | >1 week | Split into smaller stories |

---

## ✅ Definition of Done

- [ ] Code follows CODING_STANDARDS.md
- [ ] No TypeScript `any` types
- [ ] Code reviewed and approved
- [ ] Unit tests written (80% coverage)
- [ ] All tests passing
- [ ] API documented (Swagger)
- [ ] Acceptance criteria met
- [ ] Merged to `dev` branch

---

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| **CSV import fails** | Check custom fields exist first |
| **Points not showing** | Board Settings → Card Layout → Add "Story Points" |
| **Sprints empty** | Manually drag issues into sprints |
| **RLS not working** | Check `app.current_workspace_id` session variable |
| **Tests failing** | Check test database connection |

---

## 🎓 ChatGPT Project Setup

**Upload these 5 files** to ChatGPT Project:

1. PROJECT_OVERVIEW.md
2. DATABASE_SCHEMA.md
3. API_ENDPOINTS.md
4. CODING_STANDARDS.md
5. CUSTOM_INSTRUCTIONS.md

**Then ask**:
- "Help me implement file locking"
- "Generate TypeORM migration for report_locks"
- "Create AI recommendation endpoint"
- "How do I set up RLS policies?"

---

## 📈 Success Metrics

| Metric | Target |
|--------|--------|
| **Sprint velocity** | 15-18 points |
| **Completion rate** | >80% |
| **Test coverage** | >80% |
| **API response time** | <200ms (p95) |
| **PDF processing** | <30s (50 pages) |
| **Deployment uptime** | >99.9% |

---

## 🎉 Milestones

| Week | Milestone |
|------|-----------|
| **2** | Database fully configured |
| **4** | Multi-tenancy working |
| **6** | Users can login |
| **10** | File upload working |
| **12** | PDF processing complete |
| **14** | Reports can be created |
| **16** | Tagging system working |
| **18** | AI recommendations live |
| **22** | Taxonomies manageable |
| **24** | iXBRL export working |
| **26** | File locking complete |
| **28** | 🚀 **Production deployment** |

---

## 🔐 Environment Variables

```env
# Database
DATABASE_HOST=db.iuoikdmkqmzggspcmggr.supabase.co
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password

# JWT
JWT_PRIVATE_KEY=<RSA private key>
JWT_PUBLIC_KEY=<RSA public key>

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Storage
STORAGE_BACKEND=gcs
GCS_BUCKET=esrs-xbrl-files
GCS_PROJECT_ID=your-project

# AI
OPENAI_API_KEY=sk-...
```

---

**Print this page and keep it at your desk!** 📌

---

**Last Updated**: 2025-11-03
**Version**: 1.0
**Status**: Ready to Rock! 🚀
