export const unixToLocalDatetime = (unixTime: number): string => {
    const date = new Date(unixTime * 1000);
    return date.toLocaleString();
}

export const mapTableData = (data: any) => {
    const mappedData: any = [];
    data.map((d: any) => {
        mappedData.push({
            date: unixToLocalDatetime(d[0]),
            value: d[1]
        });
    });

    return mappedData;
}

export const capitalizeFirstLetter = (word: string): string => {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

export const prepareDataAndLabelsForChart = (data: Array<Array<number>> | any): [number[], string[]] => {
    const chartData: any = [];
    const tableData: any = [];

    data.map((d: any) => {
        chartData.push(d[1]);
        tableData.push(unixToLocalDatetime(d[0]).substring(11, 17));
    });

    return [chartData, tableData];
}


export const mapTableDataForPrediction = (data: any) => {
    data = data.message;

    const mappedData: any = [];
    data.map((d: any, index: number) => {
        const formattedIndex = String(index).padStart(2, '0');
        const formattedDate = `${formattedIndex}:00`;
        mappedData.push({
            date: formattedDate,
            value: d
        });
    });

    return mappedData;
}


export const prepareDataAndLabelsForPredictionChart = (data: Array<number> | any): [number[], string[]] => {
    data = data.message;

    const chartData: any = [];
    const tableData: any = [];

    data.map((d: any, index: number) => {
        const formattedIndex = String(index).padStart(2, '0');
        const formattedDate = `${formattedIndex}:00`;
        chartData.push(d);
        tableData.push(formattedDate);
    });

    return [chartData, tableData];
}

export const transformLinkName = (str: string) => {
    str = capitalizeFirstLetter(str);

    if (str.includes('_')) {
        const words = str.split('_');
        if (words.length === 2) {
            str = capitalizeFirstLetter(words[1]) + ' ' + capitalizeFirstLetter(words[0]);
        } else {
            str = words.map(capitalizeFirstLetter).join(' ');
        }
    }
    return str;
}

export const mapTableDataForValidationMetrics = (data: any) => {
    const mappedData: any = [];

    data.start_time.forEach((_: any, index: number) => {
        mappedData.push({
            start_time: new Date(data.start_time[index]).toLocaleString(),
            end_time: new Date(data.end_time[index]).toLocaleString(),
            mean_error: data.mean_error[index],
            mean_squared_error: data.mean_squared_error[index]
        });
    });

    return mappedData;
}

export const mapTableDataForTrainingMetrics = (data: any) => {
    const mappedData: any = [];

    data.start_time.forEach((_: any, index: number) => {
        mappedData.push({
            start_time: new Date(data.start_time[index]).toLocaleString(),
            end_time: new Date(data.end_time[index]).toLocaleString(),
            EVS_latest: data.EVS_latest[index],
            MAE_latest: data.MAE_latest[index],
            MSE_latest: data.MSE_latest[index]
        });
    });

    return mappedData;
}