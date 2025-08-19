import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function generateUniqueId(): string {
  return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
}

export const getInitials = (fullName?: string, username?: string): string => {
  if (fullName) {
    return fullName
      .split(' ').splice(0, 2)
      .map((n: string) => n[0])
      .join('')
      .toUpperCase();
  }
  return username?.slice(0, 2).toUpperCase() || 'U';
};