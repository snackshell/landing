"use client";

import { motion } from "framer-motion";
import { Code2, Terminal, Play } from "lucide-react";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const codeSnippets: Record<string, string> = {
  typescript: `import { SelamAI } from "selamai";

const client = new SelamAI({ apiKey: process.env.SELAM_AI_KEY });

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are an expert assistant." },
    { role: "user", content: "Generate a product launch plan." },
  ],
  stream: true,
});

for await (const chunk of response) {
  process.stdout.write(chunk);
}`,
  python: `import os
from selamai import SelamAI

client = SelamAI(api_key=os.environ.get("SELAM_AI_KEY"))

stream = client.chat.completions.create(
    model="claude-3-5",
    messages=[
        {"role": "system", "content": "You are an expert assistant."},
        {"role": "user", "content": "Summarize this technical doc."},
    ],
    stream=True,
)

for chunk in stream:
    print(chunk, end="")`}

export function PlaygroundPreview() {
  return (
    <section className="relative py-24" id="playground">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <Badge variant="outline" className="mb-4">
            API Playground
          </Badge>
          <h2 className="text-3xl font-semibold tracking-tight text-neutral-900 sm:text-4xl">
            Build and experiment in real-time
          </h2>
          <p className="mt-4 text-lg text-neutral-600">
            Prototype prompts, evaluate models, and ship production-ready workflows — all inside SelamAI.
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]"
        >
          <Card className="border-border bg-neutral-900 text-neutral-50 shadow-2xl">
            <CardHeader className="border-b border-white/10">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="rounded-md bg-white/10 p-2">
                    <Terminal className="h-4 w-4" />
                  </div>
                  <div>
                    <CardTitle className="text-base font-medium text-white">Live Code Editor</CardTitle>
                    <CardDescription className="text-sm text-white/60">
                      Swap languages and stream responses instantly.
                    </CardDescription>
                  </div>
                </div>
                <Badge className="bg-white text-neutral-900">Streaming</Badge>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <Tabs defaultValue="typescript" className="w-full">
                <TabsList className="w-full justify-start rounded-none border-b border-white/10 bg-transparent px-6">
                  <TabsTrigger value="typescript" className="data-[state=active]:bg-white/10">
                    TypeScript
                  </TabsTrigger>
                  <TabsTrigger value="python" className="data-[state=active]:bg-white/10">
                    Python
                  </TabsTrigger>
                </TabsList>
                {Object.entries(codeSnippets).map(([key, value]) => (
                  <TabsContent key={key} value={key} className="m-0">
                    <pre className="overflow-auto whitespace-pre-wrap break-words bg-neutral-900 px-6 py-6 font-mono text-sm text-white/90">
                      <code>{value}</code>
                    </pre>
                  </TabsContent>
                ))}
              </Tabs>
            </CardContent>
          </Card>

          <Card className="border-border">
            <CardHeader>
              <div className="flex items-center gap-2">
                <div className="rounded-md bg-blue-100 p-2">
                  <Code2 className="h-4 w-4 text-blue-700" />
                </div>
                <div>
                  <CardTitle className="text-lg">Deploy in one click</CardTitle>
                  <CardDescription>Spin up a production-ready endpoint without leaving the playground.</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="rounded-xl border border-blue-100 bg-blue-50/60 p-5 text-sm text-blue-900">
                <p className="font-medium">Live response</p>
                <p className="mt-2 text-blue-800/80">
                  "Here’s a launch plan that includes positioning, channels, and AI-assisted creative ideas."
                </p>
              </div>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-100 text-blue-700">1</span>
                  Connect your provider keys securely within SelamAI.
                </div>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-100 text-blue-700">2</span>
                  Experiment with prompts in the playground and stream live completions.
                </div>
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-100 text-blue-700">3</span>
                  Deploy to production with routing, logging, and analytics enabled by default.
                </div>
              </div>
              <Button className="w-full" size="lg">
                <Play className="mr-2 h-4 w-4" />
                Launch Playground
              </Button>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}
