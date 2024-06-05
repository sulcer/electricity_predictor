'use client';
import React, {FC} from 'react';
import {Line} from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    CategoryScale
} from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, Title, Tooltip, Legend, CategoryScale);


const options = {
    scales: {
        y: {
            beginAtZero: true,
        },
    },
};

interface LineChartProps {
    chart_data: [number[], string[]];
    label: string;
}

const LineChart: FC<LineChartProps> = ({ chart_data, label }) => {
    const data = {
    labels: chart_data[1],
    datasets: [
        {
            label: label,
            backgroundColor: 'rgba(75,192,192,0.2)',
            borderColor: 'rgba(75,192,192,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(75,192,192,0.4)',
            hoverBorderColor: 'rgba(75,192,192,1)',
            data: chart_data[0],
        },
    ],
};

    return (
        <div className="max-h-[550px] max-w-4/5">
            <Line data={data} options={options}/>
        </div>
    );
};

export default LineChart;