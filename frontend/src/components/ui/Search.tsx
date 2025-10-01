import { useState } from "react";
import { Input, Button } from "antd";
import { SearchOutlined } from "@ant-design/icons";

type SearchProps = {
    onSubmit?: (value: string) => void;
};

export default function Search({ onSubmit }: SearchProps) {
    const [value, setValue] = useState("");

    function handleSearch() {
        if (value.trim()) {
            onSubmit?.(value);
        }
    }

    return (
        <div className="flex items-center justify-center mt-[40px] md:mt-[100px] px-4 w-full max-w-md">
            <Input
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onPressEnter={handleSearch}
                placeholder="Search products..."
                style={{ borderRadius: "9999px", padding: "10px 16px" }}
            />
            <Button
                type="primary"
                shape="circle"
                icon={<SearchOutlined />}
                onClick={handleSearch}
                style={{ marginLeft: "8px" }}
            />
        </div>
    );
}
