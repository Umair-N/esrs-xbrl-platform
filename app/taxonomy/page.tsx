"use client";

import { useState, useMemo, useEffect } from "react";
import {
  Search,
  Info,
  ChevronRight,
  ChevronDown,
  Folder,
  FolderOpen,
  FileText,
  Home,
  AlertCircle,
  Calculator,
  Plus,
  Minus,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import {
  getTaxonomyData,
  searchTaxonomy,
  flattenTree,
  getNodePath,
  getCalculationChildren,
} from "@/lib/taxomony-data";
import type { TaxonomyNode } from "@/types/taxonomy";

// Tree Node Component
const TreeNode = ({
  node,
  level = 0,
  onSelect,
  selectedId,
  searchQuery,
}: {
  node: TaxonomyNode;
  level?: number;
  onSelect: (node: TaxonomyNode) => void;
  selectedId?: string;
  searchQuery: string;
}) => {
  const [isExpanded, setIsExpanded] = useState(level < 2);
  const hasChildren = node.children && node.children.length > 0;
  const hasCalculations = node.calculations && node.calculations.length > 0;

  const isSelected = selectedId === node.id;
  const matchesSearch =
    !searchQuery ||
    node.label?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    node.id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (node.name && node.name.toLowerCase().includes(searchQuery.toLowerCase()));

  const getIcon = () => {
    if (hasChildren) {
      return isExpanded ? (
        <FolderOpen className="h-4 w-4" />
      ) : (
        <Folder className="h-4 w-4" />
      );
    }
    return <FileText className="h-4 w-4" />;
  };

  const getBadgeColor = (labelType?: string) => {
    switch (labelType) {
      case "abstract":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300";
      case "table":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300";
      case "axis":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300";
      case "member":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300";
      case "text block":
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";
      case "line items":
        return "bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-300";
      case "typed axis":
        return "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";
    }
  };

  if (!matchesSearch && !hasChildren) return null;

  return (
    <div className="select-none">
      <div
        className={`flex items-center py-2 px-2 rounded-md cursor-pointer hover:bg-muted/50 transition-colors ${
          isSelected ? "bg-primary/10 border-l-2 border-primary" : ""
        }`}
        style={{ paddingLeft: `${level * 16 + 8}px` }}
        onClick={() => onSelect(node)}
      >
        {hasChildren && (
          <Button
            variant="ghost"
            size="sm"
            className="h-6 w-6 p-0 mr-1 hover:bg-muted"
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded(!isExpanded);
            }}
          >
            {isExpanded ? (
              <ChevronDown className="h-3 w-3" />
            ) : (
              <ChevronRight className="h-3 w-3" />
            )}
          </Button>
        )}

        <div className="flex items-center min-w-0 flex-1">
          <span className="mr-2 text-muted-foreground">{getIcon()}</span>
          <div className="min-w-0 flex-1">
            <div className="font-medium text-sm truncate flex items-center gap-1">
              {node.label}
              {hasCalculations && (
                <Calculator
                  className="h-3 w-3 text-blue-500"
                  // title="Has-calculations"
                />
              )}
            </div>
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              <span className="text-xs text-muted-foreground truncate font-mono">
                {node.id}
              </span>
              {node.labelType && (
                <Badge
                  variant="outline"
                  className={`text-xs ${getBadgeColor(node.labelType)}`}
                >
                  {node.labelType}
                </Badge>
              )}
              {node.order && (
                <Badge variant="secondary" className="text-xs">
                  #{node.order}
                </Badge>
              )}
            </div>
          </div>
        </div>
      </div>

      {hasChildren && isExpanded && (
        <div>
          {node.children?.map((child, index) => (
            <TreeNode
              key={`${child.id}-${index}`}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              selectedId={selectedId}
              searchQuery={searchQuery}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// Calculation Display Component
const CalculationDisplay = ({
  node,
  allNodes,
  onNodeSelect,
}: {
  node: TaxonomyNode;
  allNodes: TaxonomyNode[];
  onNodeSelect: (node: TaxonomyNode) => void;
}) => {
  const calculationChildren = getCalculationChildren(node, allNodes);

  if (!node.calculations || node.calculations.length === 0) {
    return (
      <div className="p-8 text-center">
        <Calculator className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
        <h3 className="font-medium mb-1">No Calculations</h3>
        <p className="text-muted-foreground text-sm">
          This element has no calculation relationships.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="text-sm text-muted-foreground">
        Calculation formula for <strong>{node.label}</strong>:
      </div>

      <div className="bg-muted p-4 rounded-md border">
        <div className="font-mono text-sm">
          {node.label} ={" "}
          {calculationChildren
            .map((child, index) => {
              const calc = node.calculations?.find((c) => c.to === child.id);
              const weight = calc?.weight || 1;
              const isPositive = weight > 0;

              return (
                <span key={child.id} className="inline-flex items-center">
                  {index > 0 && (
                    <span className="mx-2">
                      {isPositive ? (
                        <Plus className="h-3 w-3 text-green-600" />
                      ) : (
                        <Minus className="h-3 w-3 text-red-600" />
                      )}
                    </span>
                  )}
                  <span
                    className={isPositive ? "text-green-700" : "text-red-700"}
                  >
                    {Math.abs(weight) !== 1 && `${Math.abs(weight)} × `}
                    {child.label}
                  </span>
                </span>
              );
            })
            .reduce((prev, curr, index) => [prev, curr], [])}
        </div>
      </div>

      <div className="space-y-2">
        <div className="text-sm font-medium">Calculation components:</div>
        {calculationChildren.map((child) => {
          const calc = node.calculations?.find((c) => c.to === child.id);
          const weight = calc?.weight || 1;

          return (
            <Card
              key={child.id}
              className="p-3 cursor-pointer hover:bg-muted/50 transition-colors"
              onClick={() => onNodeSelect(child)}
            >
              <div className="flex items-center justify-between">
                <div className="min-w-0 flex-1">
                  <div className="font-medium text-sm">{child.label}</div>
                  <div className="text-xs text-muted-foreground font-mono">
                    {child.id}
                  </div>
                </div>
                <div className="flex items-center gap-2 ml-2">
                  <Badge
                    variant={weight > 0 ? "default" : "destructive"}
                    className="text-xs"
                  >
                    {weight > 0 ? "+" : ""}
                    {weight}
                  </Badge>
                  {calc?.order && (
                    <Badge variant="outline" className="text-xs">
                      Order: {calc.order}
                    </Badge>
                  )}
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default function TaxonomyPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedNode, setSelectedNode] = useState<TaxonomyNode | null>(null);

  // Load taxonomy data with error handling
  const taxonomyData = useMemo(() => {
    try {
      return getTaxonomyData();
    } catch (error) {
      console.error("Error loading taxonomy data:", error);
      return null;
    }
  }, []);

  // Debug: Log the structure
  useEffect(() => {
    if (taxonomyData) {
      console.log("Taxonomy data structure:", {
        data: taxonomyData,
        hasChildren: taxonomyData?.children,
        childrenType: Array.isArray(taxonomyData?.children),
        childrenLength: taxonomyData?.children?.length,
      });
    }
  }, [taxonomyData]);

  // Flatten tree for search with safety checks
  const allNodes = useMemo(() => {
    if (!taxonomyData || !taxonomyData.children) {
      console.warn("No taxonomy data or children found");
      return [];
    }
    return flattenTree(taxonomyData.children);
  }, [taxonomyData]);

  const filteredNodes = useMemo(() => {
    if (!searchQuery) return [];
    return searchTaxonomy(allNodes, searchQuery);
  }, [searchQuery, allNodes]);

  // Get breadcrumb path for selected node
  const breadcrumbPath = useMemo(() => {
    if (!selectedNode || !taxonomyData?.children) return [];
    return getNodePath(taxonomyData.children, selectedNode.id) || [];
  }, [selectedNode, taxonomyData]);

  // Count nodes with calculations
  const nodesWithCalculations = useMemo(() => {
    return allNodes.filter(
      (node) => node.calculations && node.calculations.length > 0
    ).length;
  }, [allNodes]);

  // Error state - if data couldn't be loaded
  if (!taxonomyData) {
    return (
      <div className="container mx-auto py-6 px-4">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Failed to load taxonomy data. Please check that `esrs_outline.json`
            exists in the `lib` folder and has the correct structure.
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  // No children state
  if (
    !taxonomyData.children ||
    !Array.isArray(taxonomyData.children) ||
    taxonomyData.children.length === 0
  ) {
    return (
      <div className="container mx-auto py-6 px-4">
        <Alert>
          <Info className="h-4 w-4" />
          <AlertDescription>
            Taxonomy data loaded but no children found. Data structure:{" "}
            {JSON.stringify(Object.keys(taxonomyData), null, 2)}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6 px-4">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">ESRS Taxonomy Browser</h1>
        <p className="text-muted-foreground mt-2">
          Browse the European Sustainability Reporting Standards (ESRS) XBRL
          Taxonomy - Section {taxonomyData.sectionCode || "General"}
        </p>

        {/* Breadcrumb for selected node */}
        {breadcrumbPath.length > 0 && (
          <div className="mt-4">
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbLink
                    href="#"
                    onClick={() => setSelectedNode(null)}
                  >
                    <Home className="h-4 w-4" />
                  </BreadcrumbLink>
                </BreadcrumbItem>
                {breadcrumbPath.map((segment, index) => (
                  <div key={index} className="flex items-center">
                    <BreadcrumbSeparator />
                    <BreadcrumbItem>
                      <BreadcrumbLink
                        href="#"
                        className={
                          index === breadcrumbPath.length - 1
                            ? "font-medium"
                            : ""
                        }
                      >
                        {segment}
                      </BreadcrumbLink>
                    </BreadcrumbItem>
                  </div>
                ))}
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        )}

        {/* Stats */}
        <div className="mt-2 text-sm text-muted-foreground flex gap-4">
          <span>Total elements: {allNodes.length}</span>
          <span>With calculations: {nodesWithCalculations}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Taxonomy Tree */}
        <div className="lg:col-span-1">
          <Card className="h-[calc(100vh-200px)]">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2">
                <Folder className="h-5 w-5" />
                Taxonomy Structure
              </CardTitle>
              <CardDescription>
                {taxonomyData.labelCode || "ESRS"} - {allNodes.length} total
                elements
              </CardDescription>
              <div className="relative mt-2">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search taxonomy..."
                  className="pl-8"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <ScrollArea className="h-[calc(100vh-350px)]">
                <div className="p-2">
                  {searchQuery ? (
                    // Search results - flat list
                    <div className="space-y-1">
                      {filteredNodes.length === 0 ? (
                        <div className="text-center py-8 text-muted-foreground">
                          <Search className="h-8 w-8 mx-auto mb-2" />
                          <p>No results found for "{searchQuery}"</p>
                        </div>
                      ) : (
                        <>
                          <div className="text-sm text-muted-foreground mb-2">
                            {filteredNodes.length} result
                            {filteredNodes.length === 1 ? "" : "s"}
                          </div>
                          {filteredNodes.map((node, index) => (
                            <div
                              key={`${node.id}-${index}`}
                              className={`p-2 cursor-pointer hover:bg-muted rounded-md transition-colors ${
                                selectedNode?.id === node.id
                                  ? "bg-primary/10 border-l-2 border-primary"
                                  : ""
                              }`}
                              onClick={() => setSelectedNode(node)}
                            >
                              <div className="font-medium text-sm flex items-center gap-1">
                                {node.label}
                                {node.calculations &&
                                  node.calculations.length > 0 && (
                                    <Calculator className="h-3 w-3 text-blue-500" />
                                  )}
                              </div>
                              <div className="text-xs text-muted-foreground mt-1 flex items-center gap-2 flex-wrap">
                                <span className="font-mono">{node.id}</span>
                                {node.labelType && (
                                  <Badge variant="outline" className="text-xs">
                                    {node.labelType}
                                  </Badge>
                                )}
                              </div>
                            </div>
                          ))}
                        </>
                      )}
                    </div>
                  ) : (
                    // Hierarchical tree view
                    <div>
                      <div className="mb-2 p-2 bg-muted rounded-md">
                        <div className="font-semibold text-sm">
                          {taxonomyData.label}
                        </div>
                        <div className="text-xs text-muted-foreground font-mono">
                          {taxonomyData.id || "Root"}
                        </div>
                        {taxonomyData.sectionCode && (
                          <Badge variant="secondary" className="text-xs mt-1">
                            Section {taxonomyData.sectionCode}
                          </Badge>
                        )}
                      </div>
                      {taxonomyData.children.map((child, index) => (
                        <TreeNode
                          key={`${child.id}-${index}`}
                          node={child}
                          onSelect={setSelectedNode}
                          selectedId={selectedNode?.id}
                          searchQuery={searchQuery}
                        />
                      ))}
                    </div>
                  )}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        {/* Details Panel */}
        <div className="lg:col-span-2">
          {selectedNode ? (
            <Card className="h-[calc(100vh-200px)]">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="min-w-0 flex-1">
                    <CardTitle className="break-words leading-relaxed flex items-center gap-2">
                      {selectedNode.label}
                      {selectedNode.calculations &&
                        selectedNode.calculations.length > 0 && (
                          <Calculator className="h-5 w-5 text-blue-500" />
                        )}
                    </CardTitle>
                    <CardDescription className="mt-1 font-mono text-xs break-all">
                      {selectedNode.id}
                    </CardDescription>
                  </div>
                  <div className="flex gap-2 ml-4 flex-wrap">
                    {selectedNode.labelType && (
                      <Badge variant="outline">{selectedNode.labelType}</Badge>
                    )}
                    {selectedNode.abstract === "true" && (
                      <Badge variant="secondary">Abstract</Badge>
                    )}
                    {selectedNode.order && (
                      <Badge variant="outline">
                        Order: {selectedNode.order}
                      </Badge>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="details" className="h-full">
                  <TabsList className="grid w-full grid-cols-5">
                    <TabsTrigger value="details">Details</TabsTrigger>
                    <TabsTrigger
                      value="calculations"
                      className="flex items-center gap-1"
                    >
                      <Calculator className="h-3 w-3" />
                      Calculations
                    </TabsTrigger>
                    <TabsTrigger value="hierarchy">Hierarchy</TabsTrigger>
                    <TabsTrigger value="properties">Properties</TabsTrigger>
                    <TabsTrigger value="children">
                      Children{" "}
                      {selectedNode.children?.length
                        ? `(${selectedNode.children.length})`
                        : ""}
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="details" className="space-y-4 mt-4">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">
                          Name
                        </h3>
                        <p className="text-sm font-mono bg-muted p-2 rounded">
                          {selectedNode.name || "N/A"}
                        </p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">
                          Type
                        </h3>
                        <p className="text-sm bg-muted p-2 rounded">
                          {selectedNode.type || "N/A"}
                        </p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">
                          Period Type
                        </h3>
                        <p className="text-sm capitalize bg-muted p-2 rounded">
                          {selectedNode.periodType || "N/A"}
                        </p>
                      </div>
                      <div>
                        <h3 className="text-sm font-medium text-muted-foreground mb-1">
                          Substitution Group
                        </h3>
                        <p className="text-sm bg-muted p-2 rounded font-mono">
                          {selectedNode.substitutionGroup || "N/A"}
                        </p>
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <h3 className="text-sm font-medium text-muted-foreground mb-2">
                        Original Label
                      </h3>
                      <p className="text-sm bg-muted p-3 rounded border">
                        {selectedNode.originalLabel}
                      </p>
                    </div>

                    {selectedNode.calculations &&
                      selectedNode.calculations.length > 0 && (
                        <>
                          <Separator />
                          <div>
                            <h3 className="text-sm font-medium text-muted-foreground mb-2">
                              Calculation Summary
                            </h3>
                            <p className="text-sm bg-blue-50 p-3 rounded border border-blue-200">
                              This element has{" "}
                              {selectedNode.calculations.length} calculation
                              relationship(s). View the "Calculations" tab for
                              detailed formula.
                            </p>
                          </div>
                        </>
                      )}
                  </TabsContent>

                  <TabsContent value="calculations" className="mt-4">
                    <ScrollArea className="h-[400px]">
                      <CalculationDisplay
                        node={selectedNode}
                        allNodes={allNodes}
                        onNodeSelect={setSelectedNode}
                      />
                    </ScrollArea>
                  </TabsContent>

                  <TabsContent value="hierarchy" className="mt-4">
                    <div className="space-y-3">
                      <div className="text-sm text-muted-foreground">
                        Element hierarchy path:
                      </div>
                      <div className="p-4 bg-muted rounded-md border">
                        <div className="text-sm font-mono">
                          {breadcrumbPath.join(" → ") ||
                            "Root → " + selectedNode.label}
                        </div>
                      </div>

                      {selectedNode.children &&
                        selectedNode.children.length > 0 && (
                          <>
                            <div className="text-sm text-muted-foreground mt-4">
                              Direct children:
                            </div>
                            <div className="space-y-1">
                              {selectedNode.children
                                .slice(0, 5)
                                .map((child, index) => (
                                  <div
                                    key={index}
                                    className="text-sm p-2 bg-muted rounded"
                                  >
                                    {child.label}
                                  </div>
                                ))}
                              {selectedNode.children.length > 5 && (
                                <div className="text-sm text-muted-foreground">
                                  ... and {selectedNode.children.length - 5}{" "}
                                  more
                                </div>
                              )}
                            </div>
                          </>
                        )}
                    </div>
                  </TabsContent>

                  <TabsContent value="properties" className="mt-4">
                    <ScrollArea className="h-[400px]">
                      <div className="space-y-2">
                        {Object.entries(selectedNode).map(([key, value]) => {
                          if (key === "children") return null;
                          return (
                            <div
                              key={key}
                              className="flex flex-col sm:flex-row sm:justify-between p-3 bg-muted rounded-md text-sm gap-2"
                            >
                              <span className="font-medium font-mono">
                                {key}:
                              </span>
                              <span className="text-right break-all font-mono text-xs">
                                {Array.isArray(value)
                                  ? value.join(", ")
                                  : String(value)}
                              </span>
                            </div>
                          );
                        })}
                      </div>
                    </ScrollArea>
                  </TabsContent>

                  <TabsContent value="children" className="mt-4">
                    {selectedNode.children &&
                    selectedNode.children.length > 0 ? (
                      <ScrollArea className="h-[400px]">
                        <div className="space-y-2">
                          {selectedNode.children.map((child, index) => (
                            <div
                              key={`${child.id}-${index}`}
                              className="p-3 border rounded-md cursor-pointer hover:bg-muted/50 transition-colors group"
                              onClick={() => setSelectedNode(child)}
                            >
                              <div className="flex items-start justify-between">
                                <div className="min-w-0 flex-1">
                                  <div className="font-medium text-sm group-hover:text-primary transition-colors flex items-center gap-1">
                                    {child.label}
                                    {child.calculations &&
                                      child.calculations.length > 0 && (
                                        <Calculator className="h-3 w-3 text-blue-500" />
                                      )}
                                  </div>
                                  <div className="text-xs text-muted-foreground mt-1 flex items-center gap-2 flex-wrap">
                                    <span className="font-mono">
                                      {child.id}
                                    </span>
                                    {child.labelType && (
                                      <Badge
                                        variant="outline"
                                        className="text-xs"
                                      >
                                        {child.labelType}
                                      </Badge>
                                    )}
                                    {child.children &&
                                      child.children.length > 0 && (
                                        <Badge
                                          variant="secondary"
                                          className="text-xs"
                                        >
                                          {child.children.length} children
                                        </Badge>
                                      )}
                                    {child.order && (
                                      <Badge
                                        variant="outline"
                                        className="text-xs"
                                      >
                                        #{child.order}
                                      </Badge>
                                    )}
                                  </div>
                                </div>
                                <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
                              </div>
                            </div>
                          ))}
                        </div>
                      </ScrollArea>
                    ) : (
                      <div className="p-8 text-center">
                        <Info className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
                        <h3 className="font-medium mb-1">No Children</h3>
                        <p className="text-muted-foreground text-sm">
                          This element has no child elements.
                        </p>
                      </div>
                    )}
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          ) : (
            <Card className="h-[calc(100vh-200px)] flex items-center justify-center">
              <CardContent className="text-center py-10">
                <Info className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">
                  No Element Selected
                </h3>
                <p className="text-muted-foreground max-w-md mx-auto">
                  Select an element from the taxonomy tree to view its details,
                  properties, and relationships.
                </p>
                <div className="mt-4 text-sm text-muted-foreground">
                  <p>Total elements: {allNodes.length}</p>
                  <p>Elements with calculations: {nodesWithCalculations}</p>
                  <p>
                    Section: {taxonomyData.sectionCode || "General disclosures"}
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
