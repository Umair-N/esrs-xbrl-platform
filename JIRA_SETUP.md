# JIRA SETUP GUIDE

Complete guide to setting up Jira for ESRS XBRL Platform project.

---

## Import User Stories

### Step 1: Import CSV

1. Go to your Jira project
2. Click **Project Settings** → **Import**
3. Select **CSV** as import type
4. Upload `jira-import.csv`
5. Map columns:
   - Summary → Summary
   - Issue Type → Issue Type
   - Priority → Priority
   - Story Points → Story Points (custom field)
   - Epic Name → Epic Name
   - Sprint → Sprint
   - Description → Description
   - Acceptance Criteria → Acceptance Criteria (custom field)
   - Labels → Labels
   - Component → Components
   - Assignee → Assignee

6. Click **Begin Import**

**Result**: 58 issues imported across 13 epics.

---

## Create Epics

Epics are automatically created from the "Epic Name" column. You should have:

1. **Sprint 0: Foundation Setup** (5 tasks, 13 points)
2. **Sprint 1: Multi-Tenancy Foundation** (4 tasks, 16 points)
3. **Sprint 2: Authentication** (4 tasks, 13 points)
4. **Sprint 3: Organization Management** (4 tasks, 16 points)
5. **Sprint 4: File Management** (4 tasks, 13 points)
6. **Sprint 5: PDF Processing** (4 tasks, 21 points)
7. **Sprint 6: Report Management** (4 tasks, 16 points)
8. **Sprint 7: Tagging System** (4 tasks, 16 points)
9. **Sprint 8: AI Integration** (3 tasks, 21 points)
10. **Sprint 9: Context Management** (4 tasks, 13 points)
11. **Sprint 10: Taxonomy Management** (4 tasks, 16 points)
12. **Sprint 11: XBRL Export** (3 tasks, 21 points)
13. **Sprint 12: File Locking** (6 tasks, 16 points)
14. **Sprint 13: Testing & Deployment** (4 tasks, 13 points)

**Total**: 58 stories, 205 story points

---

## Create Sprints

### Sprint Configuration

Each sprint is **2 weeks (10 working days)**.

**Recommended Sprint Schedule**:

| Sprint | Start Date | End Date | Story Points | Focus |
|--------|------------|----------|--------------|-------|
| Sprint 0 | Week 1 | Week 2 | 13 | Project setup, database init |
| Sprint 1 | Week 3 | Week 4 | 16 | Multi-tenancy, RLS |
| Sprint 2 | Week 5 | Week 6 | 13 | Authentication, JWT |
| Sprint 3 | Week 7 | Week 8 | 16 | Workspace members, invites |
| Sprint 4 | Week 9 | Week 10 | 13 | File upload, GCS |
| Sprint 5 | Week 11 | Week 12 | 21 | PDF processing, Bull queue |
| Sprint 6 | Week 13 | Week 14 | 16 | Reports, canvas |
| Sprint 7 | Week 15 | Week 16 | 16 | Tagging system |
| Sprint 8 | Week 17 | Week 18 | 21 | AI integration |
| Sprint 9 | Week 19 | Week 20 | 13 | XBRL contexts |
| Sprint 10 | Week 21 | Week 22 | 16 | Taxonomy management |
| Sprint 11 | Week 23 | Week 24 | 21 | iXBRL export |
| Sprint 12 | Week 25 | Week 26 | 16 | File locking |
| Sprint 13 | Week 27 | Week 28 | 13 | Testing, deployment |

### Create Sprints in Jira

1. Go to **Backlog**
2. Click **Create Sprint** (do this 14 times)
3. Name sprints: "Sprint 0", "Sprint 1", ... "Sprint 13"
4. Drag issues into corresponding sprints based on CSV "Sprint" column
5. Set start/end dates for each sprint

---

## Board Configuration

### Create Scrum Board

1. Go to **Project Settings** → **Boards**
2. Click **Create Board** → **Create a Scrum board**
3. Name: "ESRS XBRL Development Board"
4. Select your project

### Configure Columns

**Recommended columns**:

1. **Backlog** (default)
2. **To Do** → Status: To Do
3. **In Progress** → Status: In Progress
4. **Code Review** → Status: In Review (custom status)
5. **Testing** → Status: Testing (custom status)
6. **Done** → Status: Done

### Configure Swimlanes

**Option 1: By Epic**
- Shows all issues grouped by epic (Sprint 0, Sprint 1, etc.)

**Option 2: By Assignee**
- Shows issues grouped by developer

**Recommended**: Use "By Epic" for sprint planning, switch to "By Assignee" during sprint.

---

## Custom Fields

You'll need these custom fields (create if they don't exist):

### 1. Story Points

- **Type**: Number
- **Context**: All issue types
- **Description**: Effort estimation (Fibonacci: 1, 2, 3, 5, 8, 13, 21)

### 2. Acceptance Criteria

- **Type**: Text (multi-line)
- **Context**: Story, Task
- **Description**: Conditions that must be met for issue to be "Done"

### 3. Sprint

- **Type**: Sprint (built-in for Scrum projects)
- **Context**: All issue types

---

## Issue Types

Ensure you have these issue types:

1. **Epic** - Large feature (e.g., "Sprint 8: AI Integration")
2. **Story** - User-facing feature (e.g., "Implement JWT authentication")
3. **Task** - Technical work (e.g., "Setup Docker configuration")
4. **Bug** - Defects (create as needed during development)

---

## Components

Create these components for organization:

1. **Backend** - NestJS backend work
2. **Frontend** - Next.js frontend work
3. **Database** - PostgreSQL/TypeORM work
4. **DevOps** - Docker, CI/CD, deployment
5. **Testing** - Unit/E2E tests
6. **Documentation** - API docs, README updates

---

## Labels

Common labels from CSV:

- `setup` - Initial project setup
- `multi-tenancy` - Multi-tenant architecture
- `auth` - Authentication & authorization
- `files` - File management
- `pdf` - PDF processing
- `reports` - Report management
- `tagging` - XBRL tagging
- `ai` - AI integration
- `xbrl` - XBRL/iXBRL
- `taxonomy` - Taxonomy management
- `locking` - File locking
- `testing` - Testing tasks
- `performance` - Performance optimization
- `deployment` - Deployment tasks
- `backend` - Backend-specific
- `frontend` - Frontend-specific
- `database` - Database-specific
- `cloud` - Cloud services (GCS, Cloud Run)
- `migration` - Database migrations
- `cicd` - CI/CD pipeline

---

## Workflow

### Default Jira Workflow

**To Do** → **In Progress** → **Done**

### Recommended Custom Workflow

1. **Backlog** - Issue not yet prioritized
2. **To Do** - Ready to start
3. **In Progress** - Developer actively working
4. **Code Review** - Pull request submitted
5. **Testing** - QA or integration testing
6. **Done** - Merged to dev/master, deployed

### Transitions

- Backlog → To Do: Manual (during sprint planning)
- To Do → In Progress: Developer clicks "Start"
- In Progress → Code Review: Developer submits PR
- Code Review → Testing: PR approved and merged
- Testing → Done: Tests pass
- Any → Backlog: Issue blocked or deprioritized

---

## Automation Rules

### Rule 1: Auto-assign to reporter

**Trigger**: Issue created
**Action**: Set assignee to reporter (if part of project)

### Rule 2: Notify on sprint completion

**Trigger**: Sprint completed
**Action**: Send Slack/email with sprint summary (completed points, remaining work)

### Rule 3: Auto-close stale issues

**Trigger**: Issue in "In Progress" for >14 days
**Action**: Comment "Issue appears stale, please update" and move to "To Do"

### Rule 4: Auto-label backend tasks

**Trigger**: Issue contains "NestJS", "TypeORM", "PostgreSQL"
**Action**: Add "backend" label

---

## Sprint Ceremonies

### 1. Sprint Planning (Start of each sprint)

- **Duration**: 2 hours
- **Participants**: Whole team
- **Outcome**: Sprint backlog finalized, stories assigned

**Agenda**:
1. Review sprint goal (e.g., "Complete multi-tenancy foundation")
2. Review user stories for sprint
3. Break down stories into subtasks if needed
4. Assign stories to developers
5. Estimate capacity (team velocity)

### 2. Daily Standup (Every day)

- **Duration**: 15 minutes
- **Participants**: Dev team
- **Outcome**: Blockers identified, progress shared

**Questions**:
1. What did you complete yesterday?
2. What will you work on today?
3. Any blockers?

### 3. Sprint Review (End of each sprint)

- **Duration**: 1 hour
- **Participants**: Team + stakeholders
- **Outcome**: Demo completed work, gather feedback

**Agenda**:
1. Demo completed features
2. Review sprint metrics (velocity, burndown)
3. Stakeholder feedback

### 4. Sprint Retrospective (After sprint review)

- **Duration**: 1 hour
- **Participants**: Dev team
- **Outcome**: Identify improvements for next sprint

**Questions**:
1. What went well?
2. What could be improved?
3. Action items for next sprint

---

## JQL Queries (Jira Query Language)

### All open issues in current sprint

```jql
project = ESRS AND sprint in openSprints() AND status != Done
```

### My assigned issues

```jql
project = ESRS AND assignee = currentUser() AND status != Done
```

### All backend tasks

```jql
project = ESRS AND component = Backend AND status != Done
```

### High priority bugs

```jql
project = ESRS AND type = Bug AND priority = High AND status != Done
```

### Issues without story points

```jql
project = ESRS AND "Story Points" is EMPTY AND type in (Story, Task)
```

### Completed in last sprint

```jql
project = ESRS AND sprint = "Sprint 1" AND status = Done
```

### All AI integration stories

```jql
project = ESRS AND labels = ai
```

### Overdue issues

```jql
project = ESRS AND due < now() AND status != Done
```

---

## Dashboards

### Create "ESRS Overview" Dashboard

**Gadgets to add**:

1. **Sprint Burndown Chart**
   - Shows remaining work vs. ideal burndown
   - Helps track sprint progress

2. **Velocity Chart**
   - Shows completed story points per sprint
   - Helps estimate future capacity

3. **Epic Progress**
   - Shows completion % for each epic
   - Quick view of sprint goals

4. **Issue Statistics**
   - Pie chart: Issues by status
   - Pie chart: Issues by component

5. **Created vs Resolved**
   - Line chart showing issue creation vs resolution
   - Identifies scope creep

6. **Sprint Health**
   - Shows sprint capacity, committed points, completed points
   - Red/yellow/green indicator

---

## Filters

### Create Saved Filters

1. **My Sprint Work**
   ```jql
   assignee = currentUser() AND sprint in openSprints()
   ```
   - Share with team

2. **Backend Backlog**
   ```jql
   project = ESRS AND component = Backend AND status = "To Do"
   ```

3. **Blocked Issues**
   ```jql
   project = ESRS AND status = Blocked
   ```

4. **This Week's Completed**
   ```jql
   project = ESRS AND status = Done AND resolved >= -7d
   ```

---

## Team Roles

### Product Owner

- **Responsibilities**:
  - Prioritize backlog
  - Define acceptance criteria
  - Approve completed work
  - Stakeholder communication

- **Jira Permissions**: Admin

### Scrum Master

- **Responsibilities**:
  - Facilitate ceremonies
  - Remove blockers
  - Track sprint metrics
  - Improve process

- **Jira Permissions**: Admin

### Developers

- **Responsibilities**:
  - Estimate work
  - Complete assigned issues
  - Update issue status
  - Code review

- **Jira Permissions**: Edit issues, Transition issues

### QA Engineer

- **Responsibilities**:
  - Test completed stories
  - Create bug tickets
  - Verify fixes

- **Jira Permissions**: Create issues, Transition issues

---

## Metrics & Reporting

### Key Metrics to Track

1. **Velocity** - Story points completed per sprint
   - Target: 15-20 points per sprint (based on team size)

2. **Sprint Completion Rate** - % of committed stories completed
   - Target: >80%

3. **Cycle Time** - Time from "In Progress" to "Done"
   - Target: <5 days per story

4. **Defect Rate** - Bugs created vs stories completed
   - Target: <20%

5. **Code Review Time** - Time in "Code Review" status
   - Target: <1 day

### Generate Reports

1. **Burndown Report**
   - Shows remaining work over sprint
   - Accessible from Board → Reports

2. **Velocity Report**
   - Shows completed points per sprint
   - Helps forecast completion

3. **Cumulative Flow Diagram**
   - Shows work distribution across statuses
   - Identifies bottlenecks

4. **Sprint Report**
   - Summary of sprint: completed, incomplete, added mid-sprint

---

## Best Practices

### 1. Story Point Estimation

Use Fibonacci sequence: **1, 2, 3, 5, 8, 13, 21**

- **1 point** - Trivial (30 min - 1 hour)
- **2 points** - Simple (2-4 hours)
- **3 points** - Moderate (1 day)
- **5 points** - Complex (2-3 days)
- **8 points** - Very complex (1 week)
- **13 points** - Needs breakdown (should split)
- **21 points** - Too large (must split)

### 2. Acceptance Criteria

Every story/task should have clear acceptance criteria:

**Good Example**:
```
- User can upload PDF file
- File size validated (max 70MB)
- Only PDF/DOCX accepted
- File metadata returned in response
- Error shown for invalid files
```

**Bad Example**:
```
- File upload works
```

### 3. Issue Naming

**Good**:
- "Implement JWT authentication with RSA256"
- "Create POST /reports/:id/lock endpoint"
- "Fix: Tags not saving to database"

**Bad**:
- "Auth stuff"
- "Locking"
- "Bug fix"

### 4. Sprint Commitment

- Don't overcommit (target 70-80% of capacity)
- Reserve 20-30% for bugs, meetings, unplanned work
- Team velocity typically: 15-20 points per 2-week sprint (4 devs)

### 5. Work In Progress (WIP) Limits

- Max 2-3 stories "In Progress" per developer
- Prevents context switching
- Encourages completion before starting new work

---

## Troubleshooting

### Issue: CSV import fails

**Solution**:
- Ensure custom fields exist before import
- Check CSV format (UTF-8 encoding)
- Try importing 10 issues first as test

### Issue: Story points not showing

**Solution**:
- Add "Story Points" field to board view
- Go to Board Settings → Card Layout → Add "Story Points"

### Issue: Sprints not appearing in board

**Solution**:
- Check board filter (should include your project)
- Ensure issues are assigned to sprint
- Refresh browser

### Issue: Velocity chart empty

**Solution**:
- Need at least 1 completed sprint
- Ensure issues have story points
- Check sprint dates are set

---

## Quick Start Checklist

- [ ] Import `jira-import.csv` (58 issues)
- [ ] Create 14 sprints (Sprint 0 - Sprint 13)
- [ ] Configure board columns (To Do, In Progress, Code Review, Testing, Done)
- [ ] Create custom fields (Story Points, Acceptance Criteria)
- [ ] Create components (Backend, Frontend, Database, DevOps)
- [ ] Set up automation rules (at least 2)
- [ ] Create "ESRS Overview" dashboard
- [ ] Save common filters (My Sprint Work, Backend Backlog)
- [ ] Schedule sprint planning for Sprint 0
- [ ] Assign team roles (PO, Scrum Master, Devs)

---

**Last Updated**: 2025-11-03
**Project**: ESRS XBRL Platform
**Total Issues**: 58
**Total Sprints**: 13 (26 weeks)
**Total Story Points**: 205
