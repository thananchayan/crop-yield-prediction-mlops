import type {
  FieldErrors,
  PredictionFormValues,
  PredictionRequest,
} from "../types/prediction";

const toNumber = (value: string): number => Number(value.trim());

const requiredText = (
  value: string,
  fieldName: string,
  maxLength = 100,
): string | undefined => {
  const trimmed = value.trim();
  if (!trimmed) {
    return `${fieldName} is required.`;
  }
  if (trimmed.length > maxLength) {
    return `${fieldName} must be ${maxLength} characters or fewer.`;
  }
  return undefined;
};

const numberInRange = (
  value: string,
  fieldName: string,
  min: number,
  max: number,
): string | undefined => {
  if (!value.trim()) {
    return `${fieldName} is required.`;
  }

  const parsed = toNumber(value);
  if (!Number.isFinite(parsed)) {
    return `${fieldName} must be a valid number.`;
  }
  if (parsed < min || parsed > max) {
    return `${fieldName} must be between ${min} and ${max}.`;
  }

  return undefined;
};

export const validatePredictionForm = (
  values: PredictionFormValues,
): FieldErrors => {
  const errors: FieldErrors = {};

  errors.area = requiredText(values.area, "Area");
  errors.item = requiredText(values.item, "Crop");
  errors.year = numberInRange(values.year, "Year", 1900, 2100);
  errors.averageRainFallMmPerYear = numberInRange(
    values.averageRainFallMmPerYear,
    "Average rainfall",
    0,
    10000,
  );
  errors.pesticidesTonnes = numberInRange(
    values.pesticidesTonnes,
    "Pesticides",
    0,
    10000000,
  );
  errors.avgTemp = numberInRange(values.avgTemp, "Average temperature", -50, 60);

  return Object.fromEntries(
    Object.entries(errors).filter(([, value]) => Boolean(value)),
  ) as FieldErrors;
};

export const hasValidationErrors = (errors: FieldErrors): boolean =>
  Object.keys(errors).length > 0;

export const toPredictionRequest = (
  values: PredictionFormValues,
): PredictionRequest => ({
  area: values.area.trim(),
  item: values.item.trim(),
  year: toNumber(values.year),
  average_rain_fall_mm_per_year: toNumber(values.averageRainFallMmPerYear),
  pesticides_tonnes: toNumber(values.pesticidesTonnes),
  avg_temp: toNumber(values.avgTemp),
});
