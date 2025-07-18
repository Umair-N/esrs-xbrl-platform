import Link from "next/link";

export default function Unauthorized() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">403</h1>
        <p className="text-gray-600 mb-4">
          You don't have permission to access this page.
        </p>
        <Link href="/" className="text-blue-600 hover:text-blue-800">
          Go back to home
        </Link>
      </div>
    </div>
  );
}
