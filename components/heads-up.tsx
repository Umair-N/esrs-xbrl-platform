'use client';

import type React from 'react';
import { useMemo } from 'react';
import { useState, useEffect, createContext, useContext } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface NotificationProps {
  id: string;
  type?: 'success' | 'error' | 'info' | 'warning';
  title: string;
  message?: string;
  duration?: number;
  onDismiss?: (id: string) => void;
  action?: {
    label: string;
    onClick: () => void;
  };
}

const iconMap = {
  success: CheckCircle,
  error: AlertCircle,
  info: Info,
  warning: AlertTriangle,
};

const colorMap = {
  success:
    'bg-green-50 border-green-200 text-green-800 dark:bg-green-950 dark:border-green-800 dark:text-green-200',
  error:
    'bg-red-50 border-red-200 text-red-800 dark:bg-red-950 dark:border-red-800 dark:text-red-200',
  info: 'bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200',
  warning:
    'bg-yellow-50 border-yellow-200 text-yellow-800 dark:bg-yellow-950 dark:border-yellow-800 dark:text-yellow-200',
};

const iconColorMap = {
  success: 'text-green-500 dark:text-green-400',
  error: 'text-red-500 dark:text-red-400',
  info: 'text-blue-500 dark:text-blue-400',
  warning: 'text-yellow-500 dark:text-yellow-400',
};

export function HeadsUpNotification({
  id,
  type = 'info',
  title,
  message,
  duration = 5000,
  onDismiss,
  action,
}: NotificationProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);

  const Icon = iconMap[type];

  useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 50);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        handleDismiss();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration]);

  const handleDismiss = () => {
    setIsLeaving(true);
    setTimeout(() => {
      onDismiss?.(id);
    }, 300);
  };

  return (
    <div
      className={cn(
        'fixed top-4 left-4 right-4 z-50 mx-auto max-w-sm',
        'transform transition-all duration-300 ease-out',
        isVisible && !isLeaving
          ? 'translate-y-0 opacity-100'
          : '-translate-y-full opacity-0'
      )}
    >
      <div
        className={cn(
          'rounded-lg border p-4 shadow-lg backdrop-blur-sm',
          'animate-in slide-in-from-top-2',
          colorMap[type]
        )}
      >
        <div className='flex items-start gap-3'>
          <Icon
            className={cn('h-5 w-5 flex-shrink-0 mt-0.5', iconColorMap[type])}
          />

          <div className='flex-1 min-w-0'>
            <h4 className='font-medium text-sm leading-5'>{title}</h4>
            {message && (
              <p className='mt-1 text-sm opacity-90 leading-5'>{message}</p>
            )}

            {action && (
              <button
                onClick={action.onClick}
                className='mt-2 text-sm font-medium underline hover:no-underline focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-current rounded'
              >
                {action.label}
              </button>
            )}
          </div>

          <button
            onClick={handleDismiss}
            className='flex-shrink-0 p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-current transition-colors'
            aria-label='Dismiss notification'
          >
            <X className='h-4 w-4' />
          </button>
        </div>
      </div>
    </div>
  );
}

interface NotificationContextType {
  notifications: NotificationProps[];
  addNotification: (notification: Omit<NotificationProps, 'id'>) => string;
  removeNotification: (id: string) => void;
  clearAll: () => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(
  undefined
);

class NotificationManager {
  private contextRef: NotificationContextType | null = null;

  setContext(context: NotificationContextType) {
    this.contextRef = context;
  }

  private ensureContext() {
    if (!this.contextRef) {
      throw new Error(
        'Notification system not initialized. Make sure NotificationProvider is mounted.'
      );
    }
    return this.contextRef;
  }

  show(notification: Omit<NotificationProps, 'id'>) {
    return this.ensureContext().addNotification(notification);
  }

  success(notification: Omit<NotificationProps, 'id' | 'type'>) {
    return this.show({ type: 'success', ...notification });
  }

  error(notification: Omit<NotificationProps, 'id' | 'type'>) {
    return this.show({ type: 'error', ...notification });
  }

  info(notification: Omit<NotificationProps, 'id' | 'type'>) {
    return this.show({ type: 'info', ...notification });
  }

  warning(notification: Omit<NotificationProps, 'id' | 'type'>) {
    return this.show({ type: 'warning', ...notification });
  }

  dismiss(id: string) {
    this.ensureContext().removeNotification(id);
  }

  clear() {
    this.ensureContext().clearAll();
  }
}

// Global instance
const notificationManager = new NotificationManager();

// Export convenience functions for non-React usage
export const showNotification = (notification: Omit<NotificationProps, 'id'>) =>
  notificationManager.show(notification);
export const showSuccess = (
  notification: Omit<NotificationProps, 'id' | 'type'>
) => notificationManager.success(notification);
export const showError = (
  notification: Omit<NotificationProps, 'id' | 'type'>
) => notificationManager.error(notification);
export const showInfo = (
  notification: Omit<NotificationProps, 'id' | 'type'>
) => notificationManager.info(notification);
export const showWarning = (
  notification: Omit<NotificationProps, 'id' | 'type'>
) => notificationManager.warning(notification);
export const dismissNotification = (id: string) =>
  notificationManager.dismiss(id);
export const clearAllNotifications = () => notificationManager.clear();

export function NotificationProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [notifications, setNotifications] = useState<NotificationProps[]>([]);

  const addNotification = (notification: Omit<NotificationProps, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    setNotifications((prev) => [...prev, { ...notification, id }]);
    return id;
  };

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const clearAll = () => {
    setNotifications([]);
  };

  const contextValue = useMemo(
    () => ({
      notifications,
      addNotification,
      removeNotification,
      clearAll,
    }),
    [notifications]
  );

  useEffect(() => {
    notificationManager.setContext(contextValue);
  }, [contextValue]);

  return (
    <NotificationContext.Provider value={contextValue}>
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotifications() {
  const context = useContext(NotificationContext);
  if (context === undefined) {
    throw new Error(
      'useNotifications must be used within a NotificationProvider'
    );
  }
  return context;
}

export function NotificationContainer() {
  const { notifications, removeNotification } = useNotifications();

  return (
    <>
      {notifications.map((notification) => (
        <HeadsUpNotification
          key={notification.id}
          {...notification}
          onDismiss={removeNotification}
        />
      ))}
    </>
  );
}
