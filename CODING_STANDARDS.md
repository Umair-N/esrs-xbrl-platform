# CODING STANDARDS

Comprehensive coding standards and best practices for ESRS XBRL Platform (NestJS backend + Next.js frontend).

---

## General Principles

1. **Clean Code**: Write self-documenting code with clear naming
2. **DRY (Don't Repeat Yourself)**: Extract reusable logic into functions/modules
3. **SOLID Principles**: Follow object-oriented design principles
4. **Type Safety**: Use TypeScript strictly, avoid `any`
5. **Testing**: Write tests for critical business logic
6. **Documentation**: Document complex logic and public APIs

---

## TypeScript Standards

### 1. Type Annotations

**Always use explicit types** for function parameters and return values:

```typescript
// ✅ Good
function calculateTotal(price: number, quantity: number): number {
  return price * quantity;
}

// ❌ Bad
function calculateTotal(price, quantity) {
  return price * quantity;
}
```

---

### 2. Avoid `any`

**Never use `any`**. Use `unknown` if type is truly unknown, or create proper interfaces:

```typescript
// ✅ Good
interface ApiResponse {
  data: unknown;
  status: number;
}

function processResponse(response: ApiResponse): void {
  if (typeof response.data === 'string') {
    console.log(response.data.toUpperCase());
  }
}

// ❌ Bad
function processResponse(response: any): void {
  console.log(response.data.toUpperCase());
}
```

---

### 3. Use Enums for Constants

```typescript
// ✅ Good
enum ReportStatus {
  DRAFT = 'draft',
  REVIEW = 'review',
  APPROVED = 'approved',
  PUBLISHED = 'published',
}

// ❌ Bad
const STATUS_DRAFT = 'draft';
const STATUS_REVIEW = 'review';
```

---

### 4. Use Interfaces for Object Shapes

```typescript
// ✅ Good
interface CreateReportDto {
  title: string;
  description?: string;
  fileId: string;
  taxonomyId: string;
}

// ❌ Bad
type CreateReportDto = {
  title: string;
  description?: string;
  fileId: string;
  taxonomyId: string;
};
```

**When to use `type` vs `interface`**:
- Use `interface` for object shapes (DTOs, entities)
- Use `type` for unions, intersections, and primitives

---

## NestJS Backend Standards

### 1. Project Structure

```
backend/
├── src/
│   ├── common/              # Shared utilities, guards, decorators
│   │   ├── decorators/
│   │   ├── guards/
│   │   ├── interceptors/
│   │   ├── middleware/
│   │   └── utils/
│   ├── database/            # Database configuration, migrations
│   │   ├── migrations/
│   │   └── data-source.ts
│   ├── modules/             # Feature modules
│   │   ├── auth/
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── auth.module.ts
│   │   │   ├── dto/
│   │   │   ├── entities/
│   │   │   └── guards/
│   │   ├── reports/
│   │   ├── tags/
│   │   └── ...
│   ├── config/              # Configuration files
│   │   └── configuration.ts
│   ├── app.module.ts
│   └── main.ts
├── test/
├── package.json
└── tsconfig.json
```

---

### 2. Module Pattern

Each feature module should follow this structure:

```typescript
// reports/reports.module.ts
@Module({
  imports: [TypeOrmModule.forFeature([Report, Tag])],
  controllers: [ReportsController],
  providers: [ReportsService, ReportsRepository],
  exports: [ReportsService], // Export if used by other modules
})
export class ReportsModule {}
```

---

### 3. Controller Layer

**Controllers handle HTTP requests only**. No business logic.

```typescript
// reports/reports.controller.ts
@Controller('reports')
@UseGuards(JwtAuthGuard, WorkspaceGuard)
@ApiTags('reports')
export class ReportsController {
  constructor(private readonly reportsService: ReportsService) {}

  @Get()
  @ApiOperation({ summary: 'List all reports in workspace' })
  @ApiResponse({ status: 200, type: [ReportResponseDto] })
  async findAll(
    @WorkspaceId() workspaceId: string,
    @Query() query: PaginationDto,
  ): Promise<PaginatedResponse<ReportResponseDto>> {
    return this.reportsService.findAll(workspaceId, query);
  }

  @Post()
  @ApiOperation({ summary: 'Create a new report' })
  @ApiResponse({ status: 201, type: ReportResponseDto })
  async create(
    @WorkspaceId() workspaceId: string,
    @CurrentUser() user: User,
    @Body() dto: CreateReportDto,
  ): Promise<ReportResponseDto> {
    return this.reportsService.create(workspaceId, user.id, dto);
  }

  @Get(':id')
  async findOne(
    @WorkspaceId() workspaceId: string,
    @Param('id', ParseUUIDPipe) id: string,
  ): Promise<ReportResponseDto> {
    return this.reportsService.findOne(workspaceId, id);
  }

  @Patch(':id')
  async update(
    @WorkspaceId() workspaceId: string,
    @Param('id', ParseUUIDPipe) id: string,
    @Body() dto: UpdateReportDto,
  ): Promise<ReportResponseDto> {
    return this.reportsService.update(workspaceId, id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  async remove(
    @WorkspaceId() workspaceId: string,
    @Param('id', ParseUUIDPipe) id: string,
  ): Promise<void> {
    await this.reportsService.remove(workspaceId, id);
  }
}
```

**Key Patterns**:
- Use decorators for validation (`@Body()`, `@Param()`, `@Query()`)
- Use custom decorators for common data (`@WorkspaceId()`, `@CurrentUser()`)
- Use `ParseUUIDPipe` for UUID validation
- Document with Swagger decorators (`@ApiOperation`, `@ApiResponse`)
- Return DTOs, not entities

---

### 4. Service Layer

**Services contain business logic**. They orchestrate repository calls, external APIs, and validation.

```typescript
// reports/reports.service.ts
@Injectable()
export class ReportsService {
  constructor(
    private readonly reportsRepository: ReportsRepository,
    private readonly filesService: FilesService,
    private readonly auditService: AuditService,
  ) {}

  async findAll(
    workspaceId: string,
    query: PaginationDto,
  ): Promise<PaginatedResponse<ReportResponseDto>> {
    const [reports, total] = await this.reportsRepository.findAndCount({
      where: { workspaceId },
      take: query.limit,
      skip: (query.page - 1) * query.limit,
      order: { createdAt: 'DESC' },
      relations: ['file', 'taxonomy', 'createdBy'],
    });

    return {
      data: reports.map((report) => this.mapToDto(report)),
      pagination: {
        page: query.page,
        limit: query.limit,
        total,
        totalPages: Math.ceil(total / query.limit),
      },
    };
  }

  async create(
    workspaceId: string,
    userId: string,
    dto: CreateReportDto,
  ): Promise<ReportResponseDto> {
    // Validate file exists and belongs to workspace
    const file = await this.filesService.findOne(workspaceId, dto.fileId);
    if (!file) {
      throw new NotFoundException('File not found');
    }

    // Create report
    const report = this.reportsRepository.create({
      ...dto,
      workspaceId,
      createdById: userId,
      status: ReportStatus.DRAFT,
    });

    const savedReport = await this.reportsRepository.save(report);

    // Audit log
    await this.auditService.log({
      workspaceId,
      userId,
      action: 'CREATE',
      entityType: 'reports',
      entityId: savedReport.id,
    });

    return this.mapToDto(savedReport);
  }

  async update(
    workspaceId: string,
    id: string,
    dto: UpdateReportDto,
  ): Promise<ReportResponseDto> {
    const report = await this.reportsRepository.findOne({
      where: { id, workspaceId },
    });

    if (!report) {
      throw new NotFoundException('Report not found');
    }

    const oldValues = { ...report };

    Object.assign(report, dto);
    report.updatedAt = new Date();

    const updatedReport = await this.reportsRepository.save(report);

    // Audit log with changes
    await this.auditService.log({
      workspaceId,
      action: 'UPDATE',
      entityType: 'reports',
      entityId: id,
      changes: {
        old: oldValues,
        new: updatedReport,
      },
    });

    return this.mapToDto(updatedReport);
  }

  private mapToDto(report: Report): ReportResponseDto {
    return {
      id: report.id,
      title: report.title,
      description: report.description,
      status: report.status,
      file: report.file ? { id: report.file.id, filename: report.file.filename } : null,
      createdBy: report.createdBy
        ? {
            id: report.createdBy.id,
            firstName: report.createdBy.firstName,
            lastName: report.createdBy.lastName,
          }
        : null,
      createdAt: report.createdAt,
      updatedAt: report.updatedAt,
    };
  }
}
```

**Key Patterns**:
- Inject repositories and other services via constructor
- Validate input and check permissions
- Use transactions for multi-step operations
- Log audit trail for important actions
- Return DTOs via `mapToDto()` helper
- Throw standard exceptions (`NotFoundException`, `BadRequestException`, etc.)

---

### 5. Repository Pattern (TypeORM)

**Use TypeORM repositories** for database access:

```typescript
// reports/reports.repository.ts
@Injectable()
export class ReportsRepository extends Repository<Report> {
  constructor(private dataSource: DataSource) {
    super(Report, dataSource.createEntityManager());
  }

  async findByWorkspaceWithTags(workspaceId: string): Promise<Report[]> {
    return this.createQueryBuilder('report')
      .leftJoinAndSelect('report.tags', 'tags')
      .where('report.workspaceId = :workspaceId', { workspaceId })
      .andWhere('report.deletedAt IS NULL')
      .orderBy('report.createdAt', 'DESC')
      .getMany();
  }

  async countByStatus(workspaceId: string, status: ReportStatus): Promise<number> {
    return this.count({
      where: { workspaceId, status, deletedAt: IsNull() },
    });
  }
}
```

**Key Patterns**:
- Extend `Repository<Entity>`
- Use query builder for complex queries
- Filter soft-deleted records (`deletedAt IS NULL`)
- Use parameterized queries to prevent SQL injection

---

### 6. Entity Definitions

**Entities map to database tables**:

```typescript
// reports/entities/report.entity.ts
@Entity('reports')
export class Report {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ name: 'workspace_id', type: 'uuid' })
  @Index()
  workspaceId: string;

  @ManyToOne(() => Workspace, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'workspace_id' })
  workspace: Workspace;

  @Column({ name: 'file_id', type: 'uuid', nullable: true })
  fileId: string;

  @ManyToOne(() => File, { onDelete: 'SET NULL' })
  @JoinColumn({ name: 'file_id' })
  file: File;

  @Column({ name: 'created_by_id', type: 'uuid' })
  createdById: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'created_by_id' })
  createdBy: User;

  @Column({ length: 255 })
  title: string;

  @Column({ type: 'text', nullable: true })
  description: string;

  @Column({
    type: 'enum',
    enum: ReportStatus,
    default: ReportStatus.DRAFT,
  })
  status: ReportStatus;

  @Column({ type: 'jsonb', default: {} })
  metadata: Record<string, any>;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;

  @DeleteDateColumn({ name: 'deleted_at' })
  deletedAt: Date;

  @OneToMany(() => Tag, (tag) => tag.report)
  tags: Tag[];

  @OneToOne(() => Canvas, (canvas) => canvas.report)
  canvas: Canvas;
}
```

**Key Patterns**:
- Use `@Entity('table_name')` decorator
- Use snake_case for column names (`name: 'created_at'`)
- Use `@Index()` for frequently queried columns
- Define relationships (`@ManyToOne`, `@OneToMany`, etc.)
- Use `@DeleteDateColumn` for soft deletes
- Use `@CreateDateColumn` and `@UpdateDateColumn` for timestamps
- Use `@Column({ type: 'jsonb' })` for flexible metadata

---

### 7. DTOs (Data Transfer Objects)

**DTOs define request/response shapes**:

```typescript
// reports/dto/create-report.dto.ts
export class CreateReportDto {
  @ApiProperty({ example: 'Annual Sustainability Report 2023' })
  @IsString()
  @IsNotEmpty()
  @MaxLength(255)
  title: string;

  @ApiProperty({ example: 'ESRS compliance report', required: false })
  @IsString()
  @IsOptional()
  description?: string;

  @ApiProperty({ example: 'uuid' })
  @IsUUID()
  fileId: string;

  @ApiProperty({ example: 'uuid' })
  @IsUUID()
  taxonomyId: string;
}

// reports/dto/update-report.dto.ts
export class UpdateReportDto extends PartialType(CreateReportDto) {
  @ApiProperty({ enum: ReportStatus, required: false })
  @IsEnum(ReportStatus)
  @IsOptional()
  status?: ReportStatus;
}

// reports/dto/report-response.dto.ts
export class ReportResponseDto {
  @ApiProperty()
  id: string;

  @ApiProperty()
  title: string;

  @ApiProperty({ required: false })
  description?: string;

  @ApiProperty({ enum: ReportStatus })
  status: ReportStatus;

  @ApiProperty({ type: () => FileResponseDto, required: false })
  file?: FileResponseDto;

  @ApiProperty({ type: () => UserResponseDto, required: false })
  createdBy?: UserResponseDto;

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;
}
```

**Key Patterns**:
- Use class-validator decorators (`@IsString()`, `@IsUUID()`, etc.)
- Use Swagger decorators (`@ApiProperty()`)
- Extend `PartialType()` for update DTOs
- Separate request DTOs from response DTOs
- Never expose entities directly in responses

---

### 8. Custom Decorators

```typescript
// common/decorators/workspace-id.decorator.ts
export const WorkspaceId = createParamDecorator(
  (data: unknown, ctx: ExecutionContext): string => {
    const request = ctx.switchToHttp().getRequest();
    return request.headers['x-workspace-id'] || request.user?.currentWorkspaceId;
  },
);

// common/decorators/current-user.decorator.ts
export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext): User => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
```

**Usage**:
```typescript
@Get()
async findAll(
  @WorkspaceId() workspaceId: string,
  @CurrentUser() user: User,
): Promise<Report[]> {
  // ...
}
```

---

### 9. Guards

```typescript
// common/guards/jwt-auth.guard.ts
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  canActivate(context: ExecutionContext) {
    return super.canActivate(context);
  }

  handleRequest(err, user, info) {
    if (err || !user) {
      throw new UnauthorizedException('Invalid token');
    }
    return user;
  }
}

// common/guards/workspace.guard.ts
@Injectable()
export class WorkspaceGuard implements CanActivate {
  constructor(private readonly workspaceService: WorkspaceService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const workspaceId = request.headers['x-workspace-id'];
    const user = request.user;

    if (!workspaceId) {
      throw new BadRequestException('Workspace ID is required');
    }

    const hasAccess = await this.workspaceService.userHasAccess(
      user.id,
      workspaceId,
    );

    if (!hasAccess) {
      throw new ForbiddenException('Access denied to this workspace');
    }

    // Set PostgreSQL session variable for RLS
    await this.dataSource.query('SET app.current_workspace_id = $1', [workspaceId]);

    return true;
  }
}
```

---

### 10. Middleware

```typescript
// common/middleware/workspace.middleware.ts
@Injectable()
export class WorkspaceMiddleware implements NestMiddleware {
  constructor(private dataSource: DataSource) {}

  async use(req: Request, res: Response, next: NextFunction) {
    const workspaceId = req.headers['x-workspace-id'];

    if (workspaceId) {
      // Set PostgreSQL session variable for RLS
      await this.dataSource.query('SET app.current_workspace_id = $1', [workspaceId]);
    }

    next();
  }
}
```

**Register in module**:
```typescript
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(WorkspaceMiddleware).forRoutes('*');
  }
}
```

---

### 11. Exception Handling

**Use built-in NestJS exceptions**:

```typescript
import {
  BadRequestException,
  NotFoundException,
  UnauthorizedException,
  ForbiddenException,
  ConflictException,
  InternalServerErrorException,
} from '@nestjs/common';

// Usage
throw new NotFoundException('Report not found');
throw new ConflictException('Report is locked by another user');
throw new BadRequestException('Invalid file format');
```

**Custom exception filter**:
```typescript
// common/filters/http-exception.filter.ts
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse();

    response.status(status).json({
      success: false,
      error: {
        code: exception.name,
        message: exception.message,
        details: typeof exceptionResponse === 'object' ? exceptionResponse : null,
      },
      statusCode: status,
      timestamp: new Date().toISOString(),
    });
  }
}
```

---

### 12. Testing

**Unit tests** (services):

```typescript
// reports/reports.service.spec.ts
describe('ReportsService', () => {
  let service: ReportsService;
  let repository: MockType<ReportsRepository>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ReportsService,
        {
          provide: ReportsRepository,
          useFactory: repositoryMockFactory,
        },
      ],
    }).compile();

    service = module.get<ReportsService>(ReportsService);
    repository = module.get(ReportsRepository);
  });

  it('should create a report', async () => {
    const dto: CreateReportDto = {
      title: 'Test Report',
      fileId: 'uuid',
      taxonomyId: 'uuid',
    };

    repository.create.mockReturnValue(dto);
    repository.save.mockResolvedValue({ id: 'uuid', ...dto });

    const result = await service.create('workspace-id', 'user-id', dto);

    expect(result.title).toBe('Test Report');
    expect(repository.save).toHaveBeenCalled();
  });
});
```

**E2E tests** (endpoints):

```typescript
// test/reports.e2e-spec.ts
describe('ReportsController (e2e)', () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();

    // Login to get auth token
    const response = await request(app.getHttpServer())
      .post('/auth/login')
      .send({ email: 'test@example.com', password: 'password' });

    authToken = response.body.data.accessToken;
  });

  it('/reports (POST)', async () => {
    return request(app.getHttpServer())
      .post('/reports')
      .set('Authorization', `Bearer ${authToken}`)
      .set('X-Workspace-Id', 'workspace-id')
      .send({
        title: 'Test Report',
        fileId: 'file-uuid',
        taxonomyId: 'taxonomy-uuid',
      })
      .expect(201)
      .expect((res) => {
        expect(res.body.data.title).toBe('Test Report');
      });
  });
});
```

---

## Next.js Frontend Standards

### 1. Project Structure

```
app/
├── (auth)/                  # Auth routes group
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── (main)/                  # Main app routes
│   ├── (platform)/
│   │   ├── reports/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   └── layout.tsx
│   └── layout.tsx
├── api/                     # API routes (if needed)
├── layout.tsx
└── page.tsx

components/
├── ui/                      # Radix UI components
│   ├── button.tsx
│   ├── dialog.tsx
│   └── ...
├── editor/                  # Editor-specific components
│   ├── pdf-editor.tsx
│   ├── tagging-panel.tsx
│   └── ...
└── shared/                  # Shared components
    ├── header.tsx
    └── sidebar.tsx

lib/
├── api-client.ts            # Axios configuration
├── utils.ts                 # Utility functions
└── types.ts                 # Shared types

store/
├── tagging-store.ts         # Zustand stores
└── taxonomy-store.ts

features/
├── reports/                 # Feature-based organization
│   ├── hooks/
│   │   ├── useReports.ts
│   │   └── useReportLock.ts
│   └── api/
│       └── reports-api.ts
└── tags/
    └── ...
```

---

### 2. Component Patterns

**Server Components (default)**:

```typescript
// app/(main)/(platform)/reports/page.tsx
import { Suspense } from 'react';
import { ReportsList } from '@/features/reports/components/reports-list';
import { ReportsLoading } from '@/features/reports/components/reports-loading';

export default async function ReportsPage() {
  return (
    <div className="container py-8">
      <h1 className="text-3xl font-bold mb-6">Reports</h1>
      <Suspense fallback={<ReportsLoading />}>
        <ReportsList />
      </Suspense>
    </div>
  );
}
```

**Client Components** (when needed):

```typescript
// components/editor/tagging-panel.tsx
'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTaxonomyStore } from '@/store/taxonomy-store';

export function TaggingPanel({ reportId }: { reportId: string }) {
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null);
  const { taxonomy } = useTaxonomyStore();

  const { data: concepts, isLoading } = useQuery({
    queryKey: ['concepts', taxonomy?.id],
    queryFn: () => fetchConcepts(taxonomy?.id),
    enabled: !!taxonomy?.id,
  });

  if (isLoading) {
    return <div>Loading concepts...</div>;
  }

  return (
    <div className="p-4">
      {/* Component UI */}
    </div>
  );
}
```

**Key Patterns**:
- Use Server Components by default
- Only use `'use client'` when needed (state, effects, event handlers)
- Use `Suspense` for loading states
- Use React Query for data fetching in client components

---

### 3. React Query Hooks

```typescript
// features/reports/hooks/useReports.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { reportsApi } from '../api/reports-api';

export function useReports(workspaceId: string) {
  return useQuery({
    queryKey: ['reports', workspaceId],
    queryFn: () => reportsApi.findAll(workspaceId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useReport(workspaceId: string, reportId: string) {
  return useQuery({
    queryKey: ['reports', workspaceId, reportId],
    queryFn: () => reportsApi.findOne(workspaceId, reportId),
  });
}

export function useCreateReport(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateReportDto) => reportsApi.create(workspaceId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports', workspaceId] });
    },
  });
}

export function useUpdateReport(workspaceId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateReportDto }) =>
      reportsApi.update(workspaceId, id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['reports', workspaceId] });
      queryClient.invalidateQueries({ queryKey: ['reports', workspaceId, variables.id] });
    },
  });
}
```

---

### 4. Zustand Store

```typescript
// store/tagging-store.ts
import { create } from 'zustand';

interface ConceptSelection {
  conceptId: string;
  value: string;
  unit?: string;
  decimals?: number;
  confidence?: number;
}

interface TaggingStore {
  pendingConcept: ConceptSelection | null;
  selectedContextId: string | null;
  feedbackId: string | null;

  setPendingConcept: (concept: ConceptSelection | null) => void;
  setSelectedContextId: (contextId: string | null) => void;
  setFeedbackId: (feedbackId: string | null) => void;
  reset: () => void;
}

export const useTaggingStore = create<TaggingStore>((set) => ({
  pendingConcept: null,
  selectedContextId: null,
  feedbackId: null,

  setPendingConcept: (concept) => set({ pendingConcept: concept }),
  setSelectedContextId: (contextId) => set({ selectedContextId: contextId }),
  setFeedbackId: (feedbackId) => set({ feedbackId }),
  reset: () => set({ pendingConcept: null, selectedContextId: null, feedbackId: null }),
}));
```

---

### 5. API Client

```typescript
// lib/api-client.ts
import axios, { AxiosError } from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true, // Send cookies
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (add workspace ID)
apiClient.interceptors.request.use((config) => {
  const workspaceId = localStorage.getItem('currentWorkspaceId');
  if (workspaceId) {
    config.headers['X-Workspace-Id'] = workspaceId;
  }
  return config;
});

// Response interceptor (handle errors)
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Try to refresh token
      try {
        await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`, {}, {
          withCredentials: true,
        });
        // Retry original request
        return apiClient.request(error.config!);
      } catch {
        // Redirect to login
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  },
);

export default apiClient;
```

---

### 6. Form Validation

**Use React Hook Form + Zod**:

```typescript
// features/reports/components/create-report-form.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const createReportSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255),
  description: z.string().optional(),
  fileId: z.string().uuid('Invalid file ID'),
  taxonomyId: z.string().uuid('Invalid taxonomy ID'),
});

type CreateReportFormData = z.infer<typeof createReportSchema>;

export function CreateReportForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<CreateReportFormData>({
    resolver: zodResolver(createReportSchema),
  });

  const createReport = useCreateReport(workspaceId);

  const onSubmit = async (data: CreateReportFormData) => {
    await createReport.mutateAsync(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="title">Title</label>
        <input {...register('title')} />
        {errors.title && <span>{errors.title.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create Report'}
      </button>
    </form>
  );
}
```

---

### 7. Styling (TailwindCSS)

```typescript
// components/ui/button.tsx
import { cn } from '@/lib/utils';
import { VariantProps, cva } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent',
        ghost: 'hover:bg-accent',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ variant, size }), className)} {...props} />
  );
}
```

**Usage**:
```tsx
<Button variant="outline" size="sm">Click me</Button>
```

---

## Naming Conventions

### Files
- **Components**: `kebab-case.tsx` (e.g., `tagging-panel.tsx`)
- **Hooks**: `use-feature-name.ts` (e.g., `use-report-lock.ts`)
- **Utilities**: `kebab-case.ts` (e.g., `format-date.ts`)
- **Types**: `types.ts` or `feature.types.ts`

### Variables & Functions
- **camelCase** for variables and functions
- **PascalCase** for React components and classes
- **UPPER_SNAKE_CASE** for constants

```typescript
// ✅ Good
const userName = 'John';
function calculateTotal() {}
class ReportService {}
const MAX_FILE_SIZE = 70 * 1024 * 1024;

// ❌ Bad
const UserName = 'John';
function CalculateTotal() {}
const maxFileSize = 70 * 1024 * 1024;
```

---

## Git Commit Messages

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactor
- `docs`: Documentation changes
- `test`: Test additions/updates
- `chore`: Build/config changes

**Examples**:
```
feat(reports): Add file locking mechanism
fix(tags): Resolve duplicate tag creation issue
refactor(auth): Simplify JWT token refresh logic
docs(api): Update API endpoint documentation
test(reports): Add unit tests for ReportsService
chore(deps): Update TypeORM to v0.3.20
```

---

## Code Review Checklist

- [ ] Code follows TypeScript standards (no `any`, explicit types)
- [ ] DTOs have proper validation decorators
- [ ] Services contain business logic, controllers are thin
- [ ] Database queries use parameterized queries
- [ ] Audit logs created for important actions
- [ ] Errors handled with proper exception types
- [ ] Tests added for new features
- [ ] API documented with Swagger decorators
- [ ] Code is DRY (no duplication)
- [ ] Variable/function names are clear and descriptive

---

**Last Updated**: 2025-11-03
**Version**: 1.0
