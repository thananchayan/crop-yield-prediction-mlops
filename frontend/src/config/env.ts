const parseTimeout = (value: string | undefined): number => {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 15000;
};

export const env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? "",
  requestTimeoutMs: parseTimeout(import.meta.env.VITE_REQUEST_TIMEOUT_MS),
};
