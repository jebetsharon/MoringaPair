import { UserIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';

const RoleSelector = ({ selectedRole, onRoleSelect, error }) => {
  const roles = [
    {
      id: 'student',
      title: 'Student',
      description: 'Join pairing sessions and collaborate with peers',
      icon: UserIcon,
      color: 'primary',
    },
    {
      id: 'admin',
      title: 'Admin',
      description: 'Manage pairings and oversee the platform',
      icon: ShieldCheckIcon,
      color: 'purple',
    },
  ];

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
        Select your role <span className="text-red-500">*</span>
      </label>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {roles.map((role) => {
          const Icon = role.icon;
          const isSelected = selectedRole === role.id;
          
          return (
            <button
              key={role.id}
              type="button"
              onClick={() => onRoleSelect(role.id)}
              className={`p-4 rounded-lg border-2 transition-all duration-200 text-left hover:shadow-md ${
                isSelected
                  ? role.color === 'primary'
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : 'border-purple-500 bg-purple-50 dark:bg-purple-900/20'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
              } ${error ? 'border-red-500' : ''}`}
            >
              <div className="flex items-start space-x-3">
                <Icon
                  className={`h-6 w-6 mt-0.5 ${
                    isSelected
                      ? role.color === 'primary'
                        ? 'text-primary-600'
                        : 'text-purple-600'
                      : 'text-gray-400'
                  }`}
                />
                <div>
                  <h3
                    className={`font-medium ${
                      isSelected
                        ? role.color === 'primary'
                          ? 'text-primary-900 dark:text-primary-100'
                          : 'text-purple-900 dark:text-purple-100'
                        : 'text-gray-900 dark:text-gray-100'
                    }`}
                  >
                    {role.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {role.description}
                  </p>
                </div>
              </div>
            </button>
          );
        })}
      </div>
      
      {error && (
        <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
      )}
    </div>
  );
};

export default RoleSelector;