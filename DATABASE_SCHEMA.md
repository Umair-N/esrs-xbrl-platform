# DATABASE SCHEMA

Complete PostgreSQL database schema for ESRS XBRL Platform with Row-Level Security (RLS) and multi-tenancy support.

---

## Overview

- **Total Tables**: 14
- **Primary Keys**: UUID (not integer) for distributed scalability
- **Tenant Isolation**: Row-Level Security (RLS) on workspace-scoped tables
- **Soft Deletes**: All entities have `deleted_at` timestamp
- **Audit Trail**: Comprehensive logging in `audit_logs` table

---

## Table Definitions

### 1. Organizations (Top-Level Tenants)

```sql
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_organizations_slug ON organizations(slug) WHERE deleted_at IS NULL;
CREATE INDEX idx_organizations_deleted ON organizations(deleted_at);
```

**Description**: Companies or top-level tenant entities. Each organization can have multiple workspaces.

**Key Fields**:
- `slug` - URL-friendly identifier (e.g., "acme-corp")
- `settings` - JSON configuration (branding, limits, features)

---

### 2. Workspaces (Isolated Environments)

```sql
CREATE TABLE workspaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(100) NOT NULL,
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP NULL,
  UNIQUE(organization_id, slug)
);

CREATE INDEX idx_workspaces_org ON workspaces(organization_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_workspaces_slug ON workspaces(organization_id, slug);
CREATE INDEX idx_workspaces_deleted ON workspaces(deleted_at);
```

**Description**: Isolated environments within an organization (e.g., teams, projects, departments). All resources are scoped to a workspace.

**Key Fields**:
- `organization_id` - Parent organization
- `slug` - Unique within organization (e.g., "finance-team")
- `settings` - Workspace-specific configuration

---

### 3. Users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  role VARCHAR(50) DEFAULT 'user',
  is_active BOOLEAN DEFAULT true,
  email_verified BOOLEAN DEFAULT false,
  last_login_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_org ON users(organization_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_deleted ON users(deleted_at);
```

**Description**: User accounts belonging to an organization.

**Roles**:
- `super_admin` - Platform-wide admin
- `org_admin` - Organization administrator
- `workspace_admin` - Workspace administrator
- `editor` - Can create and edit reports
- `viewer` - Read-only access

---

### 4. Workspace Members

```sql
CREATE TABLE workspace_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(50) DEFAULT 'viewer',
  joined_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(workspace_id, user_id)
);

CREATE INDEX idx_workspace_members_workspace ON workspace_members(workspace_id);
CREATE INDEX idx_workspace_members_user ON workspace_members(user_id);
CREATE INDEX idx_workspace_members_role ON workspace_members(role);
```

**Description**: Maps users to workspaces with role-based access control.

**Workspace Roles**:
- `admin` - Full workspace control
- `editor` - Create/edit reports and tags
- `viewer` - Read-only access

---

### 5. Refresh Tokens

```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(500) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  revoked_at TIMESTAMP NULL
);

CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token) WHERE revoked_at IS NULL;
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at);
```

**Description**: JWT refresh tokens for authentication. Supports token rotation and revocation.

---

### 6. Invitations

```sql
CREATE TABLE invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  email VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'viewer',
  invited_by_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(255) UNIQUE NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  expires_at TIMESTAMP NOT NULL,
  accepted_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_invitations_workspace ON invitations(workspace_id);
CREATE INDEX idx_invitations_email ON invitations(email);
CREATE INDEX idx_invitations_token ON invitations(token);
CREATE INDEX idx_invitations_status ON invitations(status);
```

**Description**: Pending workspace invitations sent via email.

**Statuses**:
- `pending` - Invitation sent, awaiting acceptance
- `accepted` - User joined workspace
- `expired` - Token expired
- `revoked` - Invitation cancelled

---

### 7. Files

```sql
CREATE TABLE files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  uploaded_by_id UUID NOT NULL REFERENCES users(id),
  filename VARCHAR(255) NOT NULL,
  original_filename VARCHAR(255) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  file_size BIGINT NOT NULL,
  storage_path VARCHAR(500) NOT NULL,
  storage_backend VARCHAR(50) DEFAULT 'local',
  mime_type VARCHAR(100),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_files_workspace ON files(workspace_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_files_uploader ON files(uploaded_by_id);
CREATE INDEX idx_files_type ON files(file_type);
CREATE INDEX idx_files_deleted ON files(deleted_at);

-- RLS Policy
ALTER TABLE files ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON files
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Description**: Uploaded documents (PDF/DOCX) with metadata.

**Key Fields**:
- `storage_backend` - 'local' or 'gcs'
- `storage_path` - Path in storage system
- `metadata` - File-specific info (page count, dimensions, etc.)

---

### 8. PDF Cache

```sql
CREATE TABLE pdf_cache (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  page_number INT NOT NULL,
  text_content TEXT,
  word_data JSONB,
  image_data BYTEA,
  image_mime_type VARCHAR(50) DEFAULT 'image/jpeg',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(file_id, page_number)
);

CREATE INDEX idx_pdf_cache_file ON pdf_cache(file_id);
CREATE INDEX idx_pdf_cache_workspace ON pdf_cache(workspace_id);
CREATE INDEX idx_pdf_cache_page ON pdf_cache(file_id, page_number);

-- RLS Policy
ALTER TABLE pdf_cache ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON pdf_cache
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Description**: Preprocessed PDF data for instant loading. Stores extracted text, word bounding boxes, and rendered images.

**Key Fields**:
- `word_data` - JSON array of `{text, x, y, width, height}` for each word
- `image_data` - JPEG image of rendered page
- `metadata` - Page dimensions, rendering info

**Performance**: Enables instant PDF reload without re-processing.

---

### 9. Reports

```sql
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  file_id UUID REFERENCES files(id) ON DELETE SET NULL,
  created_by_id UUID NOT NULL REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  taxonomy_id UUID REFERENCES taxonomies(id),
  status VARCHAR(50) DEFAULT 'draft',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_reports_workspace ON reports(workspace_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_reports_file ON reports(file_id);
CREATE INDEX idx_reports_creator ON reports(created_by_id);
CREATE INDEX idx_reports_taxonomy ON reports(taxonomy_id);
CREATE INDEX idx_reports_status ON reports(status);
CREATE INDEX idx_reports_deleted ON reports(deleted_at);

-- RLS Policy
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON reports
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Description**: XBRL reports with associated documents and tags.

**Statuses**:
- `draft` - Work in progress
- `review` - Under review
- `approved` - Ready for export
- `published` - Exported as iXBRL

---

### 10. Tags

```sql
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  created_by_id UUID NOT NULL REFERENCES users(id),
  context_id UUID REFERENCES xbrl_contexts(id),
  concept_id VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  unit VARCHAR(50),
  decimals INT DEFAULT -3,
  start_index INT,
  end_index INT,
  page_number INT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_tags_report ON tags(report_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_tags_workspace ON tags(workspace_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_tags_creator ON tags(created_by_id);
CREATE INDEX idx_tags_context ON tags(context_id);
CREATE INDEX idx_tags_concept ON tags(concept_id);
CREATE INDEX idx_tags_page ON tags(page_number);
CREATE INDEX idx_tags_deleted ON tags(deleted_at);

-- RLS Policy
ALTER TABLE tags ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON tags
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Description**: XBRL concept tags applied to document text selections.

**Key Fields**:
- `concept_id` - XBRL concept (e.g., "esrs_e1:ghgEmissions")
- `context_id` - Entity, period, dimensions for this fact
- `start_index`/`end_index` - Character positions in document
- `page_number` - Page where tag appears
- `unit` - Measurement unit (e.g., "EUR", "tCO2e")
- `decimals` - Rounding precision

---

### 11. Canvases

```sql
CREATE TABLE canvases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID UNIQUE NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  canvas_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_canvases_report ON canvases(report_id);
CREATE INDEX idx_canvases_workspace ON canvases(workspace_id);

-- RLS Policy
ALTER TABLE canvases ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON canvases
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Description**: Persisted editor state for resuming editing sessions.

**Canvas Data Structure**:
```json
{
  "blocks": [...],
  "tags": [...],
  "scrollPosition": 0,
  "selectedContextId": "uuid",
  "version": "1.0"
}
```

---

### 12. XBRL Contexts

```sql
CREATE TABLE xbrl_contexts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  context_id VARCHAR(255) NOT NULL,
  entity_identifier VARCHAR(255) NOT NULL,
  entity_scheme VARCHAR(255) DEFAULT 'http://www.esrs.eu',
  period_type VARCHAR(50) NOT NULL,
  instant_date DATE,
  start_date DATE,
  end_date DATE,
  dimensions JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(report_id, context_id)
);

CREATE INDEX idx_xbrl_contexts_report ON xbrl_contexts(report_id);
CREATE INDEX idx_xbrl_contexts_workspace ON xbrl_contexts(workspace_id);
CREATE INDEX idx_xbrl_contexts_context_id ON xbrl_contexts(context_id);
CREATE INDEX idx_xbrl_contexts_period ON xbrl_contexts(period_type);

-- RLS Policy
ALTER TABLE xbrl_contexts ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON xbrl_contexts
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Description**: XBRL context definitions (entity, period, dimensions) for tagging facts.

**Period Types**:
- `instant` - Point in time (e.g., balance sheet date)
- `duration` - Time range (e.g., fiscal year)

**Example Context**:
```json
{
  "context_id": "ctx_2023_fy",
  "entity_identifier": "12345678",
  "period_type": "duration",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "dimensions": {
    "esrs:BusinessSegment": "EU Operations"
  }
}
```

---

### 13. Taxonomies

```sql
CREATE TABLE taxonomies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  version VARCHAR(50) NOT NULL,
  taxonomy_type VARCHAR(50) NOT NULL,
  storage_path VARCHAR(500) NOT NULL,
  storage_backend VARCHAR(50) DEFAULT 'local',
  is_active BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}',
  uploaded_by_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP NULL,
  UNIQUE(name, version)
);

CREATE INDEX idx_taxonomies_name ON taxonomies(name) WHERE deleted_at IS NULL;
CREATE INDEX idx_taxonomies_type ON taxonomies(taxonomy_type);
CREATE INDEX idx_taxonomies_active ON taxonomies(is_active);
CREATE INDEX idx_taxonomies_deleted ON taxonomies(deleted_at);
```

**Description**: XBRL taxonomy files (ESRS, GRI, SASB) uploaded by admins.

**Taxonomy Types**:
- `esrs` - European Sustainability Reporting Standard
- `gri` - Global Reporting Initiative
- `sasb` - Sustainability Accounting Standards Board

**Key Fields**:
- `storage_path` - Path to ZIP file in storage
- `metadata` - Taxonomy info (namespace, schemaRefs, etc.)

---

### 14. Workspace Taxonomies

```sql
CREATE TABLE workspace_taxonomies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  taxonomy_id UUID NOT NULL REFERENCES taxonomies(id) ON DELETE CASCADE,
  is_default BOOLEAN DEFAULT false,
  assigned_at TIMESTAMP DEFAULT NOW(),
  assigned_by_id UUID REFERENCES users(id),
  UNIQUE(workspace_id, taxonomy_id)
);

CREATE INDEX idx_workspace_taxonomies_workspace ON workspace_taxonomies(workspace_id);
CREATE INDEX idx_workspace_taxonomies_taxonomy ON workspace_taxonomies(taxonomy_id);
CREATE INDEX idx_workspace_taxonomies_default ON workspace_taxonomies(is_default);
```

**Description**: Maps taxonomies to workspaces. Each workspace can have multiple taxonomies.

**Key Fields**:
- `is_default` - Primary taxonomy for workspace (only one per workspace)

---

### 15. Report Locks

```sql
CREATE TABLE report_locks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID UNIQUE NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  locked_by_id UUID NOT NULL REFERENCES users(id),
  locked_at TIMESTAMP DEFAULT NOW(),
  last_activity_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL,
  lock_type VARCHAR(50) DEFAULT 'edit',
  client_info JSONB
);

CREATE INDEX idx_report_locks_report ON report_locks(report_id);
CREATE INDEX idx_report_locks_workspace ON report_locks(workspace_id);
CREATE INDEX idx_report_locks_user ON report_locks(locked_by_id);
CREATE INDEX idx_report_locks_expires ON report_locks(expires_at);

-- RLS Policy
ALTER TABLE report_locks ENABLE ROW LEVEL SECURITY;
CREATE POLICY workspace_isolation ON report_locks
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Description**: File locking mechanism to prevent concurrent edits.

**Key Fields**:
- `expires_at` - Auto-unlock after 15 minutes of inactivity
- `last_activity_at` - Updated by heartbeat every 60 seconds
- `client_info` - User agent, IP address for debugging

**Behavior**:
- Only one user can edit at a time
- Others see read-only mode with banner
- Admin can force unlock
- Cron job cleans expired locks every 5 minutes

---

### 16. Audit Logs

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID REFERENCES workspaces(id) ON DELETE SET NULL,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  action VARCHAR(100) NOT NULL,
  entity_type VARCHAR(100) NOT NULL,
  entity_id UUID,
  changes JSONB,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_workspace ON audit_logs(workspace_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at DESC);
```

**Description**: Comprehensive activity logging for compliance and debugging.

**Actions**:
- `CREATE`, `UPDATE`, `DELETE` - CRUD operations
- `LOGIN`, `LOGOUT` - Authentication events
- `INVITE`, `ACCEPT_INVITE` - User management
- `LOCK`, `UNLOCK` - File locking events
- `EXPORT` - iXBRL export events

**Example Entry**:
```json
{
  "action": "UPDATE",
  "entity_type": "tags",
  "entity_id": "uuid",
  "changes": {
    "old": {"value": "100"},
    "new": {"value": "150"}
  }
}
```

---

## Row-Level Security (RLS) Implementation

### Middleware Setup

```typescript
// src/common/middleware/workspace.middleware.ts
@Injectable()
export class WorkspaceMiddleware implements NestMiddleware {
  async use(req: Request, res: Response, next: NextFunction) {
    const workspaceId = req.headers['x-workspace-id'] || req.user?.currentWorkspaceId;

    if (workspaceId) {
      // Set PostgreSQL session variable for RLS
      await this.dataSource.query(
        'SET app.current_workspace_id = $1',
        [workspaceId]
      );
    }

    next();
  }
}
```

### RLS Policies

Applied to all workspace-scoped tables:

```sql
-- Enable RLS
ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY workspace_isolation ON {table_name}
  USING (workspace_id = current_setting('app.current_workspace_id')::uuid);
```

**Tables with RLS**:
- files
- pdf_cache
- reports
- tags
- canvases
- xbrl_contexts
- report_locks

---

## Database Migrations (TypeORM)

### Initial Migration

```bash
# Generate migration
npm run migration:generate -- src/database/migrations/InitialSchema

# Apply migration
npm run migration:run
```

### Migration File Structure

```typescript
// src/database/migrations/1234567890-InitialSchema.ts
export class InitialSchema1234567890 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    // Create tables
    await queryRunner.createTable(new Table({
      name: 'organizations',
      columns: [
        { name: 'id', type: 'uuid', isPrimary: true, default: 'gen_random_uuid()' },
        { name: 'name', type: 'varchar', length: '255', isNullable: false },
        // ... more columns
      ]
    }));

    // Create indexes
    await queryRunner.createIndex('organizations', new Index({
      columnNames: ['slug'],
      where: 'deleted_at IS NULL'
    }));

    // Enable RLS
    await queryRunner.query('ALTER TABLE files ENABLE ROW LEVEL SECURITY');
    await queryRunner.query(`
      CREATE POLICY workspace_isolation ON files
        USING (workspace_id = current_setting('app.current_workspace_id')::uuid)
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    // Reverse all changes
  }
}
```

---

## Database Connection Configuration

### TypeORM Config

```typescript
// src/database/data-source.ts
export const dataSource = new DataSource({
  type: 'postgres',
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT || '5432'),
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  ssl: {
    rejectUnauthorized: true,
  },
  entities: ['src/**/*.entity.ts'],
  migrations: ['src/database/migrations/*.ts'],
  synchronize: false, // NEVER use in production
  logging: process.env.NODE_ENV === 'development',
  poolSize: 10,
  extra: {
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000,
  },
});
```

---

## Performance Considerations

### Indexing Strategy

1. **Primary Keys**: UUID with clustered index
2. **Foreign Keys**: Indexed for JOIN performance
3. **Soft Deletes**: Partial indexes with `WHERE deleted_at IS NULL`
4. **Workspace Scoping**: Index on `workspace_id` for all RLS tables
5. **Timestamps**: Index on `created_at DESC` for pagination

### Query Optimization

1. **Use SELECT specific columns** (not SELECT *)
2. **Eager load relationships** with TypeORM `relations` option
3. **Paginate large result sets** with `take` and `skip`
4. **Use database views** for complex queries
5. **Cache frequently accessed data** (Redis)

### Connection Pooling

- **Min pool size**: 5 connections
- **Max pool size**: 20 connections
- **Idle timeout**: 30 seconds
- **Connection timeout**: 5 seconds

---

## Backup & Recovery

### Backup Strategy

1. **Automated Daily Backups** (Supabase handles this)
2. **Point-in-Time Recovery** (PITR) for last 7 days
3. **Manual Backups** before major migrations

### Restore Procedure

```bash
# Export database
pg_dump -h HOST -U USER -d DATABASE > backup.sql

# Restore database
psql -h HOST -U USER -d DATABASE < backup.sql
```

---

## dbdiagram.io Import

Complete DBML schema for visualization:

```dbml
Table organizations {
  id uuid [pk]
  name varchar(255) [not null]
  slug varchar(100) [unique, not null]
  settings jsonb
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp
}

Table workspaces {
  id uuid [pk]
  organization_id uuid [ref: > organizations.id, not null]
  name varchar(255) [not null]
  slug varchar(100) [not null]
  settings jsonb
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp

  indexes {
    (organization_id, slug) [unique]
  }
}

Table users {
  id uuid [pk]
  organization_id uuid [ref: > organizations.id, not null]
  email varchar(255) [unique, not null]
  password_hash varchar(255) [not null]
  first_name varchar(100)
  last_name varchar(100)
  role varchar(50) [default: 'user']
  is_active boolean [default: true]
  email_verified boolean [default: false]
  last_login_at timestamp
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp
}

Table workspace_members {
  id uuid [pk]
  workspace_id uuid [ref: > workspaces.id, not null]
  user_id uuid [ref: > users.id, not null]
  role varchar(50) [default: 'viewer']
  joined_at timestamp [default: `now()`]

  indexes {
    (workspace_id, user_id) [unique]
  }
}

Table refresh_tokens {
  id uuid [pk]
  user_id uuid [ref: > users.id, not null]
  token varchar(500) [unique, not null]
  expires_at timestamp [not null]
  created_at timestamp [default: `now()`]
  revoked_at timestamp
}

Table invitations {
  id uuid [pk]
  workspace_id uuid [ref: > workspaces.id, not null]
  email varchar(255) [not null]
  role varchar(50) [default: 'viewer']
  invited_by_id uuid [ref: > users.id, not null]
  token varchar(255) [unique, not null]
  status varchar(50) [default: 'pending']
  expires_at timestamp [not null]
  accepted_at timestamp
  created_at timestamp [default: `now()`]
}

Table files {
  id uuid [pk]
  workspace_id uuid [ref: > workspaces.id, not null]
  uploaded_by_id uuid [ref: > users.id, not null]
  filename varchar(255) [not null]
  original_filename varchar(255) [not null]
  file_type varchar(50) [not null]
  file_size bigint [not null]
  storage_path varchar(500) [not null]
  storage_backend varchar(50) [default: 'local']
  mime_type varchar(100)
  metadata jsonb
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp
}

Table pdf_cache {
  id uuid [pk]
  file_id uuid [ref: > files.id, not null]
  workspace_id uuid [ref: > workspaces.id, not null]
  page_number int [not null]
  text_content text
  word_data jsonb
  image_data bytea
  image_mime_type varchar(50) [default: 'image/jpeg']
  metadata jsonb
  created_at timestamp [default: `now()`]

  indexes {
    (file_id, page_number) [unique]
  }
}

Table reports {
  id uuid [pk]
  workspace_id uuid [ref: > workspaces.id, not null]
  file_id uuid [ref: > files.id]
  created_by_id uuid [ref: > users.id, not null]
  title varchar(255) [not null]
  description text
  taxonomy_id uuid [ref: > taxonomies.id]
  status varchar(50) [default: 'draft']
  metadata jsonb
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp
}

Table tags {
  id uuid [pk]
  report_id uuid [ref: > reports.id, not null]
  workspace_id uuid [ref: > workspaces.id, not null]
  created_by_id uuid [ref: > users.id, not null]
  context_id uuid [ref: > xbrl_contexts.id]
  concept_id varchar(255) [not null]
  value text [not null]
  unit varchar(50)
  decimals int [default: -3]
  start_index int
  end_index int
  page_number int
  metadata jsonb
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp
}

Table canvases {
  id uuid [pk]
  report_id uuid [ref: - reports.id, unique, not null]
  workspace_id uuid [ref: > workspaces.id, not null]
  canvas_data jsonb [not null]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table xbrl_contexts {
  id uuid [pk]
  report_id uuid [ref: > reports.id, not null]
  workspace_id uuid [ref: > workspaces.id, not null]
  context_id varchar(255) [not null]
  entity_identifier varchar(255) [not null]
  entity_scheme varchar(255) [default: 'http://www.esrs.eu']
  period_type varchar(50) [not null]
  instant_date date
  start_date date
  end_date date
  dimensions jsonb
  created_at timestamp [default: `now()`]

  indexes {
    (report_id, context_id) [unique]
  }
}

Table taxonomies {
  id uuid [pk]
  name varchar(255) [not null]
  version varchar(50) [not null]
  taxonomy_type varchar(50) [not null]
  storage_path varchar(500) [not null]
  storage_backend varchar(50) [default: 'local']
  is_active boolean [default: true]
  metadata jsonb
  uploaded_by_id uuid [ref: > users.id]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp

  indexes {
    (name, version) [unique]
  }
}

Table workspace_taxonomies {
  id uuid [pk]
  workspace_id uuid [ref: > workspaces.id, not null]
  taxonomy_id uuid [ref: > taxonomies.id, not null]
  is_default boolean [default: false]
  assigned_at timestamp [default: `now()`]
  assigned_by_id uuid [ref: > users.id]

  indexes {
    (workspace_id, taxonomy_id) [unique]
  }
}

Table report_locks {
  id uuid [pk]
  report_id uuid [ref: - reports.id, unique, not null]
  workspace_id uuid [ref: > workspaces.id, not null]
  locked_by_id uuid [ref: > users.id, not null]
  locked_at timestamp [default: `now()`]
  last_activity_at timestamp [default: `now()`]
  expires_at timestamp [not null]
  lock_type varchar(50) [default: 'edit']
  client_info jsonb
}

Table audit_logs {
  id uuid [pk]
  workspace_id uuid [ref: > workspaces.id]
  user_id uuid [ref: > users.id]
  action varchar(100) [not null]
  entity_type varchar(100) [not null]
  entity_id uuid
  changes jsonb
  ip_address varchar(45)
  user_agent text
  created_at timestamp [default: `now()`]
}
```

---

**Last Updated**: 2025-11-03
**Version**: 1.0
**Tables**: 14 (16 including audit_logs)
