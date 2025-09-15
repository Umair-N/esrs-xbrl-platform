'use client';

import type React from 'react';
import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import {
  Send,
  Trash2,
  Leaf,
  MessageCircle,
  X,
  History,
  Plus,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useGenerateChatbot } from '@/features/recommender/api/generate-chatbot';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

interface ChatSession {
  id: string;
  name: string;
  lastMessage: string;
  timestamp: Date;
  messages: Message[];
}

export function BriskyAIBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [showSessions, setShowSessions] = useState(false);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(
    null
  );
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { mutate: chatMutate, isPending: isLoading } = useGenerateChatbot({
    mutationConfig: {
      onSuccess: (data, variables) => {
        console.log('[v0] Chat response received:', data);

        // Create bot message from successful response
        const botMessage: Message = {
          id: `bot_${Date.now()}`,
          text: data?.text || 'Sorry, I received an empty response.',
          isUser: false,
          timestamp: new Date(),
        };

        // Update session with bot response
        setCurrentSession((prevSession) => {
          if (!prevSession) return null;

          const updatedSession = {
            ...prevSession,
            messages: [...prevSession.messages, botMessage],
            lastMessage:
              (data?.text?.substring(0, 50) || 'No response') + '...',
            timestamp: new Date(),
          };

          // Update sessions list
          setSessions((prev) =>
            prev.map((s) => (s.id === prevSession.id ? updatedSession : s))
          );

          return updatedSession;
        });
      },
      onError: (error) => {
        console.error('[v0] Chat mutation error:', error);

        // Create error message
        const errorMessage: Message = {
          id: `error_${Date.now()}`,
          text: 'Sorry, I encountered an error. Please try again.',
          isUser: false,
          timestamp: new Date(),
        };

        // Update session with error message
        setCurrentSession((prevSession) => {
          if (!prevSession) return null;

          const updatedSession = {
            ...prevSession,
            messages: [...prevSession.messages, errorMessage],
          };

          setSessions((prev) =>
            prev.map((s) => (s.id === prevSession.id ? updatedSession : s))
          );

          return updatedSession;
        });
      },
    },
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentSession?.messages]);

  // Load sessions from localStorage on mount
  useEffect(() => {
    const savedSessions = localStorage.getItem('esg-chat-sessions');
    if (savedSessions) {
      const parsedSessions = JSON.parse(savedSessions).map((session: any) => ({
        ...session,
        timestamp: new Date(session.timestamp),
        messages: session.messages.map((msg: any) => ({
          ...msg,
          timestamp: new Date(msg.timestamp),
        })),
      }));
      setSessions(parsedSessions);
    }
  }, []);

  // Save sessions to localStorage whenever sessions change
  useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem('esg-chat-sessions', JSON.stringify(sessions));
    }
  }, [sessions]);

  const createNewSession = () => {
    const newSession: ChatSession = {
      id: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: `Chat ${sessions.length + 1}`,
      lastMessage: '',
      timestamp: new Date(),
      messages: [],
    };
    setSessions((prev) => [newSession, ...prev]);
    setCurrentSession(newSession);
    setShowSessions(false);
  };

  const selectSession = (session: ChatSession) => {
    setCurrentSession(session);
    setShowSessions(false);
  };

  const deleteSession = async (sessionId: string) => {
    fetch(`/chatbot/clear/${sessionId}`, {
      method: 'DELETE',
    }).catch((error) => {
      console.error('[v0] Error deleting session:', error);
    });

    setSessions((prev) => prev.filter((s) => s.id !== sessionId));
    if (currentSession?.id === sessionId) {
      setCurrentSession(null);
    }
  };

  const sendMessage = () => {
    if (!input.trim() || isLoading) return;

    if (!currentSession) {
      createNewSession();
      return;
    }

    const userMessage: Message = {
      id: `user_${Date.now()}`,
      text: input.trim(),
      isUser: true,
      timestamp: new Date(),
    };

    const updatedSession = {
      ...currentSession,
      messages: [...currentSession.messages, userMessage],
      lastMessage: input.trim(),
      timestamp: new Date(),
    };

    setCurrentSession(updatedSession);
    setSessions((prev) =>
      prev.map((s) => (s.id === currentSession.id ? updatedSession : s))
    );

    const messageToSend = input.trim();
    setInput('');

    chatMutate({
      prompt: messageToSend,
      session_id: currentSession.id,
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {!isOpen && (
        <Button
          onClick={() => setIsOpen(true)}
          className='fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 bg-primary hover:bg-primary/90'
          size='icon'
        >
          <MessageCircle className='h-6 w-6' />
        </Button>
      )}

      {isOpen && (
        <Card className='fixed bottom-6 right-6 w-96 h-[600px] shadow-2xl border-2 flex flex-col overflow-hidden'>
          <div className='bg-primary text-primary-foreground p-4 flex items-center justify-between'>
            <div className='flex items-center gap-3'>
              <Avatar className='h-8 w-8 bg-primary-foreground/20'>
                <AvatarFallback className='bg-transparent text-primary-foreground font-bold'>
                  B
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className='font-semibold'>BriskAI</h3>
                <p className='text-xs opacity-90 flex items-center gap-1'>
                  <Leaf className='h-3 w-3' />
                  ESG Expert
                </p>
              </div>
            </div>
            <div className='flex items-center gap-2'>
              <Button
                variant='ghost'
                size='icon'
                onClick={() => setShowSessions(!showSessions)}
                className='h-8 w-8 text-primary-foreground hover:bg-primary-foreground/20'
              >
                <History className='h-4 w-4' />
              </Button>
              <Button
                variant='ghost'
                size='icon'
                onClick={() => setIsOpen(false)}
                className='h-8 w-8 text-primary-foreground hover:bg-primary-foreground/20'
              >
                <X className='h-4 w-4' />
              </Button>
            </div>
          </div>

          {showSessions && (
            <div className='border-b bg-muted/50 p-3 max-h-48 overflow-y-auto'>
              <div className='flex items-center justify-between mb-3'>
                <h4 className='font-medium text-sm'>Chat History</h4>
                <Button
                  variant='outline'
                  size='sm'
                  onClick={createNewSession}
                  className='h-7 px-2 text-xs bg-transparent'
                >
                  <Plus className='h-3 w-3 mr-1' />
                  New
                </Button>
              </div>
              <div className='space-y-2'>
                {sessions.map((session) => (
                  <div
                    key={session.id}
                    className={cn(
                      'p-2 rounded cursor-pointer hover:bg-accent text-xs group flex items-center justify-between',
                      currentSession?.id === session.id && 'bg-accent'
                    )}
                    onClick={() => selectSession(session)}
                  >
                    <div className='flex-1 min-w-0'>
                      <p className='font-medium truncate'>{session.name}</p>
                      <p className='text-muted-foreground truncate'>
                        {session.lastMessage || 'New chat'}
                      </p>
                    </div>
                    <Button
                      variant='ghost'
                      size='icon'
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteSession(session.id);
                      }}
                      className='h-6 w-6 opacity-0 group-hover:opacity-100 hover:bg-destructive hover:text-destructive-foreground'
                    >
                      <Trash2 className='h-3 w-3' />
                    </Button>
                  </div>
                ))}
                {sessions.length === 0 && (
                  <p className='text-muted-foreground text-xs text-center py-4'>
                    No previous chats
                  </p>
                )}
              </div>
            </div>
          )}

          <div className='flex-1 overflow-y-auto p-4 space-y-3'>
            {!currentSession && (
              <div className='text-center py-8'>
                <div className='bg-primary/10 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3'>
                  <Leaf className='h-6 w-6 text-primary' />
                </div>
                <h4 className='font-semibold mb-2'>
                  Welcome to BriskAI's ESG Hub
                </h4>
                <p className='text-muted-foreground text-sm mb-4'>
                  I'm here to help with ESG reporting, ESRS, BRSR, and XBRL
                  tagging.
                </p>
                <Button onClick={createNewSession} size='sm'>
                  Start New Chat
                </Button>
              </div>
            )}

            {currentSession?.messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  'flex gap-2 text-sm',
                  message.isUser ? 'flex-row-reverse' : ''
                )}
              >
                <Avatar
                  className={cn(
                    'h-6 w-6 flex-shrink-0',
                    message.isUser ? 'bg-accent' : 'bg-primary'
                  )}
                >
                  <AvatarFallback
                    className={cn(
                      'text-xs',
                      message.isUser
                        ? 'bg-accent text-accent-foreground'
                        : 'bg-primary text-primary-foreground'
                    )}
                  >
                    {message.isUser ? 'U' : 'B'}
                  </AvatarFallback>
                </Avatar>
                <div
                  className={cn(
                    'rounded-lg p-3 max-w-[80%]',
                    message.isUser
                      ? 'bg-accent text-accent-foreground'
                      : 'bg-muted'
                  )}
                >
                  <p className='leading-relaxed whitespace-pre-wrap'>
                    {message.text}
                  </p>
                  <time className='text-xs opacity-70 mt-1 block'>
                    {message.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </time>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className='flex gap-2 text-sm'>
                <Avatar className='h-6 w-6 bg-primary'>
                  <AvatarFallback className='bg-primary text-primary-foreground text-xs'>
                    B
                  </AvatarFallback>
                </Avatar>
                <div className='rounded-lg p-3 bg-muted'>
                  <div className='flex items-center gap-2'>
                    <div className='flex gap-1'>
                      <div className='w-1.5 h-1.5 bg-primary rounded-full animate-bounce' />
                      <div
                        className='w-1.5 h-1.5 bg-primary rounded-full animate-bounce'
                        style={{ animationDelay: '0.1s' }}
                      />
                      <div
                        className='w-1.5 h-1.5 bg-primary rounded-full animate-bounce'
                        style={{ animationDelay: '0.2s' }}
                      />
                    </div>
                    <span className='text-xs text-muted-foreground'>
                      Thinking...
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {currentSession && (
            <div className='border-t p-3'>
              <div className='flex gap-2'>
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder='Ask about ESG reporting...'
                  className='flex-1 text-sm'
                  disabled={isLoading}
                />
                <Button
                  onClick={sendMessage}
                  disabled={!input.trim() || isLoading}
                  size='icon'
                  className='h-9 w-9'
                >
                  <Send className='h-4 w-4' />
                </Button>
              </div>
            </div>
          )}
        </Card>
      )}
    </>
  );
}
