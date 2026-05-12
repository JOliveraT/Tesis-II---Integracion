const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function getToken() {
  return localStorage.getItem('auth_token') || '';
}

async function request(path, options = {}) {
  const token = getToken();
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {})
    },
    ...options
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || data.message || 'API error');
  return data;
}

export const apiClient = {
  get: (path) => request(path),
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) })
};
