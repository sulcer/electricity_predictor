import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import {AxiosError} from "axios";
import {getPredictions, getPrice, getProduction, getTrainingMetrics, getValidationMetrics} from "@/lib/api";

export const PRICE_KEY = 'price';

export const usePrice = (opts?: UseQueryOptions<any[], AxiosError, any[], [typeof PRICE_KEY]>) => {
  return useQuery({
      queryKey: [PRICE_KEY],
      queryFn: getPrice,
      ...opts,
    },
  );
};

export const PRODUCTION_KEY = 'production';

export const useProduction = (production_type: string, opts?: Omit<UseQueryOptions<any[], AxiosError, any[], [typeof PRODUCTION_KEY, string]>, 'queryKey'>) => {
    return useQuery({
        queryKey: [PRODUCTION_KEY, production_type],
        queryFn: () => getProduction(production_type),
        ...opts,
        },
    );
};


export const PREDICTIONS_KEY = 'predictions';

export const usePredictions = (model_type: string, number: number, opts?: Omit<UseQueryOptions<any[], AxiosError, any[], (string | number)[]>, 'queryKey'>) => {
    return useQuery({
        queryKey: [PREDICTIONS_KEY, `${model_type}_${number}`],
        queryFn: () => getPredictions(model_type, number),
        ...opts || {},
    });
};

export const TRAIN_METRICS_KEY = 'train_metrics';

export const useTrainingMetrics = (opts?: UseQueryOptions<any[], AxiosError, any[], [typeof TRAIN_METRICS_KEY]>) => {
    return useQuery({
        queryKey: [TRAIN_METRICS_KEY],
        queryFn: getTrainingMetrics,
        ...opts,
    });
};

export const VALIDATION_METRICS_KEY = 'validation_metrics';

export const useValidationMetrics = (opts?: UseQueryOptions<any[], AxiosError, any[], [typeof VALIDATION_METRICS_KEY]>) => {
    return useQuery({
        queryKey: [VALIDATION_METRICS_KEY],
        queryFn: getValidationMetrics,
        ...opts,
    });
};