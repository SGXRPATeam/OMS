const BASE_URL =
  "http://127.0.0.1:8000";

export async function apiFetch(
  endpoint: string,
  options: RequestInit = {}
) {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("token")
      : null;

  const activeTenant =
    typeof window !== "undefined"
      ? JSON.parse(
          localStorage.getItem(
            "activeTenant"
          ) || "null"
        )
      : null;

  const response = await fetch(
    `${BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type":
          "application/json",

        ...(token && {
          Authorization: `Bearer ${token}`,
        }),

        ...(activeTenant && {
          "X-Tenant-ID":
            activeTenant.tenantid,
        }),

        ...(options.headers || {}),
      },
    }
  );

  if (!response.ok) {
    throw new Error("API failed");
  }

  return response.json();
}