'use client';

import type React from 'react';
import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
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
  Copy,
  Check,
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

// Custom markdown components
const MarkdownComponents = {
  code({ node, inline, className, children, ...props }: any) {
    const match = /language-(\w+)/.exec(className || '');
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
      await navigator.clipboard.writeText(String(children));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    };

    return !inline && match ? (
      <div className='relative group'>
        <button
          onClick={handleCopy}
          className='absolute right-2 top-2 p-1.5 rounded bg-gray-700 hover:bg-gray-600 opacity-0 group-hover:opacity-100 transition-opacity z-10'
          title='Copy code'
        >
          {copied ? (
            <Check className='w-3 h-3 text-green-400' />
          ) : (
            <Copy className='w-3 h-3 text-gray-300' />
          )}
        </button>
        <SyntaxHighlighter
          style={oneDark}
          language={match[1]}
          PreTag='div'
          className='text-sm rounded-md'
          {...props}
        >
          {String(children).replace(/\n$/, '')}
        </SyntaxHighlighter>
      </div>
    ) : (
      <code
        className='bg-muted px-1.5 py-0.5 rounded text-sm font-mono'
        {...props}
      >
        {children}
      </code>
    );
  },
  h1: ({ children }: any) => (
    <h1 className='mb-2 text-xl font-bold text-foreground'>{children}</h1>
  ),
  h2: ({ children }: any) => (
    <h2 className='mb-2 text-lg font-semibold text-foreground'>{children}</h2>
  ),
  h3: ({ children }: any) => (
    <h3 className='mb-1 text-base font-semibold text-foreground'>{children}</h3>
  ),
  p: ({ children }: any) => (
    <p className='mb-2 leading-relaxed text-foreground'>{children}</p>
  ),
  ul: ({ children }: any) => (
    <ul className='mb-2 space-y-1 list-disc list-inside text-foreground'>
      {children}
    </ul>
  ),
  ol: ({ children }: any) => (
    <ol className='mb-2 space-y-1 list-decimal list-inside text-foreground'>
      {children}
    </ol>
  ),
  li: ({ children }: any) => <li className='text-foreground'>{children}</li>,
  blockquote: ({ children }: any) => (
    <blockquote className='pl-4 my-2 italic border-l-4 border-primary text-muted-foreground'>
      {children}
    </blockquote>
  ),
  table: ({ children }: any) => (
    <div className='my-2 overflow-x-auto'>
      <table className='min-w-full border border-collapse border-border'>
        {children}
      </table>
    </div>
  ),
  th: ({ children }: any) => (
    <th className='px-2 py-1 font-semibold text-left border border-border bg-muted'>
      {children}
    </th>
  ),
  td: ({ children }: any) => (
    <td className='px-2 py-1 border border-border'>{children}</td>
  ),
  a: ({ children, href }: any) => (
    <a
      href={href}
      className='underline text-primary hover:text-primary/80'
      target='_blank'
      rel='noopener noreferrer'
    >
      {children}
    </a>
  ),
  strong: ({ children }: any) => (
    <strong className='font-semibold text-foreground'>{children}</strong>
  ),
  em: ({ children }: any) => (
    <em className='italic text-foreground'>{children}</em>
  ),
};

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
          className='fixed transition-all duration-200 rounded-full shadow-lg bottom-6 right-6 h-14 w-14 hover:shadow-xl bg-primary hover:bg-primary/90'
          size='icon'
        >
          <MessageCircle className='w-6 h-6' />
        </Button>
      )}

      {isOpen && (
        <Card className='fixed z-[51] bottom-6 right-6 w-96 h-[600px] shadow-2xl border-2 flex flex-col overflow-hidden'>
          <div className='flex items-center justify-between p-4 bg-primary text-primary-foreground'>
            <div className='flex items-center gap-3'>
              <Avatar className='w-8 h-8 bg-primary-foreground/20'>
                <AvatarFallback className='font-bold bg-transparent text-primary-foreground'>
                  B
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className='font-semibold'>BriskAI</h3>
                <p className='flex items-center gap-1 text-xs opacity-90'>
                  <Leaf className='w-3 h-3' />
                  ESG Expert
                </p>
              </div>
            </div>
            <div className='flex items-center gap-2'>
              <Button
                variant='ghost'
                size='icon'
                onClick={() => setShowSessions(!showSessions)}
                className='w-8 h-8 text-primary-foreground hover:bg-primary-foreground/20'
              >
                <History className='w-4 h-4' />
              </Button>
              <Button
                variant='ghost'
                size='icon'
                onClick={() => setIsOpen(false)}
                className='w-8 h-8 text-primary-foreground hover:bg-primary-foreground/20'
              >
                <X className='w-4 h-4' />
              </Button>
            </div>
          </div>

          {showSessions && (
            <div className='p-3 overflow-y-auto border-b bg-muted/50 max-h-48'>
              <div className='flex items-center justify-between mb-3'>
                <h4 className='text-sm font-medium'>Chat History</h4>
                <Button
                  variant='outline'
                  size='sm'
                  onClick={createNewSession}
                  className='px-2 text-xs bg-transparent h-7'
                >
                  <Plus className='w-3 h-3 mr-1' />
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
                      <p className='truncate text-muted-foreground'>
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
                      className='w-6 h-6 opacity-0 group-hover:opacity-100 hover:bg-destructive hover:text-destructive-foreground'
                    >
                      <Trash2 className='w-3 h-3' />
                    </Button>
                  </div>
                ))}
                {sessions.length === 0 && (
                  <p className='py-4 text-xs text-center text-muted-foreground'>
                    No previous chats
                  </p>
                )}
              </div>
            </div>
          )}

          <div className='flex-1 p-4 space-y-3 overflow-y-auto'>
            {!currentSession && (
              <div className='py-8 text-center'>
                <div className='flex items-center justify-center w-12 h-12 mx-auto mb-3 rounded-full bg-primary/10'>
                  <Leaf className='w-6 h-6 text-primary' />
                </div>
                <h4 className='mb-2 font-semibold'>
                  Welcome to BriskAI's ESG Hub
                </h4>
                <p className='mb-4 text-sm text-muted-foreground'>
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
                    'h-6 w-6 flex-shrink-0 mt-1',
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
                    'rounded-lg p-3 max-w-[85%] min-w-0',
                    message.isUser
                      ? 'bg-accent text-accent-foreground'
                      : 'bg-muted'
                  )}
                >
                  {message.isUser ? (
                    <p className='leading-relaxed whitespace-pre-wrap'>
                      {message.text}
                    </p>
                  ) : (
                    <div className='prose-sm prose max-w-none'>
                      <ReactMarkdown
                        components={MarkdownComponents}
                        remarkPlugins={[remarkGfm]}
                      >
                        {message.text}
                      </ReactMarkdown>
                    </div>
                  )}
                  <time className='block mt-2 text-xs opacity-70'>
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
                <Avatar className='w-6 h-6 mt-1 bg-primary'>
                  <AvatarFallback className='text-xs bg-primary text-primary-foreground'>
                    B
                  </AvatarFallback>
                </Avatar>
                <div className='p-3 rounded-lg bg-muted'>
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
            <div className='p-3 border-t'>
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
                  <Send className='w-4 h-4' />
                </Button>
              </div>
            </div>
          )}
        </Card>
      )}
    </>
  );
}
