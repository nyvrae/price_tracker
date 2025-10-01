import '@ant-design/v5-patch-for-react-19';

import './globals.css';

import StoreProvider from './StoreProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body>
                <StoreProvider>
                    {children}
                </StoreProvider>
            </body>
        </html>
    );
}