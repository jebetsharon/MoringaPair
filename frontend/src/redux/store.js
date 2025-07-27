import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import pairingReducer from './slices/pairingSlice';
import themeReducer from './slices/themeSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    pairing: pairingReducer,
    theme: themeReducer,
  },
});

export default store;