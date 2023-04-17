import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {MDBInput} from 'mdb-react-ui-kit';
import {useLoginUserMutation, useRegisterUserMutation} from '../../services/auth/authApi';
import {toast} from 'react-toastify';
import {useAppDispatch} from '../../app/hooks';
import {setUser} from '../../features/auth/authSlice';

const initialState = {
	firstName: "",
	lastName: "",
	username: "",
	email: "",
	password: "",
	confirm_password: "",
}

const AuthPage = () => {
	const dispatch = useAppDispatch();
	const [form, setForm] = useState(initialState);
	const navigate = useNavigate();
	const {
		firstName, 
		lastName, 
		username,
		email,
		password,
		confirm_password
	} = form;
	const [showRegister, setShowRegister] = useState(false);
	const [loginUser, {
		data: loginData, 
		isSuccess: isSuccessLogin, 
		isError: isErrorLogin, 
		error: errorLogin
	}] = useLoginUserMutation();
	const [registerUser, {
		data: registerData, 
		isSuccess: isSuccessRegister, 
		isError: isErrorRegister, 
		error: errorRegister
	}] = useRegisterUserMutation();

	const handleChange = (e: any) => {
		setForm({...form, [e.target.name]: e.target.value})
	}

	const handleLogin = async () => {
		if (username && password) {
			await loginUser({username, password});
		} else {
			toast.error('Fill all Input field')
		}
	}

	const handleRegister = async () => {
		if (password !== confirm_password) {
			return toast.error("Password don't match");
		}
		if (email && username && password && confirm_password) {
			await registerUser({email, username, password, confirm_password});
		} else {
			toast.error('Fill all Input field');
		}
	}

	useEffect(() => {
		if(isSuccessLogin) {
			toast.success('User login successfully');
			dispatch(setUser({
				name: username,
				access: loginData.access,
				refresh: loginData.refresh,
			}))
			navigate('/dashboard');
		}
		if(isSuccessRegister) {
			toast.success('User registration successfully');
			navigate('/auth');
		}
	}, [isSuccessLogin, isSuccessRegister])

	useEffect(() => {
		if(isErrorLogin) {
			toast.error((errorLogin as any).data.message);
		}
		if(isErrorRegister) {
			const data = (errorRegister as any).data;
			for (let key in data) {
				data[key].forEach((err:any)=>toast.error(err));
			}
			// toast.error((errorRegister as any).data.message);
		}
	}, [isErrorLogin, isErrorRegister])

	return (
		<section className='vh-100 gradient-custom'>
			<div className="container py-4 h-100">
				<div className="row d-flex justify-content-center align-items-center h-100">
					<div className="col-12 col-md-8 col-lg-6 col-xl-5">
						<div className="card bg-dark text-white" style={{borderRadius:"1rem"}}>
							<div className="card-body p-4 text-center">
								<div className="md-md-5 mt-md-4 pb-5">
									<h2 className="fw-bold md-2 text-uppercase">
										{!showRegister 
											? "Login"
											: "Register"
										}
									</h2>
									<p className="text-white-50 mb-4">
										{!showRegister 
											? "Enter user name"
											: "Enter User detail"
										}
									</p>
									{showRegister && (
										<>
										{/*<div className="form-outline form-white mb-4">
											<MDBInput 
												type="text" 
												name="first_name" 
												value={firstName}
												onChange={handleChange}
												label="First name"
												className="form-control form-control-lg" 
											/>
										</div>
										<div className="form-outline form-white mb-4">
											<MDBInput 
												type="text" 
												name="last_name" 
												value={lastName}
												onChange={handleChange}
												label="Last name"
												className="form-control form-control-lg" 
											/>
										</div>*/}
										<div className="form-outline form-white mb-4">
											<MDBInput 
												type="email" 
												name="email" 
												value={email}
												onChange={handleChange}
												label="Email"
												className="form-control form-control-lg" 
											/>
										</div>
										</>
									)}
									<div className="form-outline form-white mb-4">
										<MDBInput 
											type="text" 
											name="username" 
											value={username}
											onChange={handleChange}
											label="User name"
											className="form-control form-control-lg" 
										/>
									</div>
									<div className="form-outline form-white mb-4">
										<MDBInput 
											type="password" 
											name="password" 
											value={password}
											onChange={handleChange}
											label="Password"
											className="form-control form-control-lg" 
										/>
									</div>
									{showRegister && (
										<>
										<div className="form-outline form-white mb-4">
											<MDBInput 
												type="password" 
												name="confirm_password" 
												value={confirm_password}
												onChange={handleChange}
												label="Confirm password"
												className="form-control form-control-lg" 
											/>
										</div>
										</>
									)}
									{!showRegister ? (
										<button 
											className="btn btn-outline-light btn-lg px-5"
											onClick={()=>handleLogin()}
										>
											Login
										</button>
									) : (
										<button 
											className="btn btn-outline-light btn-lg px-5"
											onClick={()=>handleRegister()}
										>
											Register
										</button>
									)}
									<div>
										<h5 className="mb-0 mt-5">
											{!showRegister ? (
												<>
													Don't have an account?
													<p 
														className="text-white-50 fw-bold"
														style={{cursor:"pointer"}}
														onClick={()=>setShowRegister(true)}
													>
														Sign Up
													</p>
												</>
											) : (
												<>
													Have an account?
													<p 
														className="text-white-50 fw-bold"
														style={{cursor:"pointer"}}
														onClick={()=>setShowRegister(false)}
													>
														Sign In
													</p>
												</>
											)}
										</h5>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	)
}

export default AuthPage