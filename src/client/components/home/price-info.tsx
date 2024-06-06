'use client';
import React from 'react';
import {usePrice} from "@/lib/hooks/prediction-service";
import LineChart from "@/components/ui/line-chart";
import {mapTableData, prepareDataAndLabelsForChart} from "@/utils/utils";
import {DataTable} from "@/components/ui/data-table";
import LoadingSpinner from "@/components/ui/loading-spinner";

const columns = [
    {
        accessorKey: 'date',
        header: 'Date',
    },
    {
        accessorKey: 'value',
        header: 'Price',
    },
];

const PriceInfo = () => {
    const {data: price, isLoading, isError} = usePrice();

    return (
        <div className={' w-full'}>
            {isLoading ? <LoadingSpinner/> : <>
                <h3 className={'text-xl font-bold mt-10'}>Data for Today Price</h3>
                <div className="flex justify-center items-center gap-20">
                    <div className="flex-1">
                        {isLoading ? <LoadingSpinner/> : <DataTable columns={columns} data={mapTableData(price)}/>}
                    </div>
                    <div className="flex-1">
                        {isLoading ? <LoadingSpinner/> :
                            <LineChart chart_data={prepareDataAndLabelsForChart(price)} label={'Actual values'}/>}
                    </div>
                </div>
            </>}
        </div>
    );
};

export default PriceInfo;