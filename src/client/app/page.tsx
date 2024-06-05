import PriceInfo from "@/components/home/price-info";
import ProductionInfo from "@/components/home/production-info";
import LineChart from "@/components/ui/line-chart";

const production_types = ["cross", "fossil", "hydro", "nuclear"];

export default function Home() {
    return (
        <>
            <PriceInfo/>
            {/*{production_types.map((production_type) => <ProductionInfo production_type={production_type} key={production_type}/>)}*/}
        </>
    );
}