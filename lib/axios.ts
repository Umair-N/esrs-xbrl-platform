import Axios, {
  AxiosError,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios';
function authRequestInterceptor(config: InternalAxiosRequestConfig) {
  if (config?.params) {
    Object.keys(config?.params).forEach((key) => {
      if (config?.params[key] === '') {
        delete config?.params[key];
      }
    });
  }
  if (config.headers) {
    config.headers.Accept = 'application/json';
  }

  config.withCredentials = true;
  return config;
}

export const axiosInstance = Axios.create({
  baseURL:
    `${process.env.NEXT_PUBLIC_API_URL}/api/v1` ||
    'https://api.briskbold.ai/api/v1',
});

axiosInstance.interceptors.request.use(authRequestInterceptor);

export interface AxiosErrorResponse extends AxiosResponse {
  error: AxiosError;
  response: {
    data: {
      message: string;
    };
  };
}
