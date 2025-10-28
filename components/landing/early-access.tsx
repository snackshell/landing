"use client";

import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function EarlyAccess() {
  return (
    <section className="relative py-24" id="signin">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <Card className="relative overflow-hidden border-border bg-gradient-to-br from-neutral-900 via-neutral-900 to-neutral-800 text-neutral-50">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(59,130,246,0.35),rgba(37,99,235,0))]" />
            <CardContent className="relative p-10 md:p-14">
              <div className="flex flex-col gap-10 md:flex-row md:items-center md:justify-between">
                <div className="max-w-xl space-y-4">
                  <Badge className="bg-white/10 text-white">Secure access</Badge>
                  <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">
                    Sign in and orchestrate all of your AI operations from one dashboard
                  </h2>
                  <p className="text-base text-neutral-300">
                    Manage teams, track billing, and unlock advanced routing with enterprise-grade security and audit logs.
                  </p>
                  <div className="flex items-center gap-3 text-sm text-neutral-400">
                    <ShieldCheck className="h-4 w-4 text-blue-400" />
                    SOC 2 Type II and GDPR ready
                  </div>
                </div>

                <div className="flex flex-col gap-3 md:items-end">
                  <Button size="lg" variant="secondary" className="bg-white text-neutral-950 hover:bg-neutral-200" asChild>
                    <a href="/login" className="flex items-center gap-2">
                      Sign In
                      <ArrowRight className="h-4 w-4" />
                    </a>
                  </Button>
                  <Button size="lg" variant="outline" className="border-white/30 text-neutral-50 hover:bg-white/10" asChild>
                    <a href="#pricing">Book a demo</a>
                  </Button>
                  <p className="text-xs text-neutral-400">No setup fees. 14-day trial on all plans.</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}
