import { useQuery, UseQueryOptions } from '@tanstack/react-query';
import {Prediction, Price, Production} from "@/lib/models";
import {AxiosError} from "axios";
import {getPredictions, getPrice, getProduction} from "@/lib/api";

export const PRICE_KEY = 'price';

export const usePrice = (opts?: UseQueryOptions<Price[], AxiosError, Price[], [typeof PRICE_KEY]>) => {
  return useQuery({
      queryKey: [PRICE_KEY],
      queryFn: getPrice,
      ...opts,
    },
  );
};

export const useBikeStations = (opts?: UseQueryOptions<BikeStation[], AxiosError, BikeStation[], [typeof BIKE_STATIONS_KEY]>) => {
  return useQuery({
      queryKey: [BIKE_STATIONS_KEY],
      queryFn: getBikeStations,
      ...opts,
    },
  );
};

export const PRODUCTION_KEY = 'production';

export const useProduction = (production_type: string, opts?: Omit<UseQueryOptions<Production[], AxiosError, Production[], [typeof PRODUCTION_KEY, string]>, 'queryKey'>) => {
    return useQuery({
        queryKey: [PRODUCTION_KEY, production_type],
        queryFn: () => getProduction(production_type),
        ...opts,
        },
    );
};


export const PREDICTIONS_KEY = 'predictions';

export const usePredictions = (model_type: string, number: number, opts?: Omit<UseQueryOptions<Prediction[], AxiosError, Prediction[], (typeof PREDICTIONS_KEY | number)[]>, 'queryKey'>) => {
    return useQuery({
        queryKey: [PREDICTIONS_KEY, model_type, number],
        queryFn: () => getPredictions(model_type, number),
        ...opts,
        },
    );
};
