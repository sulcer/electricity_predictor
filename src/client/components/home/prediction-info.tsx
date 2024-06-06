'use client';
import React, {FC} from 'react';
import {usePredictions} from "@/lib/hooks/prediction-service";
import {DataTable} from "@/components/ui/data-table";
import {
    capitalizeFirstLetter,
    mapTableDataForPrediction,
    prepareDataAndLabelsForChart,
    prepareDataAndLabelsForPredictionChart, transformLinkName
} from "@/utils/utils";
import LineChart from "@/components/ui/line-chart";
import LoadingSpinner from "@/components/ui/loading-spinner";

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

const PredictionInfo: FC<PredictionInfoProps> = ({modelType, number}) => {
    const {data: prediction, isLoading, isError} = usePredictions(modelType, number);

    return (
        <div className={'w-full'}>
            {isLoading ? <LoadingSpinner/> : <>
                <h3 className={'text-xl font-bold mt-10'}>Predictions for {modelType === 'price' ? <>Tomorrow</> : <>Today</>} {transformLinkName(modelType)}</h3>
                <div className="flex justify-center items-center gap-20">
                    <div className="flex-1">
                        {isLoading ? <LoadingSpinner/> :
                            <DataTable columns={columns} data={mapTableDataForPrediction(prediction)}/>}
                    </div>
                    <div className="flex-1">
                        {isLoading ? <LoadingSpinner/> :
                            <LineChart chart_data={prepareDataAndLabelsForPredictionChart(prediction)}
                                       label={'Predicted values'}/>}
                    </div>
                </div>
            </>}
        </div>
    );
};

export default PredictionInfo;