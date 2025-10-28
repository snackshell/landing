"use client";

import { motion } from "framer-motion";
import { Layers, Activity, Shuffle, BarChart3 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const features = [
  {
    title: "Unified API Access",
    description: "Call GPT-4, Claude, Gemini, and more through a single, beautifully designed interface.",
    icon: Layers,
    accent: "from-blue-500/10 to-blue-500/20",
  },
  {
    title: "Real-time Streaming",
    description: "Lightning-fast streaming responses with advanced retry, logging, and observability tools.",
    icon: Activity,
    accent: "from-purple-500/10 to-purple-500/20",
  },
  {
    title: "Multi-Model Switching",
    description: "Seamlessly switch providers or cascade between models with one click, without redeployment.",
    icon: Shuffle,
    accent: "from-emerald-500/10 to-emerald-500/20",
  },
  {
    title: "Usage Analytics",
    description: "Granular analytics across teams, projects, and models to help you track cost and performance.",
    icon: BarChart3,
    accent: "from-indigo-500/10 to-indigo-500/20",
  },
];

export function FeatureHighlights() {
  return (
    <section className="relative py-24" id="features">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <Badge variant="outline" className="mb-4">
            Why teams choose SelamAI
          </Badge>
          <h2 className="text-3xl font-semibold tracking-tight text-neutral-900 sm:text-4xl">
            Built for teams shipping AI at scale
          </h2>
          <p className="mt-4 text-lg text-neutral-600">
            Powerful features packaged in an elegant dashboard that feels premium out of the box.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-80px" }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group"
            >
              <Card className="relative h-full overflow-hidden border-border transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
                <div className={`absolute inset-x-0 top-0 h-1 bg-gradient-to-r ${feature.accent}`} />
                <CardHeader>
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-white to-neutral-50 shadow-inner">
                    <feature.icon className="h-6 w-6 text-neutral-900" />
                  </div>
                  <CardTitle className="text-xl mt-4">{feature.title}</CardTitle>
                  <CardDescription className="text-base leading-7 text-neutral-600">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    {index === 0 && "SDKs for TypeScript, Python, and Go."}
                    {index === 1 && "Deliver conversational experiences that feel instantaneous."}
                    {index === 2 && "Route by latency, cost, or accuracy — no reconfiguration required."}
                    {index === 3 && "Stay on top of consumption with predictive alerts and anomaly detection."}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
