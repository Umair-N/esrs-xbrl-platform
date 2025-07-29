"use client";
import ProtectedRoute from "@/components/protectedRoute";
import Dashboard from "@/components/dashboard";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <Dashboard />
      </div>
    </ProtectedRoute>
  );
}
