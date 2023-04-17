import React from 'react';
import {useNavigate} from 'react-router-dom';
import {useAppSelector, useAppDispatch} from '../../../app/hooks';
import {selectAuth, logout} from '../../../features/auth/authSlice';
import {toast} from 'react-toastify';

const HomePage = () => {
	const dispatch = useAppDispatch()
	const {name} = useAppSelector(selectAuth);
	const navigate = useNavigate();

	const loginHandle = () => {
		navigate('/auth');
	}

	return (
		<div className="vh-100 gradient-custom">
			
				<div className="row d-flex justify-content-center align-items-center h-100">
					<div className="col-12 col-md-8 col-lg-6 col-xl-5">
						<div className="card bg-dark text-white" style={{borderRadius:"1rem"}}>
							<div className="card-body p-4 text-center">
								<div className="md-md-5 mt-md-4 pb-5">
									<h2 className="fw-bold md-2">
										Home page
									</h2>
									{!name ? (
										<button 
											className="btn btn-outline-light btn-lg px-5 mt-3"
											type="button"
											onClick={()=>loginHandle()}
										>
											Login
										</button>
									) : (
										<h4>
											Name: {name}
										</h4>
									)}
									
								</div>
							</div>
						</div>
					</div>
				</div>
			
		</div>
	)
}

export default HomePage