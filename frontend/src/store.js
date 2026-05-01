import { configureStore, createSlice } from "@reduxjs/toolkit";

const crmSlice = createSlice({
  name: "crm",
  initialState: { response: "" },
  reducers: {
    setResponse: (state, action) => {
      state.response = action.payload;
    },
  },
});

export const { setResponse } = crmSlice.actions;

export const store = configureStore({
  reducer: { crm: crmSlice.reducer },
});