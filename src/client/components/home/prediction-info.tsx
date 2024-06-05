'use client';
import React, {FC} from 'react';
import {usePredictions} from "@/lib/hooks/prediction-service";
import {DataTable} from "@/components/ui/data-table";
import {
    mapTableDataForPrediction,
    prepareDataAndLabelsForChart,
    prepareDataAndLabelsForPredictionChart
} from "@/utils/utils";
import LineChart from "@/components/ui/line-chart";

const columns = [
  {
    accessorKey: 'date',
    header: 'Time',
  },
  {
    accessorKey: 'value',
    header: 'Prediction',
  },
];

interface PredictionInfoProps {
    modelType: string,
    number: number
}

const PredictionInfo: FC<PredictionInfoProps> = ({ modelType, number }) => {
    const { data: prediction, isLoading, isError } = usePredictions(modelType, number);

    console.log(!isLoading && mapTableDataForPrediction(prediction));

    return (
        <div>
            <h1>Prediction Info</h1>
            <div>
                {isLoading ? <p>Loading...</p> :
                    <DataTable columns={columns} data={mapTableDataForPrediction(prediction)}/>}
            </div>
            <div className={'mt-5'}>
                {isLoading ? <p>Loading...</p> : <LineChart chart_data={prepareDataAndLabelsForPredictionChart(prediction)}/>}
            </div>
        </div>
    );
};

export default PredictionInfo;