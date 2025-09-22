import { configureStore } from "@reduxjs/toolkit";
import searchReducer from "./searchSlice";

export const makeStore = () => {
  return configureStore({
    reducer: {
      search: searchReducer, // ключ "search" реально есть
    },
  });
};

export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore["getState"]>; // <-- теперь RootState знает про "search"
export type AppDispatch = AppStore["dispatch"];
