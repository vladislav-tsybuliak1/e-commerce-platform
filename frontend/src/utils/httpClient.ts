export const HOST_URL = 'http://127.0.0.1:8000';
export const BASE_URL = `${HOST_URL}/api/v1`;

const handleResponse = (response: Response) => {
    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}`)
    }
    return response.status !== 204 ? response.json() : undefined;
  }
;

export const client = {
  get<T>(url: string): Promise<T> {
    return fetch(BASE_URL + url)
      .then(handleResponse);
  },
  post<T, U = unknown>(url: string, data: U): Promise<T> {
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
      body: JSON.stringify(data)
    };
    return fetch(BASE_URL + url, options)
      .then(handleResponse);
  },
  delete<T>(url: string): Promise<T> {
    return fetch(BASE_URL + url, {method: 'DELETE'})
      .then(handleResponse)
  },
};
