# SPRINT BOARDS

Detailed board templates for each sprint with tasks, dependencies, and acceptance criteria.

---

## Sprint 0: Foundation Setup (Weeks 1-2)

**Goal**: Set up development environment, database, and CI/CD pipeline

**Story Points**: 13

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-1 | Setup NestJS project with prime-nestjs | Task | 3 | Backend Dev | None |
| ESRS-2 | Configure PostgreSQL with Supabase | Task | 5 | Backend Dev | None |
| ESRS-3 | Create initial database migration | Task | 3 | Backend Dev | ESRS-2 |
| ESRS-4 | Setup Docker configuration | Task | 2 | DevOps | ESRS-1 |
| ESRS-5 | Configure CI/CD pipeline | Task | 0 | DevOps | ESRS-4 |

### Sprint Board View

```
┌─────────────┬──────────────┬────────────┬──────┐
│   TO DO     │ IN PROGRESS  │   REVIEW   │ DONE │
├─────────────┼──────────────┼────────────┼──────┤
│ ESRS-1 (3)  │              │            │      │
│ ESRS-2 (5)  │              │            │      │
│ ESRS-4 (2)  │              │            │      │
│             │              │            │      │
│ Blocked:    │              │            │      │
│ ESRS-3 (3)  │              │            │      │
│ ESRS-5 (0)  │              │            │      │
└─────────────┴──────────────┴────────────┴──────┘
```

### Definition of Done

- [ ] All 5 tasks completed
- [ ] Database has all 14 tables
- [ ] Docker containers start successfully
- [ ] CI/CD pipeline runs without errors
- [ ] Documentation updated (README.md)

---

## Sprint 1: Multi-Tenancy Foundation (Weeks 3-4)

**Goal**: Implement multi-tenant architecture with Row-Level Security

**Story Points**: 16

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-6 | Implement organization entity and CRUD | Story | 5 | Backend Dev | Sprint 0 |
| ESRS-7 | Implement workspace entity and CRUD | Story | 5 | Backend Dev | ESRS-6 |
| ESRS-8 | Setup Row-Level Security policies | Task | 3 | Backend Dev | ESRS-7 |
| ESRS-9 | Create workspace middleware | Task | 3 | Backend Dev | ESRS-8 |

### Sprint Board View

```
┌─────────────┬──────────────┬────────────┬──────┐
│   TO DO     │ IN PROGRESS  │   REVIEW   │ DONE │
├─────────────┼──────────────┼────────────┼──────┤
│ ESRS-7 (5)  │ ESRS-6 (5)   │            │      │
│ ESRS-8 (3)  │              │            │      │
│ ESRS-9 (3)  │              │            │      │
└─────────────┴──────────────┴────────────┴──────┘
```

### Testing Checklist

- [ ] Create 2 organizations
- [ ] Create 3 workspaces (2 in org1, 1 in org2)
- [ ] Verify RLS: workspace1 data not visible when querying workspace2
- [ ] Test middleware sets session variable correctly
- [ ] API returns 403 when accessing other workspace data

---

## Sprint 2: Authentication (Weeks 5-6)

**Goal**: Implement JWT authentication with refresh tokens

**Story Points**: 13

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-10 | Implement user entity and repository | Story | 5 | Backend Dev | Sprint 1 |
| ESRS-11 | Implement JWT authentication | Story | 5 | Backend Dev | ESRS-10 |
| ESRS-12 | Create auth endpoints (register/login/logout) | Story | 3 | Backend Dev | ESRS-11 |
| ESRS-13 | Implement refresh token rotation | Task | 0 | Backend Dev | ESRS-12 |

### Sprint Board View

```
┌─────────────┬──────────────┬────────────┬──────┐
│   TO DO     │ IN PROGRESS  │   REVIEW   │ DONE │
├─────────────┼──────────────┼────────────┼──────┤
│ ESRS-11 (5) │ ESRS-10 (5)  │            │      │
│ ESRS-12 (3) │              │            │      │
│ ESRS-13 (0) │              │            │      │
└─────────────┴──────────────┴────────────┴──────┘
```

### API Testing

**Test with Postman/cURL**:

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "organizationName": "Test Corp",
    "organizationSlug": "test-corp",
    "email": "admin@test.com",
    "password": "SecurePass123!",
    "firstName": "John",
    "lastName": "Doe"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "SecurePass123!"
  }'

# Get current user
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

## Sprint 3: Organization Management (Weeks 7-8)

**Goal**: Workspace members, invitations, and role-based access

**Story Points**: 16

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-14 | Create workspace member management | Story | 5 | Backend Dev | Sprint 2 |
| ESRS-15 | Implement invitation system | Story | 5 | Backend Dev | ESRS-14 |
| ESRS-16 | Create workspace guard | Task | 3 | Backend Dev | Sprint 2 |
| ESRS-17 | Implement role-based access control | Task | 3 | Backend Dev | ESRS-16 |

### User Flow Testing

1. **Admin invites user to workspace**
   - POST /invitations with email
   - Verify email sent (check logs or inbox)
   - Copy invitation token

2. **User accepts invitation**
   - POST /invitations/:token/accept
   - User account created
   - User added to workspace_members

3. **Role-based access**
   - Viewer: Cannot create/edit reports (403)
   - Editor: Can create/edit own reports
   - Admin: Can manage all reports and members

---

## Sprint 4: File Management (Weeks 9-10)

**Goal**: File upload with GCS integration

**Story Points**: 13

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-18 | Implement file upload endpoint | Story | 5 | Backend Dev | Sprint 3 |
| ESRS-19 | Setup Google Cloud Storage integration | Task | 3 | Backend Dev | None |
| ESRS-20 | Implement file metadata extraction | Task | 3 | Backend Dev | ESRS-18 |
| ESRS-21 | Create file download endpoint | Story | 2 | Backend Dev | ESRS-18 |

### GCS Setup Checklist

- [ ] GCS bucket created: `esrs-xbrl-files-prod`
- [ ] Service account with Storage Object Admin role
- [ ] Service account key downloaded
- [ ] Environment variables set: GCS_BUCKET, GCS_PROJECT_ID
- [ ] Test upload/download with presigned URLs

---

## Sprint 5: PDF Processing (Weeks 11-12)

**Goal**: Extract text, word positions, and render images from PDFs

**Story Points**: 21

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-22 | Implement PDF text extraction | Story | 5 | Backend Dev | Sprint 4 |
| ESRS-23 | Extract word-level bounding boxes | Story | 8 | Backend Dev | ESRS-22 |
| ESRS-24 | Render PDF pages to JPEG images | Story | 5 | Backend Dev | ESRS-22 |
| ESRS-25 | Create Bull queue for async processing | Task | 3 | Backend Dev | ESRS-22 |

### Performance Targets

| Metric | Target | How to Test |
|--------|--------|-------------|
| Text extraction | <5s for 50 pages | Upload 50-page PDF, check logs |
| Word extraction | <10s for 50 pages | Check pdf_cache.word_data populated |
| Image rendering | <15s for 50 pages | Check pdf_cache.image_data size |
| Total processing | <30s for 50 pages | End-to-end upload to cache complete |

---

## Sprint 6: Report Management (Weeks 13-14)

**Goal**: Reports with canvas persistence

**Story Points**: 16

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-26 | Implement report entity and CRUD | Story | 5 | Backend Dev | Sprint 5 |
| ESRS-27 | Create canvas persistence | Story | 5 | Backend Dev | ESRS-26 |
| ESRS-28 | Implement report listing with filters | Task | 3 | Backend Dev | ESRS-26 |
| ESRS-29 | Create report sharing (workspace-level) | Task | 3 | Backend Dev | ESRS-26 |

### API Testing

```bash
# Create report
curl -X POST http://localhost:8000/api/v1/reports \
  -H "Authorization: Bearer <token>" \
  -H "X-Workspace-Id: <workspace_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Annual Report 2023",
    "fileId": "<file_id>",
    "taxonomyId": "<taxonomy_id>"
  }'

# Save canvas state
curl -X POST http://localhost:8000/api/v1/reports/<report_id>/canvas \
  -H "Authorization: Bearer <token>" \
  -d '{
    "canvasData": {
      "blocks": [],
      "scrollPosition": 100
    }
  }'

# List reports with filters
curl -X GET "http://localhost:8000/api/v1/reports?status=draft&sort=createdAt:desc"
```

---

## Sprint 7: Tagging System (Weeks 15-16)

**Goal**: XBRL tag creation with validation

**Story Points**: 16

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-30 | Implement tag entity and CRUD | Story | 5 | Backend Dev | Sprint 6 |
| ESRS-31 | Create tag listing with grouping | Task | 3 | Backend Dev | ESRS-30 |
| ESRS-32 | Implement tag validation | Task | 3 | Backend Dev | ESRS-30 |
| ESRS-33 | Add tag conflict detection | Task | 5 | Backend Dev | ESRS-30 |

### Tag Testing Scenarios

1. **Create valid tag**
   - Concept exists in taxonomy
   - Unit matches concept
   - Context exists
   - Returns 201 Created

2. **Invalid concept ID**
   - Returns 400 with error: "Concept not found in taxonomy"

3. **Overlapping tags**
   - Create tag at index 100-150
   - Create second tag at index 125-175
   - Both succeed, warning returned

---

## Sprint 8: AI Integration (Weeks 17-18)

**Goal**: AI-powered XBRL concept recommendations

**Story Points**: 21

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-34 | Integrate OpenAI API for recommendations | Story | 8 | Backend Dev | Sprint 7 |
| ESRS-35 | Create AI recommendation endpoint | Story | 8 | Backend Dev | ESRS-34 |
| ESRS-36 | Implement context suggestion | Task | 5 | Backend Dev | ESRS-35 |

### AI Prompt Template Example

```typescript
const prompt = `
You are an XBRL expert for ESRS (European Sustainability Reporting Standard).

Selected text: "${selectedText}"
Surrounding context: "${surroundingContext}"

Task: Suggest the most appropriate XBRL concept(s) for this text.

Respond in JSON format:
{
  "recommendations": [
    {
      "conceptId": "esrs_e1:ghgEmissions",
      "conceptLabel": "GHG Emissions",
      "confidence": 0.95,
      "suggestedValue": "12500",
      "suggestedUnit": "tCO2e",
      "reasoning": "Text explicitly mentions greenhouse gas emissions..."
    }
  ]
}
`;
```

---

## Sprint 9: Context Management (Weeks 19-20)

**Goal**: XBRL contexts with validation

**Story Points**: 13

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-37 | Implement XBRL context entity and CRUD | Story | 5 | Backend Dev | Sprint 8 |
| ESRS-38 | Add context validation | Task | 3 | Backend Dev | ESRS-37 |
| ESRS-39 | Create context templates | Task | 2 | Backend Dev | ESRS-37 |
| ESRS-40 | Auto-suggest most used contexts | Task | 3 | Backend Dev | ESRS-37 |

### Context Examples

**Instant Context** (Balance sheet):
```json
{
  "contextId": "ctx_2023_12_31",
  "entityIdentifier": "12345678",
  "periodType": "instant",
  "instantDate": "2023-12-31"
}
```

**Duration Context** (Income statement):
```json
{
  "contextId": "ctx_2023_fy",
  "entityIdentifier": "12345678",
  "periodType": "duration",
  "startDate": "2023-01-01",
  "endDate": "2023-12-31"
}
```

---

## Sprint 10: Taxonomy Management (Weeks 21-22)

**Goal**: Upload and assign taxonomies to workspaces

**Story Points**: 16

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-41 | Implement taxonomy upload (admin) | Story | 5 | Backend Dev | Sprint 9 |
| ESRS-42 | Parse taxonomy metadata | Task | 5 | Backend Dev | ESRS-41 |
| ESRS-43 | Implement workspace taxonomy assignment | Story | 3 | Backend Dev | ESRS-42 |
| ESRS-44 | Create taxonomy browsing endpoint | Task | 3 | Backend Dev | ESRS-43 |

### Taxonomy Upload Test

1. Download ESRS taxonomy ZIP
2. Upload via POST /taxonomies (admin token)
3. Verify taxonomy.metadata contains:
   - namespace
   - schemaRefs
   - concept list (1000+ concepts)
4. Assign to workspace
5. Browse concepts: GET /taxonomies/:id/concepts?search=emission

---

## Sprint 11: XBRL Export (Weeks 23-24)

**Goal**: Generate iXBRL documents

**Story Points**: 21

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-45 | Implement iXBRL generation service | Story | 13 | Backend Dev | Sprint 10 |
| ESRS-46 | Create export endpoint | Story | 5 | Backend Dev | ESRS-45 |
| ESRS-47 | Implement XBRL validation | Task | 3 | Backend Dev | ESRS-45 |

### iXBRL Output Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
      xmlns:esrs-e1="http://www.esrs.eu/xbrl/esrs/e1">
  <head>
    <title>Annual Sustainability Report 2023</title>
    <link:schemaRef xlink:href="http://www.esrs.eu/xbrl/esrs/esrs-e1.xsd"/>
  </head>
  <body>
    <p>
      Total GHG emissions:
      <ix:nonFraction contextRef="ctx_2023_fy"
                      name="esrs-e1:ghgEmissions"
                      unitRef="tCO2e"
                      decimals="-3">12,500</ix:nonFraction>
      tonnes CO2 equivalent.
    </p>
  </body>
</html>
```

---

## Sprint 12: File Locking (Weeks 25-26)

**Goal**: Prevent concurrent edits with file locking

**Story Points**: 16

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-48 | Implement report lock acquisition | Story | 5 | Backend Dev | Sprint 11 |
| ESRS-49 | Implement lock refresh (heartbeat) | Story | 3 | Backend Dev | ESRS-48 |
| ESRS-50 | Implement lock release | Story | 2 | Backend Dev | ESRS-48 |
| ESRS-51 | Create lock status endpoint | Story | 2 | Backend Dev | ESRS-48 |
| ESRS-52 | Implement admin force unlock | Task | 2 | Backend Dev | ESRS-48 |
| ESRS-53 | Create expired lock cleanup cron | Task | 2 | Backend Dev | ESRS-48 |

### Lock Flow Testing

**Scenario 1: Successful locking**
1. User A: POST /reports/:id/lock → 200 OK
2. User A: PUT /reports/:id/lock/refresh (after 60s) → 200 OK
3. User A: DELETE /reports/:id/lock → 204 No Content

**Scenario 2: Conflict**
1. User A: POST /reports/:id/lock → 200 OK
2. User B: POST /reports/:id/lock → 409 Conflict
3. User B: GET /reports/:id/lock → Returns User A details

**Scenario 3: Auto-expire**
1. User A: POST /reports/:id/lock → 200 OK
2. Wait 15 minutes (no heartbeat)
3. Cron job runs, deletes lock
4. User B: POST /reports/:id/lock → 200 OK

---

## Sprint 13: Testing & Deployment (Weeks 27-28)

**Goal**: Write tests, optimize, and deploy to production

**Story Points**: 13

### Tasks

| ID | Task | Type | Points | Assignee | Dependencies |
|----|------|------|--------|----------|--------------|
| ESRS-54 | Write unit tests for core services | Task | 5 | Backend Dev | Sprint 12 |
| ESRS-55 | Write E2E tests for critical flows | Task | 5 | Backend Dev | Sprint 12 |
| ESRS-56 | Performance optimization | Task | 3 | Backend Dev | Sprint 12 |
| ESRS-57 | Deploy to Google Cloud Run | Task | 0 | DevOps | ESRS-56 |

### Test Coverage Goals

| Service | Target Coverage |
|---------|----------------|
| AuthService | 85% |
| ReportsService | 80% |
| TagsService | 80% |
| LocksService | 90% |
| XBRLService | 75% |

### Deployment Checklist

- [ ] Docker image built and pushed to Artifact Registry
- [ ] Environment variables configured in Cloud Run
- [ ] Cloud SQL connector configured
- [ ] Redis (Memorystore) connected
- [ ] GCS bucket accessible
- [ ] Health check endpoint responds: GET /health
- [ ] Smoke tests pass (register, login, upload, tag, export)
- [ ] Monitor logs for errors (first 24 hours)

---

## Sprint Retrospective Template

After each sprint, hold a retrospective using this template:

### What went well? 👍

- (Team adds items)

### What could be improved? 🔧

- (Team adds items)

### Action items for next sprint 📋

- (Team adds items with assignees)

### Metrics

| Metric | Value |
|--------|-------|
| Committed points | X |
| Completed points | Y |
| Velocity | Y |
| Completion rate | Y/X % |
| Bugs created | N |
| Bugs fixed | M |

---

**Last Updated**: 2025-11-03
**Total Sprints**: 13
**Total Story Points**: 205
**Duration**: 26 weeks
