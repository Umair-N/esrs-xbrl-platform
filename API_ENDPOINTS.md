# API ENDPOINTS

Complete REST API documentation for ESRS XBRL Platform backend (NestJS).

---

## Base URL

- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://api.esrs-xbrl.com/api/v1`

---

## Authentication

All endpoints (except public auth endpoints) require JWT authentication via `Authorization` header or httpOnly cookie.

```
Authorization: Bearer <access_token>
```

---

## Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "statusCode": 400
}
```

---

## 1. Authentication & Authorization

### POST `/auth/register`

Register a new organization and admin user.

**Request Body**:
```json
{
  "organizationName": "Acme Corp",
  "organizationSlug": "acme-corp",
  "email": "admin@acme.com",
  "password": "SecurePass123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "admin@acme.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "org_admin"
    },
    "organization": {
      "id": "uuid",
      "name": "Acme Corp",
      "slug": "acme-corp"
    },
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc..."
  }
}
```

---

### POST `/auth/login`

Login with email and password.

**Request Body**:
```json
{
  "email": "admin@acme.com",
  "password": "SecurePass123!"
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "admin@acme.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "org_admin",
      "organizationId": "uuid"
    },
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc..."
  }
}
```

**Cookies Set**:
- `access_token` (httpOnly, 30 min)
- `refresh_token` (httpOnly, 7 days)

---

### POST `/auth/refresh`

Refresh access token using refresh token.

**Request Body**:
```json
{
  "refreshToken": "eyJhbGc..."
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc..."
  }
}
```

---

### POST `/auth/logout`

Logout and revoke refresh token.

**Headers**: `Authorization: Bearer <token>`

**Response**: `200 OK`
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### GET `/auth/me`

Get current user profile.

**Headers**: `Authorization: Bearer <token>`

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "admin@acme.com",
    "firstName": "John",
    "lastName": "Doe",
    "role": "org_admin",
    "organizationId": "uuid",
    "isActive": true,
    "emailVerified": true,
    "lastLoginAt": "2025-11-03T10:00:00Z"
  }
}
```

---

## 2. Organizations

### GET `/organizations/:id`

Get organization details.

**Headers**:
- `Authorization: Bearer <token>`

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Acme Corp",
    "slug": "acme-corp",
    "settings": {
      "maxWorkspaces": 10,
      "allowedFileTypes": ["pdf", "docx"]
    },
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-01T00:00:00Z"
  }
}
```

---

### PATCH `/organizations/:id`

Update organization settings (org_admin only).

**Request Body**:
```json
{
  "name": "Acme Corporation",
  "settings": {
    "maxWorkspaces": 20
  }
}
```

**Response**: `200 OK`

---

## 3. Workspaces

### GET `/workspaces`

List all workspaces for current user.

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `page` (optional, default: 1)
- `limit` (optional, default: 20)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "workspaces": [
      {
        "id": "uuid",
        "name": "Finance Team",
        "slug": "finance-team",
        "organizationId": "uuid",
        "role": "admin",
        "settings": {},
        "createdAt": "2025-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 5,
      "totalPages": 1
    }
  }
}
```

---

### POST `/workspaces`

Create a new workspace (org_admin only).

**Request Body**:
```json
{
  "name": "Sustainability Team",
  "slug": "sustainability-team",
  "settings": {
    "defaultTaxonomy": "esrs"
  }
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Sustainability Team",
    "slug": "sustainability-team",
    "organizationId": "uuid",
    "createdAt": "2025-11-03T10:00:00Z"
  }
}
```

---

### GET `/workspaces/:id`

Get workspace details.

**Headers**:
- `Authorization: Bearer <token>`
- `X-Workspace-Id: <workspace_id>`

**Response**: `200 OK`

---

### PATCH `/workspaces/:id`

Update workspace (workspace_admin only).

**Request Body**:
```json
{
  "name": "Updated Name",
  "settings": {
    "defaultTaxonomy": "gri"
  }
}
```

**Response**: `200 OK`

---

### DELETE `/workspaces/:id`

Soft delete workspace (org_admin only).

**Response**: `204 No Content`

---

## 4. Workspace Members

### GET `/workspaces/:workspaceId/members`

List all members in workspace.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "members": [
      {
        "id": "uuid",
        "userId": "uuid",
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane@acme.com",
        "role": "editor",
        "joinedAt": "2025-01-15T00:00:00Z"
      }
    ]
  }
}
```

---

### POST `/workspaces/:workspaceId/members`

Add member to workspace (workspace_admin only).

**Request Body**:
```json
{
  "userId": "uuid",
  "role": "editor"
}
```

**Response**: `201 Created`

---

### PATCH `/workspaces/:workspaceId/members/:memberId`

Update member role (workspace_admin only).

**Request Body**:
```json
{
  "role": "admin"
}
```

**Response**: `200 OK`

---

### DELETE `/workspaces/:workspaceId/members/:memberId`

Remove member from workspace (workspace_admin only).

**Response**: `204 No Content`

---

## 5. Invitations

### POST `/invitations`

Invite user to workspace (workspace_admin only).

**Headers**: `X-Workspace-Id: <workspace_id>`

**Request Body**:
```json
{
  "email": "newuser@acme.com",
  "role": "editor"
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "newuser@acme.com",
    "role": "editor",
    "token": "inv_abc123",
    "expiresAt": "2025-11-10T10:00:00Z",
    "inviteLink": "https://app.esrs-xbrl.com/invite/inv_abc123"
  }
}
```

---

### POST `/invitations/:token/accept`

Accept workspace invitation (public endpoint).

**Request Body**:
```json
{
  "password": "SecurePass123!",
  "firstName": "Jane",
  "lastName": "Smith"
}
```

**Response**: `200 OK`

---

### GET `/invitations`

List pending invitations for workspace.

**Headers**: `X-Workspace-Id: <workspace_id>`

**Response**: `200 OK`

---

### DELETE `/invitations/:id`

Revoke invitation (workspace_admin only).

**Response**: `204 No Content`

---

## 6. Files

### POST `/files/upload`

Upload file (PDF/DOCX).

**Headers**:
- `Authorization: Bearer <token>`
- `X-Workspace-Id: <workspace_id>`
- `Content-Type: multipart/form-data`

**Form Data**:
- `file` (required) - File to upload (max 70MB)

**Response**: `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "filename": "report.pdf",
    "originalFilename": "Annual Report 2023.pdf",
    "fileType": "pdf",
    "fileSize": 2458624,
    "mimeType": "application/pdf",
    "storageBackend": "gcs",
    "metadata": {
      "pageCount": 50,
      "hasImages": true
    },
    "createdAt": "2025-11-03T10:00:00Z"
  }
}
```

---

### GET `/files/:id`

Get file metadata.

**Response**: `200 OK`

---

### GET `/files/:id/download`

Download file.

**Response**: `200 OK` (file stream or signed URL)
```json
{
  "success": true,
  "data": {
    "downloadUrl": "https://storage.googleapis.com/...",
    "expiresAt": "2025-11-03T11:00:00Z"
  }
}
```

---

### DELETE `/files/:id`

Soft delete file.

**Response**: `204 No Content`

---

## 7. PDF Cache

### GET `/pdf-cache/:fileId`

Get all cached pages for a PDF file.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "fileId": "uuid",
    "pages": [
      {
        "pageNumber": 1,
        "textContent": "Full text content...",
        "wordData": [
          {"text": "Hello", "x": 100, "y": 200, "width": 50, "height": 20}
        ],
        "imageUrl": "/api/v1/pdf-cache/uuid/pages/1/image",
        "metadata": {
          "width": 595,
          "height": 842
        }
      }
    ]
  }
}
```

---

### GET `/pdf-cache/:fileId/pages/:pageNumber`

Get specific page data.

**Response**: `200 OK`

---

### GET `/pdf-cache/:fileId/pages/:pageNumber/image`

Get page image (JPEG).

**Response**: `200 OK` (image/jpeg)

---

## 8. Reports

### GET `/reports`

List all reports in workspace.

**Headers**: `X-Workspace-Id: <workspace_id>`

**Query Parameters**:
- `page` (optional, default: 1)
- `limit` (optional, default: 20)
- `status` (optional, filter by status: draft, review, approved, published)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "reports": [
      {
        "id": "uuid",
        "title": "Annual Sustainability Report 2023",
        "description": "ESRS compliance report",
        "fileId": "uuid",
        "taxonomyId": "uuid",
        "status": "draft",
        "createdById": "uuid",
        "createdByName": "John Doe",
        "createdAt": "2025-11-01T00:00:00Z",
        "updatedAt": "2025-11-03T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 15,
      "totalPages": 1
    }
  }
}
```

---

### POST `/reports`

Create a new report.

**Request Body**:
```json
{
  "title": "Q4 2023 Sustainability Report",
  "description": "ESRS E1 Climate reporting",
  "fileId": "uuid",
  "taxonomyId": "uuid"
}
```

**Response**: `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Q4 2023 Sustainability Report",
    "description": "ESRS E1 Climate reporting",
    "fileId": "uuid",
    "taxonomyId": "uuid",
    "status": "draft",
    "workspaceId": "uuid",
    "createdById": "uuid",
    "createdAt": "2025-11-03T10:00:00Z"
  }
}
```

---

### GET `/reports/:id`

Get report details with tags and contexts.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Annual Sustainability Report 2023",
    "description": "ESRS compliance report",
    "file": {
      "id": "uuid",
      "filename": "report.pdf",
      "fileType": "pdf"
    },
    "taxonomy": {
      "id": "uuid",
      "name": "ESRS",
      "version": "1.0"
    },
    "status": "draft",
    "tagCount": 45,
    "contextCount": 3,
    "createdBy": {
      "id": "uuid",
      "firstName": "John",
      "lastName": "Doe"
    },
    "createdAt": "2025-11-01T00:00:00Z",
    "updatedAt": "2025-11-03T10:00:00Z"
  }
}
```

---

### PATCH `/reports/:id`

Update report.

**Request Body**:
```json
{
  "title": "Updated Title",
  "status": "review"
}
```

**Response**: `200 OK`

---

### DELETE `/reports/:id`

Soft delete report.

**Response**: `204 No Content`

---

## 9. Tags

### GET `/reports/:reportId/tags`

List all tags for a report.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "tags": [
      {
        "id": "uuid",
        "conceptId": "esrs_e1:ghgEmissions",
        "value": "12500",
        "unit": "tCO2e",
        "decimals": -3,
        "startIndex": 1250,
        "endIndex": 1280,
        "pageNumber": 5,
        "context": {
          "id": "uuid",
          "contextId": "ctx_2023_fy",
          "entityIdentifier": "12345678",
          "periodType": "duration",
          "startDate": "2023-01-01",
          "endDate": "2023-12-31"
        },
        "createdBy": {
          "id": "uuid",
          "firstName": "Jane",
          "lastName": "Smith"
        },
        "createdAt": "2025-11-02T15:30:00Z"
      }
    ]
  }
}
```

---

### POST `/reports/:reportId/tags`

Create a new tag.

**Request Body**:
```json
{
  "conceptId": "esrs_e1:ghgEmissions",
  "value": "12500",
  "unit": "tCO2e",
  "decimals": -3,
  "contextId": "uuid",
  "startIndex": 1250,
  "endIndex": 1280,
  "pageNumber": 5,
  "metadata": {
    "source": "ai_recommendation",
    "confidence": 0.95
  }
}
```

**Response**: `201 Created`

---

### PATCH `/tags/:id`

Update tag.

**Request Body**:
```json
{
  "value": "13000",
  "decimals": -2
}
```

**Response**: `200 OK`

---

### DELETE `/tags/:id`

Soft delete tag.

**Response**: `204 No Content`

---

## 10. Canvases

### GET `/reports/:reportId/canvas`

Get persisted canvas state.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "reportId": "uuid",
    "canvasData": {
      "blocks": [...],
      "tags": [...],
      "scrollPosition": 1500,
      "selectedContextId": "uuid",
      "version": "1.0"
    },
    "updatedAt": "2025-11-03T10:00:00Z"
  }
}
```

---

### POST `/reports/:reportId/canvas`

Save canvas state.

**Request Body**:
```json
{
  "canvasData": {
    "blocks": [...],
    "tags": [...],
    "scrollPosition": 1500,
    "selectedContextId": "uuid",
    "version": "1.0"
  }
}
```

**Response**: `200 OK`

---

## 11. XBRL Contexts

### GET `/reports/:reportId/contexts`

List all contexts for a report.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "contexts": [
      {
        "id": "uuid",
        "contextId": "ctx_2023_fy",
        "entityIdentifier": "12345678",
        "entityScheme": "http://www.esrs.eu",
        "periodType": "duration",
        "startDate": "2023-01-01",
        "endDate": "2023-12-31",
        "dimensions": {
          "esrs:BusinessSegment": "EU Operations"
        },
        "createdAt": "2025-11-01T00:00:00Z"
      }
    ]
  }
}
```

---

### POST `/reports/:reportId/contexts`

Create a new context.

**Request Body**:
```json
{
  "contextId": "ctx_2023_q4",
  "entityIdentifier": "12345678",
  "periodType": "duration",
  "startDate": "2023-10-01",
  "endDate": "2023-12-31",
  "dimensions": {
    "esrs:BusinessSegment": "EU Operations"
  }
}
```

**Response**: `201 Created`

---

### PATCH `/contexts/:id`

Update context.

**Response**: `200 OK`

---

### DELETE `/contexts/:id`

Delete context (only if no tags reference it).

**Response**: `204 No Content`

---

## 12. Taxonomies

### GET `/taxonomies`

List available taxonomies for current workspace.

**Headers**: `X-Workspace-Id: <workspace_id>`

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "taxonomies": [
      {
        "id": "uuid",
        "name": "ESRS",
        "version": "1.0",
        "taxonomyType": "esrs",
        "isActive": true,
        "isDefault": true,
        "metadata": {
          "namespace": "http://www.esrs.eu/xbrl/esrs",
          "conceptCount": 1250
        },
        "createdAt": "2025-01-01T00:00:00Z"
      }
    ]
  }
}
```

---

### POST `/taxonomies` (Admin only)

Upload new taxonomy file.

**Headers**: `Content-Type: multipart/form-data`

**Form Data**:
- `file` (ZIP file containing taxonomy)
- `name` (e.g., "ESRS")
- `version` (e.g., "1.0")
- `taxonomyType` (esrs, gri, sasb)

**Response**: `201 Created`

---

### POST `/workspaces/:workspaceId/taxonomies/:taxonomyId/assign`

Assign taxonomy to workspace (workspace_admin only).

**Request Body**:
```json
{
  "isDefault": true
}
```

**Response**: `200 OK`

---

### DELETE `/workspaces/:workspaceId/taxonomies/:taxonomyId/unassign`

Remove taxonomy from workspace.

**Response**: `204 No Content`

---

## 13. AI Recommendations

### POST `/ai/recommend-concepts`

Get AI-powered XBRL concept recommendations for selected text.

**Headers**: `X-Workspace-Id: <workspace_id>`

**Request Body**:
```json
{
  "reportId": "uuid",
  "selectedText": "Total greenhouse gas emissions in 2023 were 12,500 tonnes CO2 equivalent.",
  "taxonomyId": "uuid",
  "context": {
    "pageNumber": 5,
    "surroundingText": "... previous paragraph ... selected text ... next paragraph ..."
  }
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "conceptId": "esrs_e1:ghgEmissions",
        "conceptLabel": "GHG Emissions (Scope 1, 2, 3)",
        "confidence": 0.95,
        "suggestedValue": "12500",
        "suggestedUnit": "tCO2e",
        "suggestedDecimals": -3,
        "reasoning": "Text explicitly mentions greenhouse gas emissions with numeric value and unit."
      },
      {
        "conceptId": "esrs_e1:ghgEmissionsScope1",
        "conceptLabel": "GHG Emissions - Scope 1",
        "confidence": 0.72,
        "reasoning": "Could be Scope 1 emissions if context clarifies."
      }
    ],
    "suggestedContext": {
      "periodType": "duration",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31"
    }
  }
}
```

---

### POST `/ai/recommend-context`

Get AI-suggested XBRL context for a tag.

**Request Body**:
```json
{
  "reportId": "uuid",
  "conceptId": "esrs_e1:ghgEmissions",
  "value": "12500",
  "surroundingText": "... context text ..."
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "suggestedContext": {
      "periodType": "duration",
      "startDate": "2023-01-01",
      "endDate": "2023-12-31",
      "dimensions": {}
    },
    "confidence": 0.88,
    "reasoning": "Text references 'in 2023', suggesting annual reporting period."
  }
}
```

---

## 14. XBRL Export

### POST `/reports/:reportId/export/ixbrl`

Generate and download iXBRL document.

**Response**: `200 OK` (application/xml)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
      xmlns:esrs-e1="http://www.esrs.eu/xbrl/esrs/e1">
  <head>
    <title>Annual Sustainability Report 2023</title>
    <link:schemaRef xlink:type="simple"
                    xlink:href="http://www.esrs.eu/xbrl/esrs/esrs-e1.xsd"/>
  </head>
  <body>
    <ix:nonFraction contextRef="ctx_2023_fy"
                    name="esrs-e1:ghgEmissions"
                    unitRef="tCO2e"
                    decimals="-3">12,500</ix:nonFraction>
  </body>
</html>
```

**Headers**:
- `Content-Type: application/xml`
- `Content-Disposition: attachment; filename="report-ixbrl.xml"`

---

### POST `/reports/:reportId/validate`

Validate XBRL report against taxonomy.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "isValid": false,
    "errors": [
      {
        "severity": "error",
        "code": "MISSING_CONTEXT",
        "message": "Tag references undefined context 'ctx_invalid'",
        "tagId": "uuid"
      }
    ],
    "warnings": [
      {
        "severity": "warning",
        "code": "UNUSUAL_PRECISION",
        "message": "Decimals value -5 is unusual for this concept",
        "tagId": "uuid"
      }
    ]
  }
}
```

---

## 15. Report Locks

### POST `/reports/:reportId/lock`

Acquire edit lock on report.

**Headers**: `X-Workspace-Id: <workspace_id>`

**Request Body** (optional):
```json
{
  "clientInfo": {
    "userAgent": "Mozilla/5.0...",
    "ipAddress": "192.168.1.1"
  }
}
```

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "reportId": "uuid",
    "lockedById": "uuid",
    "lockedByName": "John Doe",
    "lockedAt": "2025-11-03T10:00:00Z",
    "expiresAt": "2025-11-03T10:15:00Z",
    "lastActivityAt": "2025-11-03T10:00:00Z"
  }
}
```

**Error**: `409 Conflict` (if already locked)
```json
{
  "success": false,
  "error": {
    "code": "REPORT_LOCKED",
    "message": "Report is currently being edited by another user",
    "lockedBy": {
      "id": "uuid",
      "firstName": "Jane",
      "lastName": "Smith"
    },
    "lockedAt": "2025-11-03T09:50:00Z",
    "expiresAt": "2025-11-03T10:05:00Z"
  },
  "statusCode": 409
}
```

---

### PUT `/reports/:reportId/lock/refresh`

Refresh lock (heartbeat to extend expiry).

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "expiresAt": "2025-11-03T10:16:00Z",
    "lastActivityAt": "2025-11-03T10:01:00Z"
  }
}
```

---

### DELETE `/reports/:reportId/lock`

Release lock.

**Response**: `204 No Content`

---

### GET `/reports/:reportId/lock`

Check lock status.

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "isLocked": true,
    "lock": {
      "id": "uuid",
      "lockedBy": {
        "id": "uuid",
        "firstName": "Jane",
        "lastName": "Smith"
      },
      "lockedAt": "2025-11-03T09:50:00Z",
      "expiresAt": "2025-11-03T10:05:00Z"
    }
  }
}
```

**Response** (if not locked): `200 OK`
```json
{
  "success": true,
  "data": {
    "isLocked": false,
    "lock": null
  }
}
```

---

### DELETE `/reports/:reportId/lock/force` (Admin only)

Force unlock report.

**Response**: `204 No Content`

---

## 16. Audit Logs

### GET `/audit-logs`

List audit logs for workspace.

**Headers**: `X-Workspace-Id: <workspace_id>`

**Query Parameters**:
- `page` (optional, default: 1)
- `limit` (optional, default: 50)
- `action` (optional, filter by action: CREATE, UPDATE, DELETE, etc.)
- `entityType` (optional, filter by entity: reports, tags, etc.)
- `userId` (optional, filter by user)
- `startDate` (optional, ISO 8601 date)
- `endDate` (optional, ISO 8601 date)

**Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "logs": [
      {
        "id": "uuid",
        "action": "UPDATE",
        "entityType": "tags",
        "entityId": "uuid",
        "user": {
          "id": "uuid",
          "firstName": "Jane",
          "lastName": "Smith"
        },
        "changes": {
          "old": {"value": "12500"},
          "new": {"value": "13000"}
        },
        "ipAddress": "192.168.1.1",
        "userAgent": "Mozilla/5.0...",
        "createdAt": "2025-11-03T10:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 50,
      "total": 234,
      "totalPages": 5
    }
  }
}
```

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request body or parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication token |
| `FORBIDDEN` | 403 | User lacks permission for this action |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict (e.g., duplicate, locked) |
| `REPORT_LOCKED` | 409 | Report is locked by another user |
| `FILE_TOO_LARGE` | 413 | Uploaded file exceeds 70MB limit |
| `UNSUPPORTED_FILE_TYPE` | 415 | File type not supported (only PDF/DOCX) |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected server error |
| `SERVICE_UNAVAILABLE` | 503 | External service (AI, storage) unavailable |

---

## Rate Limiting

- **Default**: 100 requests per minute per IP
- **AI Endpoints**: 10 requests per minute per workspace
- **File Upload**: 5 requests per minute per user

**Headers** (included in response):
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699000000
```

---

## Pagination

All list endpoints support pagination:

**Query Parameters**:
- `page` (default: 1)
- `limit` (default: 20, max: 100)

**Response Structure**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8,
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

---

## Filtering & Sorting

Many list endpoints support filtering and sorting:

**Query Parameters**:
- `sort` (e.g., `createdAt:desc`, `title:asc`)
- `filter[field]` (e.g., `filter[status]=draft`)

**Example**:
```
GET /api/v1/reports?sort=createdAt:desc&filter[status]=draft&page=1&limit=20
```

---

## Webhooks (Future Enhancement)

Not implemented in MVP. Planned for future releases:

- `report.created`
- `report.published`
- `tag.created`
- `export.completed`

---

**Last Updated**: 2025-11-03
**Version**: 1.0
**API Version**: v1
