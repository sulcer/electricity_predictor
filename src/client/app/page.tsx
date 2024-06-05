import Navbar from "@/components/ui/Navbar";
import Link from "next/link";
import {transformLinkName} from "@/utils/utils";
import React from "react";

const prediction_types = [
    'price',
    'production_cross',
    'production_fossil',
    'production_hydro',
    'production_nuclear',
]

export default function Home() {
    return (
        <div className={'m-5'}>
            <Navbar/>
            <div className="flex flex-col min-h-[100dvh]">
                <main className="flex-1">
                    <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
                        <div className="container px-4 md:px-6">
                            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
                                <div className="flex flex-col justify-center space-y-4">
                                    <div className="space-y-2">
                                        <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">
                                            Accurate Electricity Forecasting for Slovenia
                                        </h1>
                                        <p className="max-w-[600px] text-gray-500 md:text-xl dark:text-gray-400">
                                            Our cutting-edge platform provides real-time data and precise forecasting to
                                            help you optimize your
                                            energy usage and costs.
                                        </p>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </section>
                    <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
                        <div className="container px-4 md:px-6">
                            <div className="flex flex-col items-center justify-center space-y-4 text-center">
                                <div className="space-y-2">
                                    <div
                                        className="inline-block rounded-lg bg-gray-100 px-3 py-1 text-sm dark:bg-gray-800">
                                        Key Features
                                    </div>
                                    <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">Optimize Your <span
                                        className={'hover:text-blue-600 hover:drop-shadow-2xl transition duration-300'}>Energy Usage</span>
                                    </h2>
                                    <p className="max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                                        Our platform provides accurate forecasting, real-time data, and a user-friendly
                                        interface to help you
                                        make informed decisions about your energy consumption.
                                    </p>
                                </div>
                            </div>
                            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-2 lg:gap-12">
                                <div className="flex flex-col justify-center space-y-4">
                                    <ul className="grid gap-6">
                                        <li>
                                            <div className="grid gap-1">
                                                <h3 className="text-xl font-bold">Accurate Forecasting</h3>
                                                <p className="text-gray-500 dark:text-gray-400">
                                                    Our advanced algorithms provide precise predictions of electricity
                                                    demand and supply to help you
                                                    plan ahead.
                                                </p>
                                            </div>
                                        </li>
                                        <li>
                                            <div className="grid gap-1">
                                                <h3 className="text-xl font-bold">Real-Time Data</h3>
                                                <p className="text-gray-500 dark:text-gray-400">
                                                    Monitor your energy usage in real-time and make informed decisions
                                                    to
                                                    optimize your consumption.
                                                </p>
                                            </div>
                                        </li>
                                        <li>
                                            <div className="grid gap-1">
                                                <h3 className="text-xl font-bold">User-Friendly Interface</h3>
                                                <p className="text-gray-500 dark:text-gray-400">
                                                    Our intuitive dashboard makes it easy to understand and analyze your
                                                    energy data.
                                                </p>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                                <div className="flex flex-col justify-center space-y-4">
                                    <ul className="grid gap-6">
                                        <li>
                                            <div className="grid gap-1">
                                                <h3 className="text-xl font-bold">Latest Technologies Used</h3>
                                                <p className="text-gray-500 dark:text-gray-400">
                                                    We use cutting-edge technologies to provide you with the most accurate
                                                    and up-to-date information.
                                                </p>
                                            </div>
                                        </li>
                                        <li>
                                            <div className="grid gap-1">
                                                <h3 className="text-xl font-bold">Interactive Dashboard</h3>
                                                <p className="text-gray-500 dark:text-gray-400">
                                                    Take a look at models in realtime and see how they perform.
                                                </p>
                                            </div>
                                        </li>
                                        <li>
                                            <div className="grid gap-1">
                                                <h3 className="text-xl font-bold">Compare Realtime and Predicted Data</h3>
                                                <p className="text-gray-500 dark:text-gray-400">
                                                    See how well our models perform in real-time and compare them to
                                                    actual data.
                                                </p>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </section>
                    <section className="w-full py-12 md:py-24 lg:py-32 border-t">
                        <div className="container grid items-center justify-center gap-4 px-4 text-center md:px-6">
                            <div className="space-y-3">
                                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">
                                    Take Control of Your Energy Costs
                                </h2>
                                <p className="mx-auto max-w-[600px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                                    With use of our electricity prediction service start optimizing your energy usage
                                    today.
                                </p>
                            </div>
                            <div className={'flex flex-1 gap-x-20 mt-20'}>
                                {prediction_types.map((modelType) => {
                                    return (
                                        <div key={modelType}>
                                            <Link
                                                className={"font-bold hover:text-blue-600 hover:drop-shadow-2xl  transition duration-300"}
                                                href={`/details/${modelType}`}>{transformLinkName(modelType)}</Link>
                                        </div>
                                    )
                                })}
                            </div>
                        </div>
                    </section>
                </main>
            </div>
        </div>
    );
}