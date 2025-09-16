'use client';
import React, { useState, useEffect } from 'react';
import {
  ArrowRight,
  FileText,
  Calendar,
  BookOpen,
  Zap,
  BarChart3,
  CheckCircle,
  TrendingUp,
  Sparkles,
  Activity,
  Shield,
  Clock,
  Users,
  Globe,
  ChevronRight,
  Play,
} from 'lucide-react';

const Dashboard = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [activeCard, setActiveCard] = useState(null as number | null);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const features = [
    {
      icon: FileText,
      title: 'Smart Document Processing',
      description: 'AI-powered document analysis and parsing',
      content:
        'Advanced OCR and NLP technology automatically extracts and structures data from your financial reports, with built-in AI tag recommender to suggest optimal tags for user selection.',
      href: '/editor',
      buttonText: 'Try Smart Editor',
      gradient: 'from-blue-500 via-blue-600 to-cyan-500',
      bgGradient: 'from-blue-50 to-cyan-50',
      darkBgGradient: 'from-blue-950 to-cyan-950',
      stats: 'AI tag recommendations',
      metric: 'Smart',
      metricLabel: 'suggestions',
    },
    {
      icon: Calendar,
      title: 'Dynamic Context Engine',
      description: 'Intelligent context management with auto-suggestions',
      content:
        'Our AI suggests optimal contexts based on your data patterns and regulatory requirements, with an integrated AI chatbot to guide you through the process.',
      href: '/contexts',
      buttonText: 'Explore Contexts',
      gradient: 'from-purple-500 via-purple-600 to-pink-500',
      bgGradient: 'from-purple-50 to-pink-50',
      darkBgGradient: 'from-purple-950 to-pink-950',
      stats: 'AI chatbot included',
      metric: '24/7',
      metricLabel: 'ai support',
    },
    {
      icon: BookOpen,
      title: 'XBRL Viewer',
      description: 'Efficient exploration and analysis of XBRL data',
      content:
        'Visualize and analyze XBRL financial data with an interactive viewer. Get instant help from our AI chatbot for navigation and analysis insights.',
      href: '/xbrl-viewer',
      buttonText: 'View XBRL Data',
      gradient: 'from-emerald-500 via-emerald-600 to-teal-500',
      bgGradient: 'from-emerald-50 to-teal-50',
      darkBgGradient: 'from-emerald-950 to-teal-950',
      stats: '100+ reports supported',
      metric: 'New',
      metricLabel: 'feature',
    },
  ];

  const quickStats = [
    // {
    //   label: 'Processing Time Saved',
    //   value: '90%',
    //   icon: Clock,
    //   color: 'text-blue-600',
    // },
    {
      label: 'XBRL Viewer',
      value: 'Advanced',
      icon: CheckCircle,
      color: 'text-green-600',
    },
    {
      label: 'Taxonomy Parser',
      value: 'Universal',
      icon: CheckCircle,
      color: 'text-green-600',
    },

    {
      label: 'Built-in Tag Recommender',
      value: 'AI',
      icon: Sparkles,
      color: 'text-purple-600',
    },
    {
      label: 'Interactive AI Chatbot',
      value: '24/7',
      icon: Activity,
      color: 'text-orange-600',
    },
  ];

  return (
    <div className='min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/50'>
      {/* Hero Section */}
      <div className='relative overflow-hidden'>
        <div className='absolute inset-0 bg-gradient-to-r from-blue-600/5 to-purple-600/5 dark:from-blue-600/10 dark:to-purple-600/10'></div>
        <div className='relative container mx-auto px-6 pt-12 pb-16'>
          <div
            className={`text-center space-y-8 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}
          >
            <div className='inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 border border-blue-200/50 dark:border-blue-800/50'>
              <Sparkles className='w-4 h-4 text-blue-600 dark:text-blue-400' />
              <span className='text-sm font-medium text-blue-700 dark:text-blue-300'>
                AI-Powered XBRL Solution
              </span>
            </div>

            <h1 className='text-4xl md:text-6xl lg:text-7xl font-bold text-slate-900 dark:text-white leading-tight'>
              Everything you need for{' '}
              <span className='bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent'>
                perfect compliance
              </span>
            </h1>

            <p className='text-xl md:text-2xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed'>
              Advanced AI-powered tools designed to streamline your XBRL
              reporting workflow with unprecedented accuracy and speed
            </p>
          </div>
        </div>
      </div>

      {/* Quick Stats Bar */}
      <div className='container mx-auto px-6 -mt-8 mb-16'>
        <div
          className={`grid grid-cols-2 md:grid-cols-4 gap-4 max-w-5xl mx-auto transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}
        >
          {quickStats.map((stat, index) => (
            <div
              key={stat.label}
              className='group bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1'
              style={{ transitionDelay: `${index * 100}ms` }}
            >
              <div className='flex items-center gap-3'>
                <div className='p-2 rounded-lg bg-gradient-to-br from-slate-100 to-slate-200 dark:from-slate-700 dark:to-slate-600'>
                  <stat.icon className={`w-4 h-4 ${stat.color}`} />
                </div>
                <div className='flex-1 min-w-0'>
                  <div className='text-lg font-bold text-slate-900 dark:text-white'>
                    {stat.value}
                  </div>
                  <div className='text-xs text-slate-500 dark:text-slate-400 truncate'>
                    {stat.label}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className='container mx-auto px-6 pb-20'>
        <div className='text-center mb-12'>
          <h2 className='text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4'>
            Powerful Features
          </h2>
          <p className='text-lg text-slate-600 dark:text-slate-400'>
            Everything you need to streamline your XBRL workflow
          </p>
        </div>

        <div className='grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto'>
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className={`group relative overflow-hidden rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}
              style={{ transitionDelay: `${(index + 4) * 150}ms` }}
              onMouseEnter={() => setActiveCard(index)}
              onMouseLeave={() => setActiveCard(null)}
            >
              {/* Simple Hover Border */}
              <div
                className={`absolute inset-0 rounded-2xl transition-all duration-300 ${activeCard === index ? `bg-gradient-to-r ${feature.gradient} p-[2px]` : ''}`}
              >
                {activeCard === index && (
                  <div className='absolute inset-[2px] bg-white dark:bg-slate-800 rounded-2xl'></div>
                )}
              </div>

              {/* Card Content */}
              <div className='relative p-8 h-full flex flex-col bg-white dark:bg-slate-800 rounded-2xl'>
                {/* Header */}
                <div className='flex items-start justify-between mb-6'>
                  <div
                    className={`p-4 rounded-xl bg-gradient-to-r ${feature.gradient} shadow-lg transition-transform duration-300 ${activeCard === index ? 'scale-105' : ''}`}
                  >
                    <feature.icon className='w-7 h-7 text-white' />
                  </div>
                  <div className='text-right'>
                    <div className='text-lg font-bold text-slate-900 dark:text-white'>
                      {feature.metric}
                    </div>
                    <div className='text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide'>
                      {feature.metricLabel}
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className='flex-grow space-y-4'>
                  <div>
                    <h3 className='text-xl font-bold text-slate-900 dark:text-white mb-3'>
                      {feature.title}
                    </h3>
                    <p className='text-slate-600 dark:text-slate-400 font-medium text-sm mb-4'>
                      {feature.description}
                    </p>
                  </div>

                  <div className='inline-flex items-center gap-2 px-3 py-2 rounded-full bg-slate-100 dark:bg-slate-700 border border-slate-200 dark:border-slate-600'>
                    <Activity className='w-3 h-3 text-green-500' />
                    <span className='text-xs font-medium text-slate-700 dark:text-slate-300'>
                      {feature.stats}
                    </span>
                  </div>

                  <p className='text-slate-600 dark:text-slate-400 leading-relaxed text-sm'>
                    {feature.content}
                  </p>
                </div>

                {/* Action Button */}
                <div className='pt-6'>
                  <button
                    className={`w-full group/btn bg-gradient-to-r ${feature.gradient} hover:shadow-lg text-white rounded-lg py-3 px-4 font-semibold text-sm transition-all duration-300 flex items-center justify-center gap-2`}
                  >
                    <Play className='w-4 h-4' />
                    {feature.buttonText}
                    <ArrowRight className='w-4 h-4 group-hover/btn:translate-x-1 transition-transform duration-200' />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className='container mx-auto px-6 py-20'>
        <div className='relative overflow-hidden'>
          {/* Background Elements */}
          <div className='absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl'></div>
          <div className='absolute inset-0 bg-black/20 rounded-3xl'></div>
          <div className='absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-white/10 to-transparent rounded-full blur-3xl'></div>
          <div className='absolute bottom-0 left-0 w-96 h-96 bg-gradient-to-tr from-white/10 to-transparent rounded-full blur-3xl'></div>

          {/* Content */}
          <div className='relative text-center text-white p-12 lg:p-20 max-w-5xl mx-auto'>
            <div className='space-y-8'>
              <div className='inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 border border-white/30'>
                <Shield className='w-4 h-4' />
                <span className='text-sm font-medium'>
                  Enterprise-Ready Solution
                </span>
              </div>

              <h2 className='text-4xl md:text-5xl lg:text-6xl font-bold leading-tight'>
                Ready to streamline your
                <br />
                <span className='text-yellow-300'>XBRL reporting?</span>
              </h2>

              <p className='text-xl md:text-2xl text-blue-100 max-w-3xl mx-auto leading-relaxed'>
                Experience intelligent XBRL reporting with built-in AI tag
                recommendations and 24/7 AI chatbot assistance
              </p>

              {/* Action Buttons */}
              {/* <div className='flex flex-col sm:flex-row gap-4 justify-center pt-8'>
                <button className='group bg-white text-slate-900 hover:bg-blue-50 rounded-xl py-4 px-8 font-bold text-lg transition-all duration-300 hover:shadow-2xl hover:scale-105 flex items-center justify-center gap-2'>
                  <BarChart3 className='w-5 h-5 text-blue-600' />
                  Start Processing Documents
                  <ArrowRight className='w-5 h-5 group-hover:translate-x-1 transition-transform duration-200' />
                </button>

                <button className='group border-2 border-white/30 text-white hover:bg-white/10 rounded-xl py-4 px-8 font-bold text-lg transition-all duration-300 flex items-center justify-center gap-2'>
                  <BookOpen className='w-5 h-5' />
                  View XBRL Data
                  <ChevronRight className='w-5 h-5 group-hover:translate-x-1 transition-transform duration-200' />
                </button>
              </div> */}

              {/* Trust Indicators */}
              <div className='flex flex-wrap justify-center items-center gap-8 pt-12 text-blue-100'>
                <div className='flex items-center gap-2'>
                  <Shield className='w-5 h-5' />
                  <span className='font-medium'>Enterprise Security</span>
                </div>
                <div className='flex items-center gap-2'>
                  <CheckCircle className='w-5 h-5' />
                  <span className='font-medium'>99.9% Uptime SLA</span>
                </div>
                <div className='flex items-center gap-2'>
                  <Globe className='w-5 h-5' />
                  <span className='font-medium'>Global Compliance</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
