'use client';
import React from 'react';
import {usePrice} from "@/lib/hooks/prediction-service";
import CustomTable from "@/components/ui/custom-table";
import LineChart from "@/components/ui/line-chart";
import {prepareDataAndLabelsForChart} from "@/utils/utils";

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

    // console.log(!isLoading && prepareDataForChart(price));

    return (
        <div className={'mt-5'}>
            <div>
                {isLoading ? <p>Loading...</p> : <CustomTable columns={columns} data={price} />}
            </div>
            <div className={'mt-5'}>
                 {isLoading ? <p>Loading...</p> : <LineChart chart_data={prepareDataAndLabelsForChart(price)}/> }
            </div>
        </div>
    );
};

export default PriceInfo;