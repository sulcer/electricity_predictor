'use client';
import React from 'react';
import {usePrice} from "@/lib/hooks/prediction-service";
import LineChart from "@/components/ui/line-chart";
import {mapTableData, prepareDataAndLabelsForChart} from "@/utils/utils";
import {DataTable} from "@/components/ui/data-table";

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
    const { data: price, isLoading, isError } = usePrice();

    return (
        <div className={'mt-5'}>
            <div>
                {isLoading ? <p>Loading...</p> : <DataTable columns={columns} data={mapTableData(price)} />}
            </div>
            <div className={'mt-5'}>
                 {isLoading ? <p>Loading...</p> : <LineChart chart_data={prepareDataAndLabelsForChart(price)}/> }
            </div>
        </div>
    );
};

export default PriceInfo;