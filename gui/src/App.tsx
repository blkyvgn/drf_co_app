import React, {useEffect} from 'react';
import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import AuthPage from './pages/auth/AuthPage';
import HomePage from './pages/front/company/HomePage';
import DashboardPage from './pages/back/company/DashboardPage';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {useAppDispatch} from './app/hooks';
import {setUser} from './features/auth/authSlice';
import PrivateRoute from './components/PrivateRoute';


function App() {
  const dispatch = useAppDispatch();
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  useEffect(() => {
    dispatch(setUser(user));
  }, []);
  return (
    <>
      <BrowserRouter>
        <ToastContainer/>
        <Routes>
          <Route path="/" element={<Navigate to="auth" replace/>}/>
          <Route path="/auth" element={<AuthPage/>}/>
          <Route path="/home" element={<HomePage/>}/>
          <Route path="/dashboard" element={
            <PrivateRoute>
              <DashboardPage/>
            </PrivateRoute>
          }/>
        </Routes>
      </BrowserRouter> 
    </>
  );
}

export default App;
