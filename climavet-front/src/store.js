import { configureStore, createSlice } from '@reduxjs/toolkit'

const store = configureStore({
  reducer: {
    // Add your reducers here
    clinic: createSlice({
      name: 'clinic',
      initialState: {
        id: null,
      },
      reducers: {
        setClinicId: (state, action) => {
          state.id = action.payload;
        },
      },
    }),
  },
})

export default store