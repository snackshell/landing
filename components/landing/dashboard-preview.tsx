"use client";

import { motion } from "framer-motion";
import {
  Activity,
  Zap,
  Code,
  Image as ImageIcon,
  MessageSquare,
  TrendingUp,
  Bot,
  Sparkles,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export function DashboardPreview() {
  return (
    <section className="relative overflow-hidden py-24 bg-neutral-50" id="dashboard">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <Badge variant="outline" className="mb-4">
            Dashboard Preview
          </Badge>
          <h2 className="text-3xl font-semibold tracking-tight text-neutral-900 sm:text-4xl">
            Everything You Need at Your Fingertips
          </h2>
          <p className="mt-4 text-lg text-neutral-600">
            Monitor your AI infrastructure with interactive cards and real-time metrics
          </p>
        </div>

        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3"
        >
          <motion.div variants={item} className="group">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="rounded-lg bg-blue-100 p-2">
                      <Activity className="h-5 w-5 text-blue-600" />
                    </div>
                    <CardTitle className="text-lg">API Usage</CardTitle>
                  </div>
                  <Badge variant="secondary">Real-time</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-muted-foreground">Requests Today</span>
                      <span className="text-sm font-semibold">3,240 / 5,000</span>
                    </div>
                    <Progress value={65} className="h-2" />
                  </div>
                  <div className="grid grid-cols-2 gap-4 pt-2">
                    <div>
                      <p className="text-xs text-muted-foreground">Success Rate</p>
                      <p className="text-xl font-semibold text-green-600">98.5%</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Avg. Latency</p>
                      <p className="text-xl font-semibold text-blue-600">243ms</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item} className="group">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="rounded-lg bg-purple-100 p-2">
                      <Zap className="h-5 w-5 text-purple-600" />
                    </div>
                    <CardTitle className="text-lg">Credits Left</CardTitle>
                  </div>
                  <Badge variant="secondary">Active</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-muted-foreground">Available Credits</span>
                      <span className="text-sm font-semibold">$780 / $1,000</span>
                    </div>
                    <Progress value={78} className="h-2" />
                  </div>
                  <div className="flex items-center justify-between pt-2">
                    <span className="text-sm text-muted-foreground">Renewal Date</span>
                    <span className="text-sm font-medium">Dec 15, 2024</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item} className="group">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <div className="rounded-lg bg-green-100 p-2">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                  </div>
                  <CardTitle className="text-lg">Performance</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Uptime</span>
                    <span className="text-sm font-semibold text-green-600">99.98%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Cost Savings</span>
                    <span className="text-sm font-semibold text-blue-600">$124.50</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Response Time</span>
                    <span className="text-sm font-semibold">Fast</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item} className="group sm:col-span-2 lg:col-span-1">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border bg-gradient-to-br from-blue-50 to-purple-50">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <div className="rounded-lg bg-blue-600 p-2">
                    <MessageSquare className="h-5 w-5 text-white" />
                  </div>
                  <CardTitle className="text-lg">AI Chat</CardTitle>
                </div>
                <CardDescription>Interactive conversational AI</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-3">
                  Access GPT-4, Claude 3.5, and more in a unified interface
                </p>
                <div className="flex items-center gap-2">
                  <Badge>GPT-4 Turbo</Badge>
                  <Badge variant="secondary">Claude 3.5</Badge>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item} className="group">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border bg-gradient-to-br from-purple-50 to-pink-50">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <div className="rounded-lg bg-purple-600 p-2">
                    <ImageIcon className="h-5 w-5 text-white" />
                  </div>
                  <CardTitle className="text-lg">Image Generation</CardTitle>
                </div>
                <CardDescription>Create stunning visuals</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-3">
                  Generate, edit, and upscale images with AI
                </p>
                <div className="flex items-center gap-2">
                  <Badge>DALL-E 3</Badge>
                  <Badge variant="secondary">Stable Diffusion</Badge>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item} className="group">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border bg-gradient-to-br from-green-50 to-emerald-50">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <div className="rounded-lg bg-green-600 p-2">
                    <Code className="h-5 w-5 text-white" />
                  </div>
                  <CardTitle className="text-lg">Code Assistant</CardTitle>
                </div>
                <CardDescription>AI-powered development</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-3">
                  Write, debug, and optimize code faster
                </p>
                <div className="flex items-center gap-2">
                  <Badge>Code Llama</Badge>
                  <Badge variant="secondary">Codex</Badge>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item} className="group sm:col-span-2 lg:col-span-2">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="rounded-lg bg-amber-100 p-2">
                      <Sparkles className="h-5 w-5 text-amber-600" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">Recent Activity</CardTitle>
                      <CardDescription>Collaborate with your entire team</CardDescription>
                    </div>
                  </div>
                  <Badge variant="outline">Team</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {[
                  {
                    name: "Jordan Lee",
                    role: "Head of Product",
                    action: "Set up Claude fallback for marketing assistant",
                  },
                  {
                    name: "Amina Yusuf",
                    role: "ML Engineer",
                    action: "Deployed new GPT-4o streaming workflow",
                  },
                  {
                    name: "Diego Alvarez",
                    role: "Support Lead",
                    action: "Reviewed usage analytics and shared report",
                  },
                ].map((user) => (
                  <div key={user.name} className="flex items-start gap-3">
                    <Avatar>
                      <AvatarImage src={`https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(user.name)}`} alt={user.name} />
                      <AvatarFallback>
                        {user.name
                          .split(" ")
                          .map((part) => part[0])
                          .join("")}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="text-sm font-semibold text-neutral-900">{user.name}</p>
                      <p className="text-xs text-muted-foreground">{user.role}</p>
                      <p className="mt-1 text-sm text-neutral-600">{user.action}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={item} className="group sm:col-span-2 lg:col-span-3">
            <Card className="transition-all duration-300 hover:shadow-lg hover:-translate-y-1 border-border">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="rounded-lg bg-indigo-100 p-2">
                      <Bot className="h-5 w-5 text-indigo-600" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">Available AI Models</CardTitle>
                      <CardDescription>Instantly switch between providers</CardDescription>
                    </div>
                  </div>
                  <Badge variant="outline" className="flex items-center gap-1">
                    <Sparkles className="h-3 w-3" />
                    12 Models
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3">
                  {[
                    { name: "GPT-4", provider: "OpenAI", status: "active" },
                    { name: "Claude 3.5", provider: "Anthropic", status: "active" },
                    { name: "Gemini Pro", provider: "Google", status: "active" },
                    { name: "Llama 3", provider: "Meta", status: "idle" },
                    { name: "Mistral", provider: "Mistral AI", status: "idle" },
                    { name: "PaLM 2", provider: "Google", status: "idle" },
                  ].map((model) => (
                    <div
                      key={model.name}
                      className="rounded-lg border border-neutral-200 bg-white p-3 text-center shadow-sm hover:shadow-md transition-shadow"
                    >
                      <div className="flex justify-center mb-2">
                        <div
                          className={`h-2 w-2 rounded-full ${
                            model.status === "active" ? "bg-green-500" : "bg-gray-300"
                          }`}
                        />
                      </div>
                      <p className="text-sm font-semibold text-neutral-900">{model.name}</p>
                      <p className="text-xs text-muted-foreground">{model.provider}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
