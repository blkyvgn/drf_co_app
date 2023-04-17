import React from 'react';
import {useSelector} from 'react-redux';
import {selectAuth} from '../features/auth/authSlice';
import LoadingToRedirect from './LoadingToRedirect';


const PrivateRoute = ({children}:{children:any}) => {
	const {access} = useSelector(selectAuth);
	return access ? children : <LoadingToRedirect/>;
}

export default PrivateRoute