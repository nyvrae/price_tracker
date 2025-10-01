import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { getAllProducts, triggerSearch } from "./api";

type Product = {
  id: number;
  title: string;
  url: string;
  image_url: string;
  prices: { site: string; price: number; created_at: string }[];
  created_at: string;
  updated_at: string;
};

type SearchState = {
  products: Product[];
  loading: boolean;
  error: string | null;
};

const initialState: SearchState = {
  products: [],
  loading: false,
  error: null,
};

export const startSearch = createAsyncThunk(
  "search/startSearch",
  async (query: string, { rejectWithValue }) => {
    try {
      const data = await triggerSearch(query);
      return data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.message || "Ошибка запуска поиска"
      );
    }
  }
);

export const fetchProducts = createAsyncThunk(
  "search/fetchProducts",
  async (_, { rejectWithValue }) => {
    try {
      const data = await getAllProducts();
      return data;
    } catch (err: any) {
      return rejectWithValue(
        err.response?.data?.message || "Ошибка получения товаров"
      );
    }
  }
);

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    clearResults(state) {
      state.products = [];
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchProducts.fulfilled,
        (state, action: PayloadAction<Product[]>) => {
          state.loading = false;
          state.products = action.payload;
        }
      )
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(startSearch.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(startSearch.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(startSearch.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearResults } = searchSlice.actions;
export default searchSlice.reducer;
