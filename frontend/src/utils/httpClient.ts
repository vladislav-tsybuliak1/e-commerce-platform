export const HOST_URL = 'http://127.0.0.1:8000';
export const BASE_URL = `${HOST_URL}/api/v1`;

async function request<T>(
  url: string,
  method: string = 'GET',
  data?: unknown,
): Promise<T> {
  const options: RequestInit = {method};

  if (data !== undefined) {
    options.body = JSON.stringify(data);
    options.headers = {
      'Content-Type': 'application/json; charset=utf-8',
    };
  }

  const response = await fetch(BASE_URL + url, options);

  if (!response.ok) {
    throw new Error(`Failed to ${method} ${url}: ${response.status} ${response.statusText}`);
  }

  return response.status !== 204 ? response.json() : undefined as T;
}

export const client = {
  get: <T>(url: string) => request<T>(url),
  post: <T>(url: string, data: unknown) => request<T>(url, 'POST', data),
  put: <T>(url: string, data: unknown) => request<T>(url, 'PUT', data),
  delete: <T>(url: string) => request<T>(url, 'DELETE'),
};
