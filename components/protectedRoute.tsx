export default function ProtectedRoute ({ children }:{children: React.ReactNode})  {
  console.log('protected route');
  
  return <>{children}</>;
};
