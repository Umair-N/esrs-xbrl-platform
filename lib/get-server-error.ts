const getErrorMessage = (err: unknown): string => {
  const axiosMsg =
    (err as any)?.response?.data?.error?.message ||
    (err as any)?.response?.data?.message;

  const fetchMsg =
    (err as any)?.data?.error?.message || (err as any)?.data?.message;

  return (
    axiosMsg || fetchMsg || (err as Error).message || 'Something went wrong'
  );
};
export default getErrorMessage;
