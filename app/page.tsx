import { Header } from "@/components/layout/Header";
import { CodeEditorCard } from "@/components/ui/CodeEditorCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      
      <section className="py-24">
        <div className="container mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            <div className="space-y-8">
              <div className="space-y-6">
                <p className="text-sm text-muted-foreground uppercase tracking-wide">
                  Modern Developer Tools
                </p>
                
                <h1 className="text-5xl lg:text-6xl font-bold tracking-tight leading-tight">
                  Build Better Software Faster
                </h1>
                
                <Badge variant="outline" className="px-4 py-2 text-sm font-mono">
                  npm install your-awesome-package
                </Badge>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Button size="lg" className="text-base px-8">
                  Get Started
                </Button>
                <Button size="lg" variant="outline" className="text-base">
                  <Plus className="mr-2 h-5 w-5" />
                  Learn More
                </Button>
              </div>
            </div>
            
            <div>
              <CodeEditorCard />
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
