import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from '../../services/api';

// Async thunks
export const fetchCurrentPairing = createAsyncThunk(
  'pairing/fetchCurrentPairing',
  async (_, { rejectWithValue }) => {
    try {
      const response = await apiService.getCurrentPairing();
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchPairingHistory = createAsyncThunk(
  'pairing/fetchPairingHistory',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await apiService.getPairingHistory(params);
      return response;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const initialState = {
  currentPairing: null,
  pairingHistory: [],
  pagination: null,
  isLoading: false,
  error: null,
};

const pairingSlice = createSlice({
  name: 'pairing',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Current pairing
      .addCase(fetchCurrentPairing.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchCurrentPairing.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentPairing = action.payload;
      })
      .addCase(fetchCurrentPairing.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })
      // Pairing history
      .addCase(fetchPairingHistory.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPairingHistory.fulfilled, (state, action) => {
        state.isLoading = false;
        state.pairingHistory = action.payload.pairings || [];
        state.pagination = action.payload.pagination || null;
      })
      .addCase(fetchPairingHistory.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError } = pairingSlice.actions;
export default pairingSlice.reducer;