'use client'

import Search from "./ui/Search";

export default function Main() {
    function handleSearch(value: string) {
        alert("Search using query: " + value);
    }

    return (
        <section className="flex justify-center items-center flex-col">
            <h1 className="text-4xl md:text-6xl font-bebas text-accent text-center px-4 tracking-wide">Never pay full price again</h1>
            <Search onSubmit={handleSearch} />
        </section>
    );
}