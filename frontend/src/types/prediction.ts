export type PredictionFormValues = {
  area: string;
  item: string;
  year: string;
  averageRainFallMmPerYear: string;
  pesticidesTonnes: string;
  avgTemp: string;
};

export type PredictionRequest = {
  area: string;
  item: string;
  year: number;
  average_rain_fall_mm_per_year: number;
  pesticides_tonnes: number;
  avg_temp: number;
};

export type PredictionResponse = {
  success: true;
  request_id: string;
  prediction: number;
  unit: string;
  model_id: string;
  model_version: string;
};

export type ApiErrorResponse = {
  success: false;
  request_id?: string;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
};

export type FieldErrors = Partial<Record<keyof PredictionFormValues, string>>;
