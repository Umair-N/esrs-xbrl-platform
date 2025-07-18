"use client";

import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import {
  ArrowRight,
  FileText,
  Tag,
  Calendar,
  BookOpen,
  FileCode,
  Users,
  LogOut,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import ProtectedRoute from "@/components/protectedRoute";

export default function Home() {
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
      // Optionally redirect or trigger a toast
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto py-10 space-y-8">
        {/* Header Section */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">
            ESRS XBRL Tagging Platform
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            A comprehensive solution for tagging financial reports with ESRS
            XBRL concepts
          </p>

          {/* Auth Buttons */}
          <div className="flex justify-center items-center gap-4 pt-4 flex-wrap">
            {isAuthenticated ? (
              <>
                <p className="text-muted-foreground">
                  Welcome back, {user?.full_name || user?.username}!
                </p>

                <Button
                  onClick={handleLogout}
                  variant="destructive"
                  size="lg"
                  className="flex items-center gap-2"
                >
                  <LogOut className="w-4 h-4" />
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button asChild size="lg">
                  <Link href="/login">Login</Link>
                </Button>
                <Button asChild variant="outline" size="lg">
                  <Link href="/register">Register</Link>
                </Button>
              </>
            )}
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-8">
          {/* Upload & Editor */}
          <Card>
            <CardHeader>
              <FileText className="h-8 w-8 text-primary mb-2" />
              <CardTitle>Report Upload & Editor</CardTitle>
              <CardDescription>
                Upload PDF/DOCX or paste raw report text for tagging
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Upload, parse, and edit your financial reports in a structured
                format. Our rich text editor allows you to modify content while
                maintaining structure.
              </p>
            </CardContent>
            <CardFooter>
              <Button variant="outline" asChild className="w-full">
                <Link href="/editor">Open Editor</Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Context Management */}
          <Card>
            <CardHeader>
              <Calendar className="h-8 w-8 text-primary mb-2" />
              <CardTitle>Context Management</CardTitle>
              <CardDescription>
                Create and manage XBRL contexts for your reports
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Define reporting contexts with entity information, time periods,
                and scenarios. Apply these contexts when tagging financial data.
              </p>
            </CardContent>
            <CardFooter>
              <Button variant="outline" asChild className="w-full">
                <Link href="/contexts">Manage Contexts</Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Taxonomy Browser */}
          <Card>
            <CardHeader>
              <BookOpen className="h-8 w-8 text-primary mb-2" />
              <CardTitle>Taxonomy Browser</CardTitle>
              <CardDescription>
                Browse and search the ESRS XBRL taxonomy
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Explore the complete ESRS taxonomy with detailed information
                about concepts, labels, definitions, and relationships.
              </p>
            </CardContent>
            <CardFooter>
              <Button variant="outline" asChild className="w-full">
                <Link href="/taxonomy">Browse Taxonomy</Link>
              </Button>
            </CardFooter>
          </Card>

          {/* Tagging Interface */}
          <Card>
            <CardHeader>
              <Tag className="h-8 w-8 text-primary mb-2" />
              <CardTitle>Tagging Interface</CardTitle>
              <CardDescription>
                Tag report sections with XBRL concepts
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Intuitive interface for selecting report sections and assigning
                appropriate XBRL concepts and contexts. View and manage all
                tagged facts.
              </p>
            </CardContent>
            <CardFooter>
              <Button variant="outline" asChild className="w-full">
                <Link href="/editor">Start Tagging</Link>
              </Button>
            </CardFooter>
          </Card>

          {/* XBRL Preview */}
          <Card>
            <CardHeader>
              <FileCode className="h-8 w-8 text-primary mb-2" />
              <CardTitle>XBRL Preview & Export</CardTitle>
              <CardDescription>
                Generate and download valid XBRL documents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Preview your tagged data as XML or JSON and export valid XBRL
                instance documents that comply with regulatory standards.
              </p>
            </CardContent>
            <CardFooter>
              <Button variant="outline" asChild className="w-full">
                <Link href="/xbrl-preview">Preview XBRL</Link>
              </Button>
            </CardFooter>
          </Card>

          {/* User Management */}
          <Card>
            <CardHeader>
              <Users className="h-8 w-8 text-primary mb-2" />
              <CardTitle>User Management</CardTitle>
              <CardDescription>Manage users and permissions</CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Create and manage user accounts with different permission
                levels. Control access to reports and tagging functionality.
              </p>
            </CardContent>
            <CardFooter>
              <Button variant="outline" asChild className="w-full">
                <Link href="/users">Manage Users</Link>
              </Button>
            </CardFooter>
          </Card>
        </div>

        {/* CTA Footer */}
        <div className="bg-muted p-8 rounded-lg mt-12">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <h2 className="text-2xl font-bold">
              Ready to streamline your XBRL reporting?
            </h2>
            <p className="text-muted-foreground">
              Our platform simplifies the complex process of XBRL tagging for
              ESRS compliance, saving you time and reducing errors.
            </p>
            <Button size="lg" asChild>
              <Link href={isAuthenticated ? "/editor" : "/register"}>
                {isAuthenticated ? "Start Tagging" : "Get Started Now"}
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
