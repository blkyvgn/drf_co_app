import {createSlice, PayloadAction} from '@reduxjs/toolkit/';
import {RootState} from '../../app/store';

export interface AuthState {
	name: string | null;
	access: string | null;
	refresh: string | null;
}

const initialState: AuthState = {
	name: null,
	access: null,
	refresh: null,
}

export const authSlice = createSlice({
	name: 'auth',
	initialState,
	reducers: {
		setUser: (state, action: PayloadAction<{name: string, access: string, refresh: string}>) => {
			localStorage.setItem(
				'user', 
				JSON.stringify({
					name: action.payload.name,
					access: action.payload.access,
					refresh: action.payload.refresh,
				})
			);
			state.name = action.payload.name;
			state.access = action.payload.access;
			state.refresh = action.payload.refresh;
		},
		logout: (state) => {
			localStorage.clear()
			state.name = null;
			state.access = null;
			state.refresh = null;
		}
	},
});

export const selectAuth = (state: RootState) => state.auth;
export const {setUser, logout} = authSlice.actions;
export default authSlice.reducer;
