import type { AxiosError } from "axios";

type ApiErrorData = {
    message: string;
    error?: { message: string; code: number };
};

export type AxiosErrorResponse = AxiosError<ApiErrorData>;

export type APIResponse<T> = {
    total: number;
    page: number;
    pages: number;
    limit: number;

}
export type BaseEntity = {
    id: string;
    created_at: string;
    updated_at: string;
};

export type Entity<T> = {
    [K in keyof T]: T[K];
} & BaseEntity;

export type User = Entity<{
    email: string;
    username: string;
    full_name: string;
    is_active: boolean;
    is_verified: boolean;
    role: string;
    company: string;
    platform_access: boolean;
    designation: string;
    status: string;
    last_login: string;
    last_accessed_at: string;
}>;
export type AuthResponse = {
    jwt: string;
    user: User;
};
export type UsersAPIResponse = APIResponse<User[]>;