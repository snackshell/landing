import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ExternalLink } from "lucide-react";

export function CodeEditorCard() {
  return (
    <Card className="bg-card border-border overflow-hidden">
      <CardHeader className="p-0 border-b border-border">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <div className="w-3 h-3 rounded-full bg-green-500" />
          </div>
          <div className="flex-1 ml-8">
            <div className="inline-flex items-center px-4 py-1 text-xs font-medium text-muted-foreground bg-secondary/50 rounded-t-md border-b-2 border-primary">
              [your-file.ts]
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <pre className="text-sm font-mono">
          <code className="block space-y-1">
            <span className="text-cyan-400">interface</span> <span className="text-foreground">Config</span> {"{"}
            <span className="block pl-4">
              <span className="text-cyan-400">apiKey</span>: <span className="text-green-400">&quot;string&quot;</span>;
            </span>
            <span className="block pl-4">
              <span className="text-cyan-400">endpoint</span>: <span className="text-green-400">&quot;string&quot;</span>;
            </span>
            <span className="block pl-4">
              <span className="text-cyan-400">timeout</span>: <span className="text-yellow-400">number</span>;
            </span>
            {"}"}
            {"\n"}
            <span className="text-purple-400">const</span> <span className="text-foreground">config</span>: <span className="text-cyan-400">Config</span> = {"{"}
            <span className="block pl-4">
              <span className="text-cyan-400">apiKey</span>: <span className="text-green-400">&quot;your-api-key&quot;</span>,
            </span>
            <span className="block pl-4">
              <span className="text-cyan-400">endpoint</span>: <span className="text-green-400">&quot;https://api.example.com&quot;</span>,
            </span>
            <span className="block pl-4">
              <span className="text-cyan-400">timeout</span>: <span className="text-yellow-400">5000</span>
            </span>
            {"}"};
          </code>
        </pre>
      </CardContent>
      <CardFooter className="px-6 py-4 border-t border-border flex justify-end">
        <Button variant="link" className="text-muted-foreground hover:text-foreground">
          View Demo
          <ExternalLink className="ml-2 h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
}
