import { useState, useRef, useEffect } from "react";
import { Select, Input, Button } from "antd";
import { SwapOutlined, SearchOutlined } from "@ant-design/icons";

const { Option } = Select;

type SearchAndFilterProps = {
    onSearch?: (titleQuery: string, keywordsQuery: string) => void;
};

export default function SearchBar({ onSearch }: SearchAndFilterProps) {
    const [titleQuery, setTitleQuery] = useState("");
    const [keywordsQuery, setKeywordsQuery] = useState("");
    const [order, setOrder] = useState("asc");
    const [filterType, setFilterType] = useState("title");
    const [minPrice, setMinPrice] = useState<string | undefined>();
    const [maxPrice, setMaxPrice] = useState<string | undefined>();

    const secondRowRef = useRef<HTMLDivElement>(null);
    const [secondRowWidth, setSecondRowWidth] = useState<number | undefined>();

    useEffect(() => {
        if (secondRowRef.current) {
            const observer = new ResizeObserver(() => {
                setSecondRowWidth(secondRowRef.current?.offsetWidth);
            });
            observer.observe(secondRowRef.current);
            return () => observer.disconnect();
        }
    }, []);

    function handleSearch() {
        if (titleQuery.trim() || keywordsQuery.trim()) {
            onSearch?.(titleQuery, keywordsQuery);
        }
    }

    const separator = <div className="border-l border-gray-300 h-6 mx-2" />;

    return (
        <div className="flex flex-col shadow-lg rounded-2xl bg-white max-w-4xl w-full p-3 gap-3">
            <div className="flex items-stretch gap-1 md:gap-2">
                <Button
                    type="primary"
                    shape="circle"
                    icon={<SearchOutlined />}
                    onClick={handleSearch}
                    className="rounded-full border-none shadow-none shrink-0"
                />
                <Input
                    value={titleQuery}
                    onChange={(e) => setTitleQuery(e.target.value)}
                    onPressEnter={handleSearch}
                    placeholder="Search by title..."
                    style={{ maxWidth: secondRowWidth }}
                    className="flex-1 border-none shadow-none outline-none min-w-[180px]"
                />
            </div>

            <div
                ref={secondRowRef}
                className="flex flex-col md:flex-row flex-wrap items-stretch gap-2"
            >
                <div className="flex items-center gap-1 md:gap-2 flex-1">
                    <Select
                        value={filterType}
                        onChange={(val) => setFilterType(val)}
                        className="!w-[120px] md:!w-[150px] border-none shadow-none outline-none"
                    >
                        <Option value="title">Title</Option>
                        <Option value="keywords">Keywords</Option>
                    </Select>
                    {separator}
                    <Input
                        value={keywordsQuery}
                        onChange={(e) => setKeywordsQuery(e.target.value)}
                        onPressEnter={handleSearch}
                        placeholder={`Enter ${filterType === "title" ? "title" : "keywords"
                            }`}
                        className="flex-1 border-none shadow-none outline-none !w-[110px] md:!w-[150px]"
                        suffix={<SearchOutlined />}
                    />
                </div>
                <span className="hidden md:block self-center">
                    {separator}
                </span>
                <div className="flex items-center gap-1 md:gap-2 flex-shrink-0">
                    <Input
                        type="number"
                        placeholder="Min. price"
                        value={minPrice}
                        onChange={(e) => setMinPrice(e.target.value)}
                        className="!w-[80px] border-none shadow-none outline-none"
                    />
                    <span className="text-gray-400">—</span>
                    <Input
                        type="number"
                        placeholder="Max. price"
                        value={maxPrice}
                        onChange={(e) => setMaxPrice(e.target.value)}
                        className="!w-[80px] border-none shadow-none outline-none"
                    />
                    {separator}
                    <Button
                        onClick={() => setOrder(order === "asc" ? "desc" : "asc")}
                        icon={<SwapOutlined />}
                        className="border-none shadow-none"
                    >
                        {order === "asc" ? "Asc" : "Desc"}
                    </Button>
                </div>
            </div>
        </div>
    );
}
