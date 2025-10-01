'use client'

import { useAppDispatch, useAppSelector } from "@/lib/hooks";
import { startSearch, fetchProducts } from "@/lib/searchSlice";
import SearchBar from "./ui/SearchBar";
import ItemLink from "./ui/ItemLink";

export default function Main() {
    const dispatch = useAppDispatch();
    const { products, loading, error } = useAppSelector((state) => state.search);

    function handleSearch(title: string, keywords?: string) {
        const query = title || keywords || "";
        dispatch(startSearch(query));
        dispatch(fetchProducts());
    }

    return (
        <section className="flex flex-col items-center gap-8 w-full px-4">
            <SearchBar onSearch={handleSearch} />

            {loading && <p>Loading...</p>}
            {error && <p className="text-red-500">{error}</p>}

            {products.length > 0 && (
                <ul className="flex flex-col gap-4 items-center w-full justify-center">
                    {products.map((item, idx) => (
                        <li key={idx} className="w-full flex justify-center items-center">
                            <ItemLink
                                title={
                                    item.title && item.title.length > 30
                                        ? item.title.slice(0, 30) + "..."
                                        : item.title ?? "No title"
                                }
                                url={item.url ?? "#"}
                                price={
                                    item.prices && item.prices.length > 0
                                        ? `${item.prices[item.prices.length - 1].price}`
                                        : "—"
                                }
                                image_url={item.image_url ?? ""}
                                date={item.created_at ?? ""}
                            />
                        </li>
                    ))}
                </ul>
            )}
        </section>
    );
}
