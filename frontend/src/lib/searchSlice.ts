import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { searchProducts } from "./api";

type SearchState = {
  results: any[];
  loading: boolean;
  error: string | null;
};

const initialState: SearchState = {
  results: [],
  loading: false,
  error: null,
};

export const fetchSearchResults = createAsyncThunk(
  "search/fetchResults",
  async (query: string, { rejectWithValue }) => {
    try {
      const data = await searchProducts(query);
      return data;
    } catch (err: any) {
      return rejectWithValue(err.response?.data?.message || "Ошибка поиска");
    }
  }
);

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    clearResults(state) {
      state.results = [];
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchSearchResults.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchSearchResults.fulfilled,
        (state, action: PayloadAction<any[]>) => {
          state.loading = false;
          state.results = action.payload;
        }
      )
      .addCase(fetchSearchResults.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearResults } = searchSlice.actions;
export default searchSlice.reducer;
