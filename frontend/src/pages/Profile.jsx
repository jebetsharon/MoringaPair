import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Navbar from '../components/Navbar';
import FormInput from '../components/FormInput';
import LoadingSpinner from '../components/LoadingSpinner';
import Toast from '../components/Toast';
import apiService from '../services/api';
import { UserIcon, CogIcon, AcademicCapIcon } from '@heroicons/react/24/outline';

const Profile = () => {
  const { user } = useSelector((state) => state.auth);
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('success');
  
  const [formData, setFormData] = useState({
    preferences: {
      programming_languages: '',
      learning_goals: '',
      availability: '',
    },
    skills: {
      technical_skills: '',
      experience_level: 'beginner',
      interests: '',
    },
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setIsLoading(true);
      const response = await apiService.getProfile();
      if (response.success) {
        setProfile(response.profile);
        setFormData({
          preferences: response.profile.preferences || {
            programming_languages: '',
            learning_goals: '',
            availability: '',
          },
          skills: response.profile.skills || {
            technical_skills: '',
            experience_level: 'beginner',
            interests: '',
          },
        });
      }
    } catch (error) {
      setToastMessage('Failed to load profile');
      setToastType('error');
      setShowToast(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (section, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value,
      },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setIsSaving(true);
      const response = await apiService.updateProfile(formData);
      if (response.success) {
        setToastMessage('Profile updated successfully!');
        setToastType('success');
        setShowToast(true);
        fetchProfile(); // Refresh profile data
      }
    } catch (error) {
      setToastMessage('Failed to update profile');
      setToastType('error');
      setShowToast(true);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCloseToast = () => {
    setShowToast(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navbar />
        <div className="flex justify-center items-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    );
  }

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

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-2">
            <UserIcon className="h-8 w-8 text-primary-600" />
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Profile
            </h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your preferences and skills
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* User info sidebar */}
          <div className="lg:col-span-1">
            <div className="card p-6">
              <div className="text-center">
                <div className="h-20 w-20 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <UserIcon className="h-10 w-10 text-white" />
                </div>
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {user?.full_name}
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mt-1">
                  {profile?.email || user?.email}
                </p>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-400 mt-2">
                  {user?.role}
                </span>
              </div>

              {/* Quiz results */}
              {profile?.quiz_result && (
                <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center space-x-2 mb-3">
                    <AcademicCapIcon className="h-5 w-5 text-primary-600" />
                    <h3 className="font-medium text-gray-900 dark:text-white">
                      Quiz Results
                    </h3>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Score:</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {profile.quiz_result.score}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Strength:</span>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {profile.quiz_result.strength_area}
                      </p>
                    </div>
                    <div>
                      <span className="text-gray-600 dark:text-gray-400">Improvement area:</span>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {profile.quiz_result.weakness_area}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Profile form */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Preferences section */}
              <div className="card p-6">
                <div className="flex items-center space-x-3 mb-6">
                  <CogIcon className="h-6 w-6 text-primary-600" />
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Preferences
                  </h2>
                </div>

                <div className="space-y-6">
                  <FormInput
                    label="Programming Languages"
                    type="text"
                    name="programming_languages"
                    value={formData.preferences.programming_languages}
                    onChange={(e) => handleChange('preferences', 'programming_languages', e.target.value)}
                    placeholder="e.g., JavaScript, Python, React"
                  />

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Learning Goals
                    </label>
                    <textarea
                      name="learning_goals"
                      value={formData.preferences.learning_goals}
                      onChange={(e) => handleChange('preferences', 'learning_goals', e.target.value)}
                      rows={3}
                      className="input-field"
                      placeholder="What do you want to achieve through pair programming?"
                    />
                  </div>

                  <FormInput
                    label="Availability"
                    type="text"
                    name="availability"
                    value={formData.preferences.availability}
                    onChange={(e) => handleChange('preferences', 'availability', e.target.value)}
                    placeholder="e.g., Weekdays 9-5, Evenings, Weekends"
                  />
                </div>
              </div>

              {/* Skills section */}
              <div className="card p-6">
                <div className="flex items-center space-x-3 mb-6">
                  <AcademicCapIcon className="h-6 w-6 text-primary-600" />
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                    Skills & Experience
                  </h2>
                </div>

                <div className="space-y-6">
                  <FormInput
                    label="Technical Skills"
                    type="text"
                    name="technical_skills"
                    value={formData.skills.technical_skills}
                    onChange={(e) => handleChange('skills', 'technical_skills', e.target.value)}
                    placeholder="e.g., Frontend development, API design, Database management"
                  />

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Experience Level
                    </label>
                    <select
                      name="experience_level"
                      value={formData.skills.experience_level}
                      onChange={(e) => handleChange('skills', 'experience_level', e.target.value)}
                      className="input-field"
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Interests
                    </label>
                    <textarea
                      name="interests"
                      value={formData.skills.interests}
                      onChange={(e) => handleChange('skills', 'interests', e.target.value)}
                      rows={3}
                      className="input-field"
                      placeholder="What areas of programming interest you most?"
                    />
                  </div>
                </div>
              </div>

              {/* Submit button */}
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={isSaving}
                  className="btn-primary flex items-center space-x-2 px-6 py-3"
                >
                  {isSaving ? (
                    <LoadingSpinner size="sm" />
                  ) : (
                    <span>Save Changes</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;