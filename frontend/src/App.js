import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Experiments from './pages/Experiments';
import ExperimentDetail from './pages/ExperimentDetail';
import NewExperiment from './pages/NewExperiment';

// Protected route — redirects to login if not authenticated
function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes */}
        <Route path="/experiments" element={
          <PrivateRoute><Experiments /></PrivateRoute>
        } />
        <Route path="/experiments/new" element={
          <PrivateRoute><NewExperiment /></PrivateRoute>
        } />
        <Route path="/experiments/:id" element={
          <PrivateRoute><ExperimentDetail /></PrivateRoute>
        } />

        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/experiments" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;