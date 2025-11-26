# JIRA MATERIALS - COMPLETE PACKAGE

All materials for setting up Jira project for ESRS XBRL Platform development.

---

## 📦 What's Included

This package contains everything you need to set up your Jira project:

### 1. **jira-import.csv** (Main Import File)
- **58 user stories** across 13 sprints
- **205 story points** total
- **26-week timeline** (13 two-week sprints)
- Complete with descriptions, acceptance criteria, labels, components

### 2. **JIRA_SETUP.md** (Setup Guide)
- Step-by-step import instructions
- Board configuration
- Custom fields setup
- Workflow configuration
- Automation rules
- JQL queries
- Dashboard templates

### 3. **SPRINT_BOARDS.md** (Sprint Templates)
- Detailed breakdown of all 13 sprints
- Task dependencies
- Testing checklists
- API examples
- Performance targets
- Retrospective templates

---

## 🚀 Quick Start (5 Steps)

### Step 1: Create Jira Project

1. Go to Jira → **Create Project**
2. Select **Scrum** template
3. Name: `ESRS XBRL Platform`
4. Key: `ESRS`

### Step 2: Import CSV

1. Go to **Project Settings** → **Import**
2. Upload `jira-import.csv`
3. Map columns (see JIRA_SETUP.md for details)
4. Click **Begin Import**
5. Wait for 58 issues to import

### Step 3: Create Sprints

1. Go to **Backlog**
2. Create 14 sprints: "Sprint 0" through "Sprint 13"
3. Drag issues into corresponding sprints
4. Set start/end dates (2 weeks per sprint)

### Step 4: Configure Board

1. Go to **Board Settings**
2. Add columns: To Do → In Progress → Code Review → Testing → Done
3. Configure swimlanes: Group by Epic
4. Add card fields: Story Points, Labels, Component

### Step 5: Start Sprint 0

1. Select Sprint 0 in backlog
2. Click **Start Sprint**
3. Set sprint goal: "Complete project setup and database initialization"
4. Schedule sprint planning meeting

---

## 📊 Project Overview

### Timeline

| Phase | Sprints | Duration | Story Points | Focus |
|-------|---------|----------|--------------|-------|
| **Foundation** | 0-1 | 4 weeks | 29 | Setup, multi-tenancy |
| **Core Platform** | 2-7 | 12 weeks | 89 | Auth, files, reports, tagging |
| **Advanced Features** | 8-11 | 8 weeks | 71 | AI, XBRL export, taxonomies |
| **Collaboration & Deploy** | 12-13 | 4 weeks | 29 | Locking, testing, deployment |
| **TOTAL** | **0-13** | **28 weeks** | **218** | **Full platform** |

### Team Composition (Recommended)

- **1 Tech Lead** - Architecture, code review
- **2 Backend Developers** - NestJS, PostgreSQL
- **1 Frontend Developer** - Next.js, React (not in CSV, separate planning needed)
- **1 DevOps Engineer** - Docker, Cloud Run, CI/CD

### Velocity Estimation

- **Team velocity**: 15-18 points per sprint (estimated for 3-4 developers)
- **Actual points per sprint**: Average 15.8 points
- **Completion target**: 80% of committed points

---

## 📋 All User Stories Summary

### Sprint 0: Foundation Setup (13 points)
1. Setup NestJS with prime-nestjs (3)
2. Configure PostgreSQL Supabase (5)
3. Create database migrations (3)
4. Setup Docker (2)
5. Configure CI/CD (0)

### Sprint 1: Multi-Tenancy (16 points)
6. Organization entity & CRUD (5)
7. Workspace entity & CRUD (5)
8. Row-Level Security policies (3)
9. Workspace middleware (3)

### Sprint 2: Authentication (13 points)
10. User entity & repository (5)
11. JWT authentication (5)
12. Auth endpoints (3)
13. Refresh token rotation (0)

### Sprint 3: Organization Management (16 points)
14. Workspace member management (5)
15. Invitation system (5)
16. Workspace guard (3)
17. Role-based access control (3)

### Sprint 4: File Management (13 points)
18. File upload endpoint (5)
19. Google Cloud Storage integration (3)
20. File metadata extraction (3)
21. File download endpoint (2)

### Sprint 5: PDF Processing (21 points)
22. PDF text extraction (5)
23. Word-level bounding boxes (8)
24. Render pages to JPEG (5)
25. Bull queue for async processing (3)

### Sprint 6: Report Management (16 points)
26. Report entity & CRUD (5)
27. Canvas persistence (5)
28. Report listing with filters (3)
29. Workspace-level sharing (3)

### Sprint 7: Tagging System (16 points)
30. Tag entity & CRUD (5)
31. Tag listing with grouping (3)
32. Tag validation (3)
33. Tag conflict detection (5)

### Sprint 8: AI Integration (21 points)
34. OpenAI API integration (8)
35. AI recommendation endpoint (8)
36. Context suggestion (5)

### Sprint 9: Context Management (13 points)
37. XBRL context entity & CRUD (5)
38. Context validation (3)
39. Context templates (2)
40. Auto-suggest contexts (3)

### Sprint 10: Taxonomy Management (16 points)
41. Taxonomy upload (admin) (5)
42. Parse taxonomy metadata (5)
43. Workspace taxonomy assignment (3)
44. Taxonomy browsing endpoint (3)

### Sprint 11: XBRL Export (21 points)
45. iXBRL generation service (13)
46. Export endpoint (5)
47. XBRL validation (3)

### Sprint 12: File Locking (16 points)
48. Lock acquisition (5)
49. Lock refresh (heartbeat) (3)
50. Lock release (2)
51. Lock status endpoint (2)
52. Admin force unlock (2)
53. Expired lock cleanup cron (2)

### Sprint 13: Testing & Deployment (13 points)
54. Unit tests for core services (5)
55. E2E tests for critical flows (5)
56. Performance optimization (3)
57. Deploy to Google Cloud Run (0)

---

## 🏷️ Labels & Components

### Labels (22 total)

**By Feature**:
- `multi-tenancy` - Multi-tenant architecture (9 issues)
- `auth` - Authentication & authorization (7 issues)
- `files` - File management (4 issues)
- `pdf` - PDF processing (4 issues)
- `reports` - Report management (4 issues)
- `tagging` - XBRL tagging (4 issues)
- `ai` - AI integration (3 issues)
- `xbrl` - XBRL/iXBRL (5 issues)
- `taxonomy` - Taxonomy management (4 issues)
- `locking` - File locking (6 issues)

**By Type**:
- `setup` - Initial setup (5 issues)
- `testing` - Testing tasks (2 issues)
- `performance` - Performance optimization (1 issue)
- `deployment` - Deployment tasks (1 issue)

**By Layer**:
- `backend` - Backend-specific (52 issues)
- `frontend` - Frontend-specific (0 issues in backend CSV)
- `database` - Database-specific (3 issues)
- `cloud` - Cloud services (1 issue)

### Components (4 main)

1. **Backend** - NestJS, TypeORM, PostgreSQL (52 issues)
2. **Database** - Schema, migrations, RLS (3 issues)
3. **DevOps** - Docker, CI/CD, deployment (3 issues)
4. **Testing** - Unit, E2E, integration tests (2 issues)

---

## 📈 Metrics & KPIs

### Sprint Metrics to Track

1. **Velocity** - Story points completed per sprint
   - Target: 15-18 points/sprint
   - Chart: Velocity Chart in Jira

2. **Sprint Completion Rate** - % of committed stories completed
   - Target: >80%
   - Formula: (Completed points / Committed points) × 100

3. **Cycle Time** - Time from "In Progress" to "Done"
   - Target: <5 days per story
   - Track in: Cumulative Flow Diagram

4. **Burndown** - Remaining work vs. ideal burndown
   - Chart: Sprint Burndown in Jira
   - Goal: Follow ideal line

5. **Defect Rate** - Bugs per completed story
   - Target: <0.2 (1 bug per 5 stories)
   - Track manually in retrospectives

### Project Health Indicators

| Indicator | Green | Yellow | Red |
|-----------|-------|--------|-----|
| Sprint completion | >85% | 70-85% | <70% |
| Velocity trend | Stable/up | Fluctuating | Declining |
| Blocked issues | 0 | 1-2 | 3+ |
| Overdue issues | 0 | 1-3 | 4+ |
| Test coverage | >80% | 70-80% | <70% |

---

## 🎯 Definition of Done

Every story/task must meet these criteria before moving to "Done":

### Code Quality
- [ ] Code follows CODING_STANDARDS.md
- [ ] TypeScript strict mode (no `any` types)
- [ ] All linting errors resolved
- [ ] Code reviewed and approved by 1+ developer

### Testing
- [ ] Unit tests written (target 80% coverage for services)
- [ ] Integration/E2E tests for critical paths
- [ ] All tests passing in CI pipeline
- [ ] Manual testing completed (if applicable)

### Documentation
- [ ] API endpoints documented (Swagger)
- [ ] README updated (if public-facing feature)
- [ ] Code comments for complex logic
- [ ] Acceptance criteria met and verified

### Security
- [ ] No SQL injection vulnerabilities
- [ ] Input validation implemented
- [ ] Authorization checks in place (RLS, guards)
- [ ] Secrets not hardcoded

### Deployment
- [ ] Merged to `dev` branch
- [ ] CI/CD pipeline passes
- [ ] Deployed to staging (if applicable)
- [ ] Smoke tested in staging

---

## 🔧 Jira Automation Rules

Set up these automation rules to save time:

### Rule 1: Auto-transition on PR merge

**Trigger**: GitHub webhook - PR merged
**Condition**: PR title contains Jira issue key (e.g., "ESRS-10")
**Action**: Transition issue to "Testing"

### Rule 2: Notify on blocked issues

**Trigger**: Issue transitioned to "Blocked"
**Action**:
- Comment: "Issue blocked, please update with blocker details"
- Send Slack notification to #dev-blockers channel
- Assign to Scrum Master

### Rule 3: Auto-close stale issues

**Trigger**: Scheduled (daily)
**Condition**: Issue in "In Progress" for >14 days
**Action**:
- Comment: "Issue appears stale, moving back to To Do"
- Transition to "To Do"

### Rule 4: Sprint health check

**Trigger**: Scheduled (every Monday during sprint)
**Condition**: Sprint in progress
**Action**:
- Calculate completion percentage
- Send Slack message with burndown chart link

---

## 📚 Additional Resources

### Documentation Files

All documentation is in the project directory:

1. **PROJECT_OVERVIEW.md** - High-level architecture, tech stack
2. **DATABASE_SCHEMA.md** - Complete 14-table schema
3. **API_ENDPOINTS.md** - All REST API endpoints
4. **CODING_STANDARDS.md** - NestJS and Next.js patterns
5. **CUSTOM_INSTRUCTIONS.md** - ChatGPT Project setup

### External Resources

- **NestJS Docs**: https://docs.nestjs.com/
- **TypeORM Docs**: https://typeorm.io/
- **Prime-NestJS**: https://github.com/josephgoksu/prime-nestjs
- **XBRL Spec**: https://www.xbrl.org/
- **ESRS Standards**: https://www.efrag.org/

---

## 🆘 Troubleshooting

### Issue: CSV import fails

**Symptoms**: Import hangs or shows error
**Solution**:
1. Ensure custom fields exist (Story Points, Acceptance Criteria)
2. Check CSV encoding is UTF-8
3. Try importing in batches (20 issues at a time)

### Issue: Story points not showing on board

**Symptoms**: Cards don't display points
**Solution**:
1. Go to **Board Settings** → **Card Layout**
2. Add "Story Points" field
3. Refresh board

### Issue: Epics not linking to stories

**Symptoms**: Stories not showing under epics
**Solution**:
1. Check "Epic Name" matches exactly
2. Manually link: Open story → "Epic Link" → Select epic
3. Re-import with correct epic names

### Issue: Sprints empty after import

**Symptoms**: All issues in backlog
**Solution**:
1. Create sprints first: Sprint 0, Sprint 1, etc.
2. Drag issues from backlog into correct sprint
3. Alternatively: Re-import CSV after creating sprints

---

## ✅ Post-Import Checklist

After importing CSV and setting up Jira:

- [ ] All 58 issues imported successfully
- [ ] 14 epics created and linked to stories
- [ ] 14 sprints created (Sprint 0 - Sprint 13)
- [ ] Issues assigned to correct sprints
- [ ] Board columns configured (5 columns)
- [ ] Custom fields visible on cards
- [ ] Swimlanes set to "By Epic"
- [ ] Components created (Backend, Frontend, Database, DevOps)
- [ ] Automation rules configured (at least 2)
- [ ] Dashboard created with velocity chart
- [ ] Team members added to project
- [ ] First sprint planning meeting scheduled

---

## 🎉 Ready to Start!

You now have everything you need to kick off development:

### Next Steps

1. **Sprint 0 Planning** (Week 1, Day 1)
   - Review 5 tasks in Sprint 0
   - Assign tasks to developers
   - Set sprint goal
   - Start sprint

2. **Daily Standups** (Every morning, 15 min)
   - What did you complete?
   - What are you working on?
   - Any blockers?

3. **Mid-Sprint Check** (Week 1, Day 5)
   - Review burndown chart
   - Identify risks
   - Re-prioritize if needed

4. **Sprint Review** (Week 2, Day 10)
   - Demo completed work
   - Gather feedback
   - Update product backlog

5. **Sprint Retrospective** (Week 2, Day 10)
   - What went well?
   - What to improve?
   - Action items for Sprint 1

---

## 📞 Support

If you encounter issues or need help:

1. **Check documentation** - All .md files in project directory
2. **Search Jira Community** - https://community.atlassian.com/
3. **ChatGPT Project** - Upload 5 docs for AI assistance
4. **Team discussion** - Slack or team chat

---

**Last Updated**: 2025-11-03
**Version**: 1.0
**Total Issues**: 58
**Total Sprints**: 13
**Timeline**: 26 weeks
**Status**: Ready for Import

---

**Good luck with your ESRS XBRL Platform development!** 🚀
