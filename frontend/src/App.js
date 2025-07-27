import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { setTheme } from './redux/slices/themeSlice';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import StudentDashboard from './pages/StudentDashboard';
import PairingHistory from './pages/PairingHistory';
import Profile from './pages/Profile';
import AdminDashboard from './pages/AdminDashboard';

// Route guards
import ProtectedRoute from './routes/ProtectedRoute';
import AdminRoute from './routes/AdminRoute';

function App() {
  const dispatch = useDispatch();
  const { mode } = useSelector((state) => state.theme);
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  useEffect(() => {
    // Apply initial theme
    dispatch(setTheme(mode));
  }, [dispatch, mode]);

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public routes */}
          <Route 
            path="/login" 
            element={
              isAuthenticated ? (
                <Navigate to={user?.role === 'admin' ? '/dashboard/admin' : '/dashboard/student'} replace />
              ) : (
                <Login />
              )
            } 
          />
          <Route 
            path="/register" 
            element={
              isAuthenticated ? (
                <Navigate to={user?.role === 'admin' ? '/dashboard/admin' : '/dashboard/student'} replace />
              ) : (
                <Register />
              )
            } 
          />

          {/* Protected student routes */}
          <Route
            path="/dashboard/student"
            element={
              <ProtectedRoute>
                <StudentDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/student/history"
            element={
              <ProtectedRoute>
                <PairingHistory />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard/student/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />

          {/* Protected admin routes */}
          <Route
            path="/dashboard/admin"
            element={
              <AdminRoute>
                <AdminDashboard />
              </AdminRoute>
            }
          />

          {/* Default redirect */}
          <Route
            path="/"
            element={
              <Navigate 
                to={
                  isAuthenticated 
                    ? user?.role === 'admin' 
                      ? '/dashboard/admin' 
                      : '/dashboard/student'
                    : '/login'
                } 
                replace 
              />
            }
          />

          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;