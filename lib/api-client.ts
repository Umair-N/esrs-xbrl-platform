import { showError } from "@/components/heads-up";

type RequestOptions = {
    method?: string;
    headers?: Record<string, string>;
    body?: any;
    cookie?: string;
    params?: Record<string, string | number | boolean | undefined | null>;
    cache?: RequestCache;
    next?: NextFetchRequestConfig;
    serviceType?: 'coreBackend' | 'aiRecommender';  // Optional serviceType
};

const CONFIG = {
    coreBackend: {
        local: 'http://localhost:8000/api/v1',
        gcp: 'https://api.briskbold.ai/api/v1',
    },
    aiRecommender: {
        local: 'http://localhost:8090',
        gcp: 'https://ai-recommender.gcp.com',
    },
};

function buildUrlWithParams(
    url: string,
    params?: RequestOptions['params'],
): string {
    if (!params) return url;
    const filteredParams = Object.fromEntries(
        Object.entries(params).filter(
            ([, value]) => value !== undefined && value !== null,
        ),
    );
    if (Object.keys(filteredParams).length === 0) return url;
    const queryString = new URLSearchParams(
        filteredParams as Record<string, string>,
    ).toString();
    return `${url}?${queryString}`;
}

async function fetchApi<T>(
    url: string,
    options: RequestOptions = {},
): Promise<T> {
    const {
        method = 'GET',
        headers = {},
        body,
        cookie,
        params,
        cache = 'no-store',
        next,
        serviceType = 'coreBackend',  // Default to coreBackend if not provided
    } = options;

    // Automatically determine the environment
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    const env = isLocal ? 'local' : 'gcp';  // Set to local or gcp based on the hostname

    // Dynamically select base URL based on serviceType and env
    const baseUrls = CONFIG[serviceType];
    const API_URL = baseUrls[env];

    const fullUrl = buildUrlWithParams(`${API_URL}${url}`, params);

    const response = await fetch(fullUrl, {
        method,
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            ...headers,
            ...(cookie ? { Cookie: cookie } : {}),
        },
        body: body ? JSON.stringify(body) : undefined,
        credentials: 'include',
        cache,
        next,
    });

    if (!response.ok) {
        const message = (await response.json()).message || response.statusText;
        if (typeof window !== 'undefined') {
            showError({
                title: "Error!",
                message: message,
                duration: 2000,
            });
        }
        throw new Error(message);
    }

    return response.json();
}

export const api = {
    get<T>(url: string, options?: RequestOptions): Promise<T> {
        return fetchApi<T>(url, { ...options, method: 'GET' });
    },
    post<T>(url: string, body?: any, options?: RequestOptions): Promise<T> {
        return fetchApi<T>(url, { ...options, method: 'POST', body });
    },
    put<T>(url: string, body?: any, options?: RequestOptions): Promise<T> {
        return fetchApi<T>(url, { ...options, method: 'PUT', body });
    },
    patch<T>(url: string, body?: any, options?: RequestOptions): Promise<T> {
        return fetchApi<T>(url, { ...options, method: 'PATCH', body });
    },
    delete<T>(url: string, options?: RequestOptions): Promise<T> {
        return fetchApi<T>(url, { ...options, method: 'DELETE' });
    },
};
