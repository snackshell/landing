"use client";

import { motion } from "framer-motion";
import { Book, Compass, Workflow, NotebookPen } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const resources = [
  {
    title: "Quickstart Guide",
    description: "Spin up your first unified API request in minutes with TypeScript or Python examples.",
    icon: Compass,
  },
  {
    title: "Streaming API",
    description: "Learn how to stream responses from GPT-4, Claude, and Gemini with built-in fallbacks.",
    icon: Workflow,
  },
  {
    title: "Playbook Library",
    description: "Prebuilt workflows for agents, image generation, and code copilots ready to deploy.",
    icon: NotebookPen,
  },
];

export function DocumentationSection() {
  return (
    <section className="relative py-24 bg-neutral-50" id="docs">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl text-center mb-16">
          <Badge variant="outline" className="mb-4">
            Documentation
          </Badge>
          <h2 className="text-3xl font-semibold tracking-tight text-neutral-900 sm:text-4xl">
            Ship faster with battle-tested guides
          </h2>
          <p className="mt-4 text-lg text-neutral-600">
            Extensive documentation, code samples, and architectural blueprints help you bring production AI to market.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6 }}
            className="group"
          >
            <Card className="h-full border-border bg-gradient-to-br from-white via-blue-50/70 to-purple-50/60">
              <CardHeader className="flex-col items-start gap-4 border-b border-white/60">
                <div className="flex items-center gap-3 rounded-xl bg-white/70 px-3 py-2 shadow-sm">
                  <Book className="h-5 w-5 text-blue-600" />
                  <span className="text-sm font-medium text-neutral-700">Developer Hub</span>
                </div>
                <CardTitle className="text-2xl leading-tight text-neutral-900">
                  Explore the SelamAI docs
                </CardTitle>
                <CardDescription className="text-base text-neutral-600">
                  A premium documentation experience with searchable endpoints, detailed tutorials, and ready-made integrations.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-5 pt-6">
                <div className="rounded-xl border border-white/60 bg-white/70 p-4 text-sm text-neutral-600">
                  <p className="font-medium text-neutral-900">Featured tutorial</p>
                  <p className="mt-2">
                    Build an AI agent that routes between GPT-4 and Claude based on latency with fewer than 30 lines of code.
                  </p>
                </div>
                <Button size="lg" className="rounded-full px-6">
                  Browse Documentation
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="grid gap-6 sm:grid-cols-2"
          >
            {resources.map((resource, index) => (
              <Card
                key={resource.title}
                className={`border-border transition-all duration-300 hover:-translate-y-1 hover:shadow-lg ${
                  index === 0 ? "sm:col-span-2" : ""
                }`}
              >
                <CardHeader className="flex h-full flex-col gap-4">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-neutral-100">
                    <resource.icon className="h-5 w-5 text-neutral-900" />
                  </div>
                  <CardTitle className="text-lg">{resource.title}</CardTitle>
                  <CardDescription className="text-base text-neutral-600">
                    {resource.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
