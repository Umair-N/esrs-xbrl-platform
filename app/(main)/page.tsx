'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import {
  ArrowRight,
  FileText,
  Tag,
  Calendar,
  BookOpen,
  FileCode,
  Users,
  Zap,
  TrendingUp,
  Award,
  CheckCircle,
  Globe,
  Lock,
  BarChart3,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import ProtectedRoute from '@/components/protectedRoute';
import { useState, useEffect } from 'react';

export default function Home() {
  // const { isAuthenticated } = useAuth();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const features = [
    {
      icon: FileText,
      title: 'Smart Document Processing',
      description: 'AI-powered document analysis and parsing',
      content:
        'Advanced OCR and NLP technology automatically extracts and structures data from your financial reports, reducing manual work by 90%.',
      href: '/editor',
      buttonText: 'Try Smart Editor',
      gradient: 'from-blue-500 to-cyan-500',
      delay: 'delay-100',
      stats: '90% faster processing',
    },
    {
      icon: Calendar,
      title: 'Dynamic Context Engine',
      description: 'Intelligent context management with auto-suggestions',
      content:
        'Our AI suggests optimal contexts based on your data patterns and regulatory requirements, ensuring compliance accuracy.',
      href: '/contexts',
      buttonText: 'Explore Contexts',
      gradient: 'from-purple-500 to-pink-500',
      delay: 'delay-200',
      stats: '99.9% accuracy rate',
    },
    {
      icon: BookOpen,
      title: 'Interactive Taxonomy Explorer',
      description: 'Visual taxonomy navigation with semantic search',
      content:
        'Navigate complex taxonomy with our interactive visual interface. Find concepts instantly with semantic AI search.',
      href: '/taxonomy',
      buttonText: 'Explore Taxonomy',
      gradient: 'from-green-500 to-emerald-500',
      delay: 'delay-300',
      stats: '10,000+ concepts indexed',
    },
    {
      icon: Tag,
      title: 'Intelligent Auto-Tagging',
      description: 'ML-powered automatic concept detection',
      content:
        'Machine learning algorithms automatically suggest and apply XBRL tags based on content analysis and historical patterns.',
      href: '/editor',
      buttonText: 'Start Auto-Tagging',
      gradient: 'from-orange-500 to-red-500',
      delay: 'delay-400',
      stats: '85% auto-tag accuracy',
    },
    {
      icon: FileCode,
      title: 'Real-time XBRL Validation',
      description: 'Live validation with instant feedback',
      content:
        'Real-time validation engine checks compliance as you work, with detailed error reporting and suggested fixes.',
      href: '/xbrl-preview',
      buttonText: 'Validate Now',
      gradient: 'from-indigo-500 to-purple-500',
      delay: 'delay-500',
      stats: 'Real-time validation',
    },
    {
      icon: Users,
      title: 'Enterprise Collaboration',
      description: 'Team workflows with advanced permissions',
      content:
        'Sophisticated role-based access control, audit trails, and collaborative workflows for enterprise teams.',
      href: '/users',
      buttonText: 'Manage Teams',
      gradient: 'from-teal-500 to-cyan-500',
      delay: 'delay-600',
      stats: 'Enterprise-grade security',
    },
  ];

  return (
    <ProtectedRoute>
      <div className='min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950'>
        {/* Features Section - Fixed Layout */}
        <div className='container mx-auto px-6 py-16'>
          <div className='text-center mb-16'>
            <h2 className='text-3xl md:text-5xl font-bold text-slate-900 dark:text-white mb-4'>
              Everything you need for{' '}
              <span className='bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent'>
                perfect compliance
              </span>
            </h2>
            <p className='text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto'>
              Advanced AI-powered tools designed to simplify your reporting
              workflow
            </p>
          </div>

          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto'>
            {features.map((feature) => (
              <Card
                key={feature.title}
                className={`group bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-slate-200/50 dark:border-slate-700/50 hover:border-blue-200 dark:hover:border-blue-700 transition-all duration-100 hover:shadow-lg animate-in fade-in-0  ${feature.delay} flex flex-col h-full`}
              >
                <CardHeader className='pb-4 flex-shrink-0'>
                  <div
                    className={`inline-flex p-3 rounded-lg bg-gradient-to-r ${feature.gradient} mb-4 w-fit`}
                  >
                    <feature.icon className='h-6 w-6 text-white' />
                  </div>
                  <div className='space-y-2'>
                    <CardTitle className='text-lg font-semibold text-slate-900 dark:text-white'>
                      {feature.title}
                    </CardTitle>
                    <CardDescription className='text-slate-600 dark:text-slate-400'>
                      {feature.description}
                    </CardDescription>
                    <Badge variant='secondary' className='text-xs w-fit'>
                      {feature.stats}
                    </Badge>
                  </div>
                </CardHeader>

                <CardContent className='pb-6 flex-grow'>
                  <p className='text-slate-600 dark:text-slate-400 leading-relaxed text-sm'>
                    {feature.content}
                  </p>
                </CardContent>

                <CardFooter className='pt-0 mt-auto flex-shrink-0'>
                  <Button
                    asChild
                    variant='outline'
                    className='w-full group/btn hover:bg-slate-50 dark:hover:bg-slate-700'
                  >
                    <Link
                      href={feature.href}
                      className='flex items-center justify-center gap-2'
                    >
                      {feature.buttonText}
                      <ArrowRight className='w-4 h-4 group-hover/btn:translate-x-1 transition-transform duration-200' />
                    </Link>
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>

        {/* CTA Section - Simplified */}
        <div className='container mx-auto px-6 py-16'>
          <div className='bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-center text-white max-w-4xl mx-auto'>
            <div className='space-y-6'>
              <h2 className='text-3xl md:text-4xl font-bold'>
                Ready to streamline your XBRL reporting?
              </h2>

              <p className='text-xl text-blue-100 max-w-2xl mx-auto'>
                Join 500+ enterprises who've reduced XBRL preparation time by
                90% while achieving 99.9% accuracy.
              </p>

              <div className='flex flex-col sm:flex-row gap-4 justify-center pt-4'>
                <Button
                  size='lg'
                  asChild
                  className='bg-white text-blue-600 hover:bg-blue-50 hover:text-blue-700 font-semibold'
                >
                  {/* <Link
                    href={isAuthenticated ? "/editor" : "/register"}
                    className="flex items-center gap-2"
                  >
                    {isAuthenticated ? (
                      <>
                        <BarChart3 className="w-5 h-5" />
                        Start Tagging Now
                      </>
                    ) : (
                      <>
                        <Zap className="w-5 h-5" />
                        Start Free Trial
                      </>
                    )}
                    <ArrowRight className="w-4 h-4" />
                  </Link> */}
                </Button>

                <Button
                  size='lg'
                  variant='outline'
                  asChild
                  className='border-white/30 text-black hover:bg-white/10 hover:border-white/50'
                >
                  <Link href='/taxonomy' className='flex items-center gap-2'>
                    <BookOpen className='w-5 h-5' />
                    Explore Features
                  </Link>
                </Button>
              </div>

              <div className='flex justify-center items-center gap-6 pt-6 text-blue-100 text-sm'>
                <div className='flex items-center gap-2'>
                  <Lock className='w-4 h-4' />
                  <span>Enterprise Security</span>
                </div>
                <div className='flex items-center gap-2'>
                  <CheckCircle className='w-4 h-4' />
                  <span>99.9% Uptime</span>
                </div>
                <div className='flex items-center gap-2'>
                  <Award className='w-4 h-4' />
                  <span>SOC 2 Compliant</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
