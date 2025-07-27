import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchPairingHistory } from '../redux/slices/pairingSlice';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';
import Toast from '../components/Toast';
import { ClockIcon, UserIcon, CalendarIcon } from '@heroicons/react/24/outline';

const PairingHistory = () => {
  const dispatch = useDispatch();
  const { pairingHistory, pagination, isLoading, error } = useSelector((state) => state.pairing);
  const [showToast, setShowToast] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    dispatch(fetchPairingHistory({ page: currentPage, per_page: 10 }));
  }, [dispatch, currentPage]);

  useEffect(() => {
    if (error) {
      setShowToast(true);
    }
  }, [error]);

  const handleCloseToast = () => {
    setShowToast(false);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
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
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-2">
            <ClockIcon className="h-8 w-8 text-primary-600" />
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Pairing History
            </h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400">
            View all your past pairing sessions
          </p>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        ) : pairingHistory.length > 0 ? (
          <div className="space-y-6">
            {/* Pairing cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pairingHistory.map((pairing) => (
                <div key={pairing.pairing_id} className="card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <CalendarIcon className="h-5 w-5 text-primary-600" />
                    <span className="font-medium text-gray-900 dark:text-white">
                      Week {pairing.week.week_number}
                    </span>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                        Description
                      </p>
                      <p className="text-gray-900 dark:text-white">
                        {pairing.week.description}
                      </p>
                    </div>
                    
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Partner
                      </p>
                      {pairing.student_b ? (
                        <div className="flex items-center space-x-2">
                          <UserIcon className="h-4 w-4 text-gray-500" />
                          <div>
                            <p className="font-medium text-gray-900 dark:text-white">
                              {pairing.student_b.full_name}
                            </p>
                            <p className="text-xs text-gray-600 dark:text-gray-400">
                              {pairing.student_b.email}
                            </p>
                          </div>
                        </div>
                      ) : (
                        <p className="text-gray-500 dark:text-gray-400 italic">
                          No partner assigned
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {pagination && pagination.total_pages > 1 && (
              <div className="flex justify-center space-x-2 mt-8">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="px-3 py-2 rounded-md bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                
                {Array.from({ length: pagination.total_pages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`px-3 py-2 rounded-md ${
                      currentPage === page
                        ? 'bg-primary-600 text-white'
                        : 'bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                    }`}
                  >
                    {page}
                  </button>
                ))}
                
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === pagination.total_pages}
                  className="px-3 py-2 rounded-md bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-12">
            <ClockIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No pairing history
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              You haven't been paired with anyone yet. Check back later!
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PairingHistory;