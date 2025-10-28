"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-24 pb-20" id="hero">
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-blue-100 via-white to-purple-100" />
      <div className="absolute -top-32 left-1/2 h-72 w-72 -translate-x-1/2 rounded-full bg-blue-400/10 blur-3xl" />
      <div className="absolute -bottom-24 right-10 h-60 w-60 rounded-full bg-purple-400/10 blur-3xl" />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-3xl text-center"
        >
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="inline-flex items-center rounded-full border border-blue-100 bg-white px-4 py-1 text-sm font-medium text-blue-700 shadow-sm"
          >
            <Sparkles className="mr-2 h-4 w-4" />
            Introducing the unified AI dashboard
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="mx-auto mt-6 max-w-4xl text-center"
        >
          <h1 className="text-4xl font-semibold tracking-tight text-neutral-900 sm:text-5xl md:text-6xl">
            Your Gateway to the Power of OpenAI
          </h1>
          <p className="mt-6 text-lg leading-8 text-neutral-600">
            SelamAI gives you a beautifully crafted control center for OpenAI, Anthropic, Gemini, and more. Monitor usage, launch tools, and switch models instantly with a unified, premium experience.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
        >
          <Button size="lg" asChild className="rounded-full px-8 text-base">
            <Link href="#dashboard" className="flex items-center gap-2">
              Launch Dashboard
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
          <Badge className="rounded-full px-4 py-2 text-sm font-medium">
            Now supporting GPT-4, Claude 3.5, and Gemini 1.5
          </Badge>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.9, delay: 0.3 }}
          className="relative mx-auto mt-16 max-w-5xl"
        >
          <div className="absolute inset-0 -z-10 rounded-3xl bg-gradient-to-br from-white via-blue-50/70 to-purple-50/60 blur-2xl" />
          <div className="rounded-3xl border border-white/70 bg-white/80 p-8 shadow-2xl backdrop-blur">
            <div className="grid gap-6 sm:grid-cols-2">
              <div className="rounded-2xl border border-blue-100 bg-blue-50/60 p-6">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-blue-700">Live Requests</span>
                  <span className="text-xs text-blue-600">+18% today</span>
                </div>
                <p className="mt-4 text-3xl font-semibold text-neutral-900">12,480</p>
                <p className="text-sm text-neutral-600">Requests processed in the last 24 hours</p>
              </div>

              <div className="grid gap-4 rounded-2xl border border-purple-100 bg-white/80 p-6">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-purple-700">Credits Remaining</span>
                    <span className="text-xs text-purple-600">78%</span>
                  </div>
                  <div className="mt-3 h-2 rounded-full bg-purple-100">
                    <div className="h-2 w-[78%] rounded-full bg-gradient-to-r from-purple-500 to-blue-500" />
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { name: "GPT-4", status: "Active" },
                    { name: "Claude 3", status: "Streaming" },
                    { name: "Gemini", status: "Idle" },
                  ].map((model) => (
                    <div
                      key={model.name}
                      className="rounded-xl border border-neutral-200 bg-white/70 p-3 text-center shadow-sm"
                    >
                      <p className="text-sm font-medium text-neutral-800">{model.name}</p>
                      <p className="text-xs text-neutral-500">{model.status}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
