import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

export interface IAuth {
	username: string;
	password: string;
}

export const authApi = createApi({
	reducerPath: 'authApi',
	baseQuery: fetchBaseQuery({
		baseUrl: 'http://127.0.0.1:8000/'
	}),
	endpoints: (builder) => ({
		loginUser:  builder.mutation({
			query: (body: {username: string, password: string}) => {
				return {
					url: 'api/token/',
					method: 'post',
					headers: {
      					Accept: "application/json",
      					"Content-Type": "application/json"
					},
					body: JSON.stringify(
						{
							username: String(body.username), 
							password: String(body.password),
						}
					),
				}
			}
		}),
		registerUser: builder.mutation({
			query: (body: {email: string, username: string, password: string, confirm_password: string}) => {
				return {
					url: 'api/account/registration/',
					method: 'post',
					headers: {
      					Accept: "application/json",
      					"Content-Type": "application/json"
					},
					body: JSON.stringify(
						{
							email: String(body.email), 
							username: String(body.username), 
							password: String(body.password),
							password_confirm: String(body.confirm_password),
						}
					),
				}
			}
		})
	})
})

export const {useLoginUserMutation, useRegisterUserMutation} = authApi