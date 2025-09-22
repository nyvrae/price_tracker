type SearchProps = {
    onSubmit?: (value: string) => void;
};

export default function Search({ onSubmit }: SearchProps) {
    function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
        if (e.key === "Enter") {
            e.preventDefault();
            onSubmit?.(e.currentTarget.value);
        }
    }

    return (
        <div className="relative w-full max-w-md mt-[40px] md:mt-[100px] flex items-center justify-center px-4">
            <input
                id="email"
                type="email"
                onKeyDown={handleKeyDown}
                className="peer w-full 
                           px-6 py-3 
                           rounded-full 
                           border border-gray-500 bg-back 
                           text-white placeholder-transparent 
                           focus:outline-none focus:border-blue-500"
                placeholder="Email"
                required
            />
            <label
                htmlFor="email"
                className="absolute left-10 top-2.5 
                           pt-[2px] bg-black px-1 text-base 
                           text-gray-500 duration-200 transform 
                           origin-[0] peer-focus:-top-3.5 
                           peer-focus:scale-75 peer-focus:text-blue-500 
                           peer-[&:not(:placeholder-shown)]:-top-3.5 
                           peer-[&:not(:placeholder-shown)]:scale-75
                           hover:cursor-text">
                Search products...
            </label>
        </div>
    );
}
