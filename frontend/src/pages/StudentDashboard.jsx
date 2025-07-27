import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchCurrentPairing } from '../redux/slices/pairingSlice';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';
import Toast from '../components/Toast';
import { UserGroupIcon, CalendarIcon, UserIcon } from '@heroicons/react/24/outline';

const StudentDashboard = () => {
  const dispatch = useDispatch();
  const { currentPairing, isLoading, error } = useSelector((state) => state.pairing);
  const { user } = useSelector((state) => state.auth);
  const [showToast, setShowToast] = useState(false);

  useEffect(() => {
    dispatch(fetchCurrentPairing());
  }, [dispatch]);

  useEffect(() => {
    if (error) {
      setShowToast(true);
    }
  }, [error]);

  const handleCloseToast = () => {
    setShowToast(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      
      {/* Toast notification */}
      {showToast && error && (
        <Toast
          message={error}
          type="error"
          onClose={handleCloseToast}
        />
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Welcome back, {user?.full_name}!
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Here's your current pairing information
          </p>
        </div>

        {/* Current pairing card */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <UserGroupIcon className="h-6 w-6 text-primary-600" />
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                Current Pairing
              </h2>
            </div>

            {isLoading ? (
              <div className="flex justify-center py-8">
                <LoadingSpinner />
              </div>
            ) : currentPairing?.success ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <CalendarIcon className="h-5 w-5 text-gray-500" />
                  <span className="text-gray-700 dark:text-gray-300">
                    Week {currentPairing.week_number}
                  </span>
                </div>
                
                {currentPairing.paired_with ? (
                  <div className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-4">
                    <div className="flex items-center space-x-3">
                      <UserIcon className="h-5 w-5 text-primary-600" />
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white">
                          {currentPairing.paired_with.full_name}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {currentPairing.paired_with.email}
                        </p>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-4">
                    <p className="text-yellow-800 dark:text-yellow-200">
                      You don't have a partner this week. Check back later!
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <p className="text-gray-600 dark:text-gray-400">
                  No pairing information available for this week.
                </p>
              </div>
            )}
          </div>

          {/* Quick stats */}
          <div className="card p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Quick Stats
            </h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400">Role</span>
                <span className="font-medium text-gray-900 dark:text-white capitalize">
                  {user?.role}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400">Status</span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
                  Active
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Quick actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card p-6 hover:shadow-lg transition-shadow duration-200 cursor-pointer">
            <div className="flex items-center space-x-3">
              <ClockIcon className="h-8 w-8 text-primary-600" />
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  View History
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  See your past pairings
                </p>
              </div>
            </div>
          </div>

          <div className="card p-6 hover:shadow-lg transition-shadow duration-200 cursor-pointer">
            <div className="flex items-center space-x-3">
              <UserIcon className="h-8 w-8 text-primary-600" />
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  Update Profile
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Manage your preferences
                </p>
              </div>
            </div>
          </div>

          <div className="card p-6 hover:shadow-lg transition-shadow duration-200 cursor-pointer">
            <div className="flex items-center space-x-3">
              <UserGroupIcon className="h-8 w-8 text-primary-600" />
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  Give Feedback
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Rate your partner
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;