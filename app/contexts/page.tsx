"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { CalendarIcon, Plus, Trash2, Edit } from "lucide-react"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { format } from "date-fns"
import { cn, generateUniqueId } from "@/lib/utils"
import type { XbrlContext } from "@/types/report"
import { sampleContexts } from "@/lib/sample-data"

export default function ContextsPage() {
  const [contexts, setContexts] = useState<XbrlContext[]>(sampleContexts)
  const [newContext, setNewContext] = useState<Partial<XbrlContext>>({
    entityName: "",
    entityScheme: "http://www.sec.gov/CIK",
    entityIdentifier: "",
    periodType: "instant",
    instantDate: new Date(),
    startDate: new Date(),
    endDate: new Date(),
  })

  const handleCreateContext = () => {
    if (!newContext.entityName || !newContext.entityIdentifier) {
      return
    }

    const contextId = `ctx-${generateUniqueId().substring(0, 8)}`

    let periodLabel = ""
    if (newContext.periodType === "instant") {
      periodLabel = `As of ${format(newContext.instantDate || new Date(), "yyyy-MM-dd")}`
    } else {
      periodLabel = `${format(newContext.startDate || new Date(), "yyyy-MM-dd")} to ${format(newContext.endDate || new Date(), "yyyy-MM-dd")}`
    }

    const context: XbrlContext = {
      id: contextId,
      label: `${newContext.entityName} - ${periodLabel}`,
      entityName: newContext.entityName || "",
      entityScheme: newContext.entityScheme || "http://www.sec.gov/CIK",
      entityIdentifier: newContext.entityIdentifier || "",
      periodType: newContext.periodType || "instant",
      instantDate: newContext.instantDate,
      startDate: newContext.startDate,
      endDate: newContext.endDate,
      createdAt: new Date().toISOString(),
    }

    setContexts([...contexts, context])

    // Reset form
    setNewContext({
      entityName: "",
      entityScheme: "http://www.sec.gov/CIK",
      entityIdentifier: "",
      periodType: "instant",
      instantDate: new Date(),
      startDate: new Date(),
      endDate: new Date(),
    })
  }

  const handleDeleteContext = (contextId: string) => {
    setContexts(contexts.filter((context) => context.id !== contextId))
  }

  return (
    <div className="container mx-auto py-6">
      <h1 className="text-3xl font-bold mb-6">Context Management</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Contexts</CardTitle>
              <CardDescription>
                Manage XBRL contexts for your reports. Contexts define the entity, period, and scenario information.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {contexts.length === 0 ? (
                <div className="text-center py-6">
                  <p className="text-sm text-muted-foreground">
                    No contexts created yet. Use the form to create a new context.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {contexts.map((context) => (
                    <div key={context.id} className="p-4 border rounded-md flex justify-between items-start">
                      <div>
                        <div className="font-medium">{context.label}</div>
                        <div className="text-sm text-muted-foreground mt-1">ID: {context.id}</div>
                        <div className="text-sm mt-2">
                          <span className="text-muted-foreground">Entity: </span>
                          {context.entityName} ({context.entityIdentifier})
                        </div>
                        <div className="text-sm">
                          <span className="text-muted-foreground">Period: </span>
                          {context.periodType === "instant"
                            ? `Instant: ${format(new Date(context.instantDate || ""), "yyyy-MM-dd")}`
                            : `Duration: ${format(new Date(context.startDate || ""), "yyyy-MM-dd")} to ${format(new Date(context.endDate || ""), "yyyy-MM-dd")}`}
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <Button size="icon" variant="ghost">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button size="icon" variant="ghost" onClick={() => handleDeleteContext(context.id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardHeader>
              <CardTitle>Create Context</CardTitle>
              <CardDescription>Define a new XBRL context to use for tagging.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="entityName">Entity Name</Label>
                <Input
                  id="entityName"
                  placeholder="e.g., Acme Corporation"
                  value={newContext.entityName || ""}
                  onChange={(e) => setNewContext({ ...newContext, entityName: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="entityScheme">Entity Scheme</Label>
                <Input
                  id="entityScheme"
                  value={newContext.entityScheme || "http://www.sec.gov/CIK"}
                  onChange={(e) => setNewContext({ ...newContext, entityScheme: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="entityIdentifier">Entity Identifier</Label>
                <Input
                  id="entityIdentifier"
                  placeholder="e.g., 0001234567"
                  value={newContext.entityIdentifier || ""}
                  onChange={(e) => setNewContext({ ...newContext, entityIdentifier: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label>Period Type</Label>
                <Select
                  value={newContext.periodType || "instant"}
                  onValueChange={(value) =>
                    setNewContext({ ...newContext, periodType: value as "instant" | "duration" })
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select period type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="instant">Instant (As of Date)</SelectItem>
                    <SelectItem value="duration">Duration (Date Range)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {newContext.periodType === "instant" ? (
                <div className="space-y-2">
                  <Label>Instant Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className={cn(
                          "w-full justify-start text-left font-normal",
                          !newContext.instantDate && "text-muted-foreground",
                        )}
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {newContext.instantDate ? format(newContext.instantDate, "PPP") : "Select date"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar
                        mode="single"
                        selected={newContext.instantDate}
                        onSelect={(date) => setNewContext({ ...newContext, instantDate: date })}
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Start Date</Label>
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button
                          variant="outline"
                          className={cn(
                            "w-full justify-start text-left font-normal",
                            !newContext.startDate && "text-muted-foreground",
                          )}
                        >
                          <CalendarIcon className="mr-2 h-4 w-4" />
                          {newContext.startDate ? format(newContext.startDate, "PPP") : "Select start date"}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0">
                        <Calendar
                          mode="single"
                          selected={newContext.startDate}
                          onSelect={(date) => setNewContext({ ...newContext, startDate: date })}
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                  </div>

                  <div className="space-y-2">
                    <Label>End Date</Label>
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button
                          variant="outline"
                          className={cn(
                            "w-full justify-start text-left font-normal",
                            !newContext.endDate && "text-muted-foreground",
                          )}
                        >
                          <CalendarIcon className="mr-2 h-4 w-4" />
                          {newContext.endDate ? format(newContext.endDate, "PPP") : "Select end date"}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0">
                        <Calendar
                          mode="single"
                          selected={newContext.endDate}
                          onSelect={(date) => setNewContext({ ...newContext, endDate: date })}
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                  </div>
                </div>
              )}
            </CardContent>
            <CardFooter>
              <Button
                className="w-full"
                onClick={handleCreateContext}
                disabled={!newContext.entityName || !newContext.entityIdentifier}
              >
                <Plus className="mr-2 h-4 w-4" />
                Create Context
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  )
}
