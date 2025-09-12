import { showError } from '@/components/heads-up';

type RequestOptions = {
  method?: string;
  headers?: Record<string, string>;
  body?: any;
  cookie?: string;
  params?: Record<string, string | number | boolean | undefined | null>;
  cache?: RequestCache;
  next?: NextFetchRequestConfig;
  serviceType?: 'coreBackend' | 'aiRecommender';
};

const CONFIG = {
  coreBackend: {
    local: 'http://localhost:8000/api/v1',
    gcp: 'https://api.briskbold.ai/api/v1',
  },
  aiRecommender: {
    local: 'https://xbrl-tag-171009084156.europe-west1.run.app/api/v1',
    gcp: 'https://xbrl-tag-171009084156.europe-west1.run.app/api/v1',
  },
};

function buildUrlWithParams(
  url: string,
  params?: RequestOptions['params']
): string {
  if (!params) return url;
  const filteredParams = Object.fromEntries(
    Object.entries(params).filter(
      ([, value]) => value !== undefined && value !== null
    )
  );
  if (Object.keys(filteredParams).length === 0) return url;
  const queryString = new URLSearchParams(
    filteredParams as Record<string, string>
  ).toString();
  return `${url}?${queryString}`;
}

function isFormDataBody(body: any): body is FormData {
  return typeof FormData !== 'undefined' && body instanceof FormData;
}
function isBinaryBody(body: any): body is Blob | ArrayBuffer | Uint8Array {
  return (
    body instanceof Blob ||
    body instanceof ArrayBuffer ||
    body instanceof Uint8Array
  );
}

async function fetchApi<T>(
  url: string,
  options: RequestOptions = {}
): Promise<T> {
  const {
    method = 'GET',
    headers = {},
    body,
    cookie,
    params,
    cache = 'no-store',
    next,
    serviceType = 'coreBackend',
  } = options;

  const isLocal =
    typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1');
  const env = isLocal ? 'local' : 'gcp';

  const baseUrls = CONFIG[serviceType];
  const API_URL = baseUrls[env];

  const fullUrl = buildUrlWithParams(`${API_URL}${url}`, params);

  // Decide how to send the body
  const sendingFormData = isFormDataBody(body);
  const sendingBinary = isBinaryBody(body);
  const shouldSendJson =
    body !== undefined &&
    body !== null &&
    !sendingFormData &&
    !sendingBinary &&
    typeof body !== 'string'; // strings are sent as-is

  const finalHeaders = new Headers({
    Accept: 'application/json',
    ...headers,
    ...(cookie ? { Cookie: cookie } : {}),
  });

  // Only set Content-Type for JSON. For FormData or binary, let the browser set it.
  if (shouldSendJson && !finalHeaders.has('Content-Type')) {
    finalHeaders.set('Content-Type', 'application/json');
  }
  if (sendingFormData || sendingBinary) {
    // Ensure we DO NOT force JSON content-type
    finalHeaders.delete('Content-Type');
  }

  const finalBody =
    body === undefined || body === null
      ? undefined
      : shouldSendJson
        ? JSON.stringify(body)
        : body; // FormData, Blob, ArrayBuffer, string pass through

  const response = await fetch(fullUrl, {
    method,
    headers: finalHeaders,
    body: method === 'GET' || method === 'HEAD' ? undefined : finalBody,
    credentials: 'include',
    cache,
    next,
  });

  // Handle non-OK with safer parsing (could be text/html or empty)
  if (!response.ok) {
    let message: string;
    try {
      const data = await response.json();
      message = (data && (data.message || data.detail)) || response.statusText;
    } catch {
      try {
        message = await response.text();
      } catch {
        message = response.statusText;
      }
    }
    if (typeof window !== 'undefined') {
      // showError({ title: 'Error!', message, duration: 2000 });
      throw new Error(message);
    }
    throw new Error(message);
  }

  // No content
  if (response.status === 204) return undefined as unknown as T;

  // Try JSON first, fall back to text
  const ct = response.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    return response.json() as Promise<T>;
  }
  const text = await response.text();
  // @ts-expect-error – caller expects T; if not JSON, return text
  return text;
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
