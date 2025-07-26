"use client"
import Link from "next/link"
import { useAuth } from "@/hooks/useAuth"
import { ArrowRight, FileText, Tag, Calendar, BookOpen, FileCode, Users, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import ProtectedRoute from "@/components/protectedRoute"

export default function Home() {
  const { user, isAuthenticated, logout } = useAuth()

  const handleLogout = async () => {
    try {
      await logout()
      // Optionally redirect or trigger a toast
    } catch (error) {
      console.error("Logout failed:", error)
    }
  }

  return (
    <ProtectedRoute>
      <div className="container mx-auto py-10 space-y-8">
        {/* Header Section */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight animate-in fade-in-0 duration-1000">
            XBRL Tagging Platform
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto animate-in fade-in-0 duration-1000 delay-200">
            A comprehensive solution for tagging ESG reports with ESRS Taxonomy
          </p>
          {/* Auth Buttons */}
          <div className="flex justify-center items-center gap-4 pt-4 flex-wrap animate-in fade-in-0 duration-1000 delay-300">
            {isAuthenticated ? (
              <>
                <p className="text-muted-foreground">Welcome back, {user?.full_name || user?.username}!</p>
                <Button
                  onClick={handleLogout}
                  variant="destructive"
                  size="lg"
                  className="flex items-center gap-2 hover:scale-105 transition-all duration-200 hover:shadow-lg"
                >
                  <LogOut className="w-4 h-4 transition-transform group-hover:rotate-12" />
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button asChild size="lg" className="hover:scale-105 transition-all duration-200 hover:shadow-lg">
                  <Link href="/login">Login</Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  size="lg"
                  className="hover:scale-105 transition-all duration-200 hover:shadow-lg hover:bg-primary hover:text-primary-foreground bg-transparent"
                >
                  <Link href="/register">Register</Link>
                </Button>
              </>
            )}
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-8">
          {/* Upload & Editor */}
          <Card className="group hover:scale-105 hover:shadow-xl transition-all duration-300 hover:border-primary/50 cursor-pointer animate-in fade-in-0 duration-700 delay-100">
            <CardHeader>
              <FileText className="h-8 w-8 text-primary mb-2 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300" />
              <CardTitle className="group-hover:text-primary transition-colors duration-300">
                Report Upload & Editor
              </CardTitle>
              <CardDescription>Upload PDF/DOCX or paste raw report text for tagging</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="group-hover:text-foreground transition-colors duration-300">
                Upload, parse, and edit your financial reports in a structured format. Our rich text editor allows you
                to modify content while maintaining structure.
              </p>
            </CardContent>
            <CardFooter>
              <Button
                variant="outline"
                asChild
                className="w-full group-hover:bg-primary group-hover:text-primary-foreground group-hover:border-primary transition-all duration-300 bg-transparent"
              >
                <Link href="/editor" className="flex items-center justify-center gap-2">
                  Open Editor
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                </Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Context Management */}
          <Card className="group hover:scale-105 hover:shadow-xl transition-all duration-300 hover:border-primary/50 cursor-pointer animate-in fade-in-0 duration-700 delay-200">
            <CardHeader>
              <Calendar className="h-8 w-8 text-primary mb-2 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300" />
              <CardTitle className="group-hover:text-primary transition-colors duration-300">
                Context Management
              </CardTitle>
              <CardDescription>Create and manage XBRL contexts for your reports</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="group-hover:text-foreground transition-colors duration-300">
                Define reporting contexts with entity information, time periods, and scenarios. Apply these contexts
                when tagging financial data.
              </p>
            </CardContent>
            <CardFooter>
              <Button
                variant="outline"
                asChild
                className="w-full group-hover:bg-primary group-hover:text-primary-foreground group-hover:border-primary transition-all duration-300 bg-transparent"
              >
                <Link href="/contexts" className="flex items-center justify-center gap-2">
                  Manage Contexts
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                </Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Taxonomy Browser */}
          <Card className="group hover:scale-105 hover:shadow-xl transition-all duration-300 hover:border-primary/50 cursor-pointer animate-in fade-in-0 duration-700 delay-300">
            <CardHeader>
              <BookOpen className="h-8 w-8 text-primary mb-2 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300" />
              <CardTitle className="group-hover:text-primary transition-colors duration-300">
                Taxonomy Browser
              </CardTitle>
              <CardDescription>Browse and search the ESRS XBRL taxonomy</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="group-hover:text-foreground transition-colors duration-300">
                Explore the complete ESRS taxonomy with detailed information about concepts, labels, definitions, and
                relationships.
              </p>
            </CardContent>
            <CardFooter>
              <Button
                variant="outline"
                asChild
                className="w-full group-hover:bg-primary group-hover:text-primary-foreground group-hover:border-primary transition-all duration-300 bg-transparent"
              >
                <Link href="/taxonomy" className="flex items-center justify-center gap-2">
                  Browse Taxonomy
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                </Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Tagging Interface */}
          <Card className="group hover:scale-105 hover:shadow-xl transition-all duration-300 hover:border-primary/50 cursor-pointer animate-in fade-in-0 duration-700 delay-400">
            <CardHeader>
              <Tag className="h-8 w-8 text-primary mb-2 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300" />
              <CardTitle className="group-hover:text-primary transition-colors duration-300">
                Tagging Interface
              </CardTitle>
              <CardDescription>Tag report sections with XBRL concepts</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="group-hover:text-foreground transition-colors duration-300">
                Intuitive interface for selecting report sections and assigning appropriate XBRL concepts and contexts.
                View and manage all tagged facts.
              </p>
            </CardContent>
            <CardFooter>
              <Button
                variant="outline"
                asChild
                className="w-full group-hover:bg-primary group-hover:text-primary-foreground group-hover:border-primary transition-all duration-300 bg-transparent"
              >
                <Link href="/editor" className="flex items-center justify-center gap-2">
                  Start Tagging
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                </Link>
              </Button>
            </CardFooter>
          </Card>

          {/* XBRL Preview */}
          <Card className="group hover:scale-105 hover:shadow-xl transition-all duration-300 hover:border-primary/50 cursor-pointer animate-in fade-in-0 duration-700 delay-500">
            <CardHeader>
              <FileCode className="h-8 w-8 text-primary mb-2 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300" />
              <CardTitle className="group-hover:text-primary transition-colors duration-300">
                XBRL Preview & Export
              </CardTitle>
              <CardDescription>Generate and download valid XBRL documents</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="group-hover:text-foreground transition-colors duration-300">
                Preview your tagged data as XML or JSON and export valid XBRL instance documents that comply with
                regulatory standards.
              </p>
            </CardContent>
            <CardFooter>
              <Button
                variant="outline"
                asChild
                className="w-full group-hover:bg-primary group-hover:text-primary-foreground group-hover:border-primary transition-all duration-300 bg-transparent"
              >
                <Link href="/xbrl-preview" className="flex items-center justify-center gap-2">
                  Preview XBRL
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                </Link>
              </Button>
            </CardFooter>
          </Card>

          {/* User Management */}
          <Card className="group hover:scale-105 hover:shadow-xl transition-all duration-300 hover:border-primary/50 cursor-pointer animate-in fade-in-0 duration-700 delay-600">
            <CardHeader>
              <Users className="h-8 w-8 text-primary mb-2 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300" />
              <CardTitle className="group-hover:text-primary transition-colors duration-300">User Management</CardTitle>
              <CardDescription>Manage users and permissions</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="group-hover:text-foreground transition-colors duration-300">
                Create and manage user accounts with different permission levels. Control access to reports and tagging
                functionality.
              </p>
            </CardContent>
            <CardFooter>
              <Button
                variant="outline"
                asChild
                className="w-full group-hover:bg-primary group-hover:text-primary-foreground group-hover:border-primary transition-all duration-300 bg-transparent"
              >
                <Link href="/users" className="flex items-center justify-center gap-2">
                  Manage Users
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                </Link>
              </Button>
            </CardFooter>
          </Card>
        </div>

        {/* CTA Footer */}
        <div className="bg-muted p-8 rounded-lg mt-12 hover:bg-muted/80 transition-all duration-300 hover:shadow-lg animate-in fade-in-0 duration-1000 delay-700 group">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <h2 className="text-2xl font-bold group-hover:text-primary transition-colors duration-300">
              Ready to streamline your XBRL reporting?
            </h2>
            <p className="text-muted-foreground group-hover:text-foreground transition-colors duration-300">
              Our platform simplifies the complex process of XBRL tagging for ESRS compliance, saving you time and
              reducing errors.
            </p>
            <Button size="lg" asChild className="hover:scale-105 transition-all duration-300 hover:shadow-xl">
              <Link href={isAuthenticated ? "/editor" : "/register"} className="flex items-center gap-2">
                {isAuthenticated ? "Start Tagging" : "Get Started Now"}
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  )
}
