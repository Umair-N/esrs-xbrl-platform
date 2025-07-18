import { useState, useEffect } from "react";
import { useAuth } from "../hooks/useAuth";
import AuthService from "../lib/auth";
import { User, ProtectedResponse } from "../types/auth";

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [protectedData, setProtectedData] = useState<ProtectedResponse | null>(
    null
  );
  const [adminData, setAdminData] = useState<ProtectedResponse | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async (): Promise<void> => {
    try {
      setLoading(true);

      // Fetch protected data
      const protectedResponse = await AuthService.getProtectedData();
      setProtectedData(protectedResponse);

      // Try to fetch admin data if user is admin
      if (user?.role === "admin") {
        try {
          const adminResponse = await AuthService.getAdminData();
          setAdminData(adminResponse);

          const usersResponse = await AuthService.getAllUsers();
          setUsers(usersResponse);
        } catch (adminError) {
          console.log(
            "Admin data not accessible:",
            (adminError as Error).message
          );
        }
      }
    } catch (error) {
      setError("Failed to fetch data: " + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async (): Promise<void> => {
    await logout();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
            <p className="text-gray-600">
              Welcome back, {user?.full_name || user?.username}!
            </p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
          >
            Logout
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* User Info */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">User Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p>
              <strong>Email:</strong> {user?.email}
            </p>
            <p>
              <strong>Username:</strong> {user?.username}
            </p>
            <p>
              <strong>Full Name:</strong> {user?.full_name || "Not provided"}
            </p>
          </div>
          <div>
            <p>
              <strong>Role:</strong>{" "}
              <span className="capitalize">{user?.role}</span>
            </p>
            <p>
              <strong>Status:</strong> {user?.is_active ? "Active" : "Inactive"}
            </p>
            <p>
              <strong>Verified:</strong> {user?.is_verified ? "Yes" : "No"}
            </p>
          </div>
        </div>
      </div>

      {/* Protected Data */}
      {protectedData && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4">Protected Content</h2>
          <div className="p-4 bg-green-50 border border-green-200 rounded">
            <p className="text-green-800">{protectedData.message}</p>
          </div>
        </div>
      )}

      {/* Admin Section */}
      {user?.role === "admin" && (
        <div className="space-y-6">
          {adminData && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-4">Admin Content</h2>
              <div className="p-4 bg-blue-50 border border-blue-200 rounded">
                <p className="text-blue-800">{adminData.message}</p>
              </div>
            </div>
          )}

          {users.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-4">All Users</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full table-auto">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-2 text-left">ID</th>
                      <th className="px-4 py-2 text-left">Username</th>
                      <th className="px-4 py-2 text-left">Email</th>
                      <th className="px-4 py-2 text-left">Role</th>
                      <th className="px-4 py-2 text-left">Status</th>
                      <th className="px-4 py-2 text-left">Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((userItem) => (
                      <tr key={userItem.id} className="border-b">
                        <td className="px-4 py-2">{userItem.id}</td>
                        <td className="px-4 py-2">{userItem.username}</td>
                        <td className="px-4 py-2">{userItem.email}</td>
                        <td className="px-4 py-2">
                          <span className="capitalize">{userItem.role}</span>
                        </td>
                        <td className="px-4 py-2">
                          <span
                            className={`px-2 py-1 rounded text-xs ${
                              userItem.is_active
                                ? "bg-green-100 text-green-800"
                                : "bg-red-100 text-red-800"
                            }`}
                          >
                            {userItem.is_active ? "Active" : "Inactive"}
                          </span>
                        </td>
                        <td className="px-4 py-2">
                          {new Date(userItem.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
