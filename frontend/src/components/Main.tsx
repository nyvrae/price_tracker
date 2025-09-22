'use client'

import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { fetchSearchResults } from "@/lib/searchSlice";
import Search from "./ui/Search";

export default function Main() {
    const dispatch = useAppDispatch();
    const { results, loading, error } = useAppSelector((state) => state.search);

    function handleSearch(value: string) {
        dispatch(fetchSearchResults(value));
    }

    return (
        <section className="flex flex-col items-center">
            <h1 className="text-4xl md:text-6xl font-bebas text-accent text-center px-4 tracking-wide">Never pay full price again</h1>

            <Search onSubmit={handleSearch} />

            {loading && <p>Загрузка...</p>}
            {error && <p className="text-red-500">{error}</p>}

            {results.length > 0 && (
                <ul>
                    {results.map((item, idx) => (
                        <li key={idx}>{item.name || JSON.stringify(item)}</li>
                    ))}
                </ul>
            )}
        </section>
    );
}
