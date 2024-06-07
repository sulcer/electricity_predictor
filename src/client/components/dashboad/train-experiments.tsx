import React from 'react';
import {useTrainingMetrics} from "@/lib/hooks/prediction-service";
import LoadingSpinner from "@/components/ui/loading-spinner";
import {DataTable} from "@/components/ui/data-table";
import {mapTableDataForTrainingMetrics} from "@/utils/utils";

 const columns = [
    {
        accessorKey: 'start_time',
        header: 'Start Time',
    },
    {
        accessorKey: 'end_time',
        header: 'End Time',
    },
    {
        accessorKey: 'EVS_latest',
        header: 'Explained Variance Score',
    },
    {
        accessorKey: 'MAE_latest',
        header: 'Mean Average Error',
    },
    {
        accessorKey: 'MSE_latest',
        header: 'Mean Squared Error',
    },
];


const TrainExperiments = () => {
    const {data: metrics, isLoading, isError} = useTrainingMetrics();

    return (
        <div className={'m-5'}>
            <h3 className={'text-xl font-bold mt-10'}>Model training metrics</h3>
            {isLoading ? <LoadingSpinner/> :
                <DataTable columns={columns} data={mapTableDataForTrainingMetrics(metrics)}/>}
        </div>
    );
};

export default TrainExperiments;