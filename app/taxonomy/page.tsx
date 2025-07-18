"use client"

import { useState } from "react"
import { Search, Info, ChevronRight, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import type { TaxonomyConcept } from "@/types/report"
import { sampleTaxonomyConcepts } from "@/lib/sample-data"

export default function TaxonomyPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedConcept, setSelectedConcept] = useState<TaxonomyConcept | null>(null)

  const filteredConcepts = sampleTaxonomyConcepts.filter(
    (concept) =>
      concept.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
      concept.id.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  return (
    <div className="container mx-auto py-6">
      <h1 className="text-3xl font-bold mb-6">Taxonomy Browser</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <Card className="h-full">
            <CardHeader className="pb-3">
              <CardTitle>ESRS Concepts</CardTitle>
              <CardDescription>Browse and search the ESRS taxonomy concepts</CardDescription>
              <div className="relative mt-2">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search concepts..."
                  className="pl-8"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <ScrollArea className="h-[calc(100vh-300px)]">
                <div className="divide-y">
                  {filteredConcepts.length === 0 ? (
                    <div className="p-4 text-center text-sm text-muted-foreground">No concepts found</div>
                  ) : (
                    filteredConcepts.map((concept) => (
                      <div
                        key={concept.id}
                        className={`p-3 cursor-pointer hover:bg-accent transition-colors ${
                          selectedConcept?.id === concept.id ? "bg-primary/10" : ""
                        }`}
                        onClick={() => setSelectedConcept(concept)}
                      >
                        <div className="font-medium">{concept.label}</div>
                        <div className="text-xs text-muted-foreground mt-1 flex items-center">
                          <span>{concept.id}</span>
                          <Badge variant="outline" className="ml-2 text-xs">
                            {concept.type}
                          </Badge>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          {selectedConcept ? (
            <Card>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle>{selectedConcept.label}</CardTitle>
                    <CardDescription className="mt-1">{selectedConcept.id}</CardDescription>
                  </div>
                  <Badge variant="outline">{selectedConcept.type}</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="details">
                  <TabsList className="grid w-full grid-cols-4">
                    <TabsTrigger value="details">Details</TabsTrigger>
                    <TabsTrigger value="presentation">Presentation</TabsTrigger>
                    <TabsTrigger value="calculation">Calculation</TabsTrigger>
                    <TabsTrigger value="references">References</TabsTrigger>
                  </TabsList>

                  <TabsContent value="details" className="space-y-4 mt-4">
                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground mb-1">Definition</h3>
                      <p>{selectedConcept.definition}</p>
                    </div>

                    <Separator />

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">Period Type</h3>
                        <p className="capitalize">{selectedConcept.periodType}</p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">Data Type</h3>
                        <p>{selectedConcept.dataType}</p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">Balance</h3>
                        <p className="capitalize">{selectedConcept.balance || "Not applicable"}</p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">Abstract</h3>
                        <p>{selectedConcept.abstract ? "Yes" : "No"}</p>
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground mb-1">Labels</h3>
                      <div className="space-y-2 mt-2">
                        {selectedConcept.labels?.map((label, index) => (
                          <div key={index} className="flex justify-between p-2 bg-muted rounded-md">
                            <span>{label.value}</span>
                            <Badge variant="outline">{label.role}</Badge>
                          </div>
                        ))}
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="presentation" className="mt-4">
                    <div className="space-y-2">
                      <div className="flex items-center p-2 bg-muted rounded-md">
                        <ChevronRight className="h-4 w-4 mr-2" />
                        <span>ESRS E1 - Climate change</span>
                      </div>
                      <div className="flex items-center p-2 bg-muted rounded-md ml-6">
                        <ChevronRight className="h-4 w-4 mr-2" />
                        <span>Disclosure Requirements</span>
                      </div>
                      <div className="flex items-center p-2 bg-primary/10 rounded-md ml-12 font-medium">
                        <span>{selectedConcept.label}</span>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="calculation" className="mt-4">
                    <div className="p-4 text-center">
                      <Info className="h-10 w-10 text-muted-foreground mx-auto mb-2" />
                      <p className="text-muted-foreground">No calculation relationships available for this concept.</p>
                    </div>
                  </TabsContent>

                  <TabsContent value="references" className="mt-4">
                    <div className="space-y-2">
                      {selectedConcept.references?.map((reference, index) => (
                        <div key={index} className="p-3 border rounded-md">
                          <div className="font-medium">{reference.name}</div>
                          <div className="text-sm text-muted-foreground mt-1">{reference.paragraph}</div>
                          {reference.uri && (
                            <Button variant="link" size="sm" className="p-0 h-auto mt-2" asChild>
                              <a href={reference.uri} target="_blank" rel="noopener noreferrer">
                                View Reference <ExternalLink className="h-3 w-3 ml-1" />
                              </a>
                            </Button>
                          )}
                        </div>
                      ))}

                      {(!selectedConcept.references || selectedConcept.references.length === 0) && (
                        <div className="p-4 text-center">
                          <p className="text-muted-foreground">No references available for this concept.</p>
                        </div>
                      )}
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          ) : (
            <Card className="h-full flex items-center justify-center">
              <CardContent className="text-center py-10">
                <Info className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">No Concept Selected</h3>
                <p className="text-muted-foreground max-w-md mx-auto">
                  Select a concept from the list to view its details, presentation, calculation relationships, and
                  references.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
