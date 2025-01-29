const BASE_URL = 'http://127.0.0.1:8000/api/v1';

export async function getData<T>(url: string): Promise<T> {
  return fetch(BASE_URL + url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`${response.status} ${response.statusText}`)
      }
      return response.json();
    })
}