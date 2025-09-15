import type { AxiosError } from "axios";

type ApiErrorData = {
    message: string;
    error?: { message: string; code: number };
};

export type AxiosErrorResponse = AxiosError<ApiErrorData>;

export type APIResponse<T, K extends string = "data"> = {
    total: number;
    page: number;
    pages: number;
    limit: number;
} & {
    [key in K]: T; // This allows dynamic property names like `users`, `clients`, etc.
};

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
    status: 'active' | 'inactive' | 'disabled' | 'pending';
    last_login: string;
    last_accessed_at: string;
}>;
export type UsersAPIResponse = APIResponse<User[], "users">;


export type AuthResponse = {
    jwt: string;
    user: User;
};
export type UserStats = {
    total: number;
    this_month: number;
    last_month: number;
    change_percentage: number;
    platform_access_true: number;
    platform_access_false: number;
    last_accessed_today: number;
    last_accessed_yesterday: number;
    access_change_percentage: number;

}

export type QueryRecommendationsBody = {
    query: string,
    taxonomy: string,
    k: number,
    rerank: boolean
}
export type QueryRecommendations = {
    query: string,
    taxonomy: string,
    results: {
        tag: string,
        datatype: string,
        reference: string,
        score: number,
        rank: number
    }[]
}

export type GenerateChatBot = {
    text: string
    session_id: string
}