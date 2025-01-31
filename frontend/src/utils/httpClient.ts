const BASE_URL = 'http://127.0.0.1:8000/api/v1';

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
  delete<T>(url: string): Promise<T> {
    return fetch(BASE_URL + url, {method: 'DELETE'})
      .then(handleResponse)
  },
};
