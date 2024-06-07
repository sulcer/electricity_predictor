import React from 'react';
import {useValidationMetrics} from "@/lib/hooks/prediction-service";
import LoadingSpinner from "@/components/ui/loading-spinner";
import {DataTable} from "@/components/ui/data-table";
import {mapTableDataForValidationMetrics} from "@/utils/utils";

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
        accessorKey: 'mean_error',
        header: 'Mean Error',
    },
    {
        accessorKey: 'mean_squared_error',
        header: 'Mean Squared Error',
    },
];


const ValidateExperiments = () => {
    const {data: metrics, isLoading, isError} = useValidationMetrics();

    return (
        <div className={'m-5'}>
            <h3 className={'text-xl font-bold mt-10'}>Model training metrics</h3>
            {isLoading ? <LoadingSpinner/> :
                <DataTable columns={columns} data={mapTableDataForValidationMetrics(metrics)}/>}
        </div>
    );
};

export default ValidateExperiments;