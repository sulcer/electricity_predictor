import PriceInfo from "@/components/home/price-info";
import ProductionInfo from "@/components/home/production-info";
import LineChart from "@/components/ui/line-chart";
import PredictionInfo from "@/components/home/prediction-info";

const production_types = ["cross", "fossil", "hydro", "nuclear"];
const prediction_types = [
    'price',
    'production_cross',
    'production_fossil',
    'production_hydro',
    'production_nuclear',
]

export default function Home() {
    return (
        <>
            {/*<PriceInfo/>*/}
            {/*{production_types.map((production_type) => <ProductionInfo production_type={production_type} key={production_type}/>)}*/}
            {/*{prediction_types.map((modelType) => <PredictionInfo modelType={modelType} number={24} key={modelType}/>)}*/}
        </>
    );
}