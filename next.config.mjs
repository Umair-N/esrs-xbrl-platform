/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // Disable ESLint during production builds
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Optionally also ignore TypeScript errors during builds
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
