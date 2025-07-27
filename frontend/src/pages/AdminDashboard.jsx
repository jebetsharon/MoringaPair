import { useState } from 'react';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';
import Toast from '../components/Toast';
import apiService from '../services/api';
import { 
  ShieldCheckIcon, 
  UserGroupIcon, 
  PlusIcon,
  CalendarIcon 
} from '@heroicons/react/24/outline';

const AdminDashboard = () => {
  const [isCreatingPairings, setIsCreatingPairings] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('success');

  const handleCreateNewWeekPairings = async () => {
    try {
      setIsCreatingPairings(true);
      const response = await apiService.createNewWeekPairings({
        description: 'Auto-generated weekly pairings'
      });
      
      if (response.success) {
        setToastMessage(`Successfully created pairings for week ${response.week.week_number}!`);
        setToastType('success');
        setShowToast(true);
      }
    } catch (error) {
      setToastMessage('Failed to create new week pairings');
      setToastType('error');
      setShowToast(true);
    } finally {
      setIsCreatingPairings(false);
    }
  };

  const handleCloseToast = () => {
    setShowToast(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      
      {/* Toast notification */}
      {showToast && (
        <Toast
          message={toastMessage}
          type={toastType}
          onClose={handleCloseToast}
        />
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-2">
            <ShieldCheckIcon className="h-8 w-8 text-primary-600" />
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Admin Dashboard
            </h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400">
            Manage pairings and oversee the platform
          </p>
        </div>

        {/* Quick actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <PlusIcon className="h-6 w-6 text-green-600" />
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Create New Week
              </h2>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Generate pairings for a new week automatically
            </p>
            <button
              onClick={handleCreateNewWeekPairings}
              disabled={isCreatingPairings}
              className="w-full btn-primary flex items-center justify-center space-x-2"
            >
              {isCreatingPairings ? (
                <LoadingSpinner size="sm" />
              ) : (
                <>
                  <PlusIcon className="h-4 w-4" />
                  <span>Create Pairings</span>
                </>
              )}
            </button>
          </div>

          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <UserGroupIcon className="h-6 w-6 text-blue-600" />
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                Manage Users
              </h2>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              View and manage all registered users
            </p>
            <button className="w-full btn-secondary">
              View Users
            </button>
          </div>

          <div className="card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <CalendarIcon className="h-6 w-6 text-purple-600" />
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                View All Pairings
              </h2>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              See all current and past pairings
            </p>
            <button className="w-full btn-secondary">
              View Pairings
            </button>
          </div>
        </div>

        {/* Stats overview */}
        <div className="card p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Platform Overview
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600 mb-2">--</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Total Users</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">--</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Active Pairings</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">--</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Total Weeks</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">--</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Feedback Received</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;