"use client";

import { motion } from "framer-motion";
import { Check, Sparkles } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const plans = [
  {
    name: "Starter",
    price: "$49",
    cadence: "per month",
    highlight: "Perfect for solo builders",
    features: ["5K requests included", "Playground access", "Community support"],
    cta: "Start for free",
    popular: false,
  },
  {
    name: "Growth",
    price: "$189",
    cadence: "per month",
    highlight: "Best for product teams",
    features: [
      "50K requests included",
      "Advanced routing",
      "Usage analytics",
      "Priority support",
    ],
    cta: "Launch dashboard",
    popular: true,
  },
  {
    name: "Scale",
    price: "Contact",
    cadence: "sales",
    highlight: "For enterprise workloads",
    features: [
      "Custom request volume",
      "Dedicated cluster",
      "SAML SSO & audit logs",
      "Enterprise SLAs",
    ],
    cta: "Talk to sales",
    popular: false,
  },
];

export function PricingSection() {
  return (
    <section className="relative py-24" id="pricing">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center mb-16">
          <Badge variant="outline" className="mb-4">
            Pricing
          </Badge>
          <h2 className="text-3xl font-semibold tracking-tight text-neutral-900 sm:text-4xl">
            Simple plans for teams of any size
          </h2>
          <p className="mt-4 text-lg text-neutral-600">
            Start for free, upgrade when you need advanced routing, analytics, and enterprise controls.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group"
            >
              <Card
                className={`relative h-full border-border transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${
                  plan.popular ? "border-blue-500/60 shadow-lg" : ""
                }`}
              >
                {plan.popular && (
                  <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-1 text-xs uppercase tracking-wide text-white">
                    Most popular
                  </Badge>
                )}
                <CardHeader>
                  <CardTitle className="text-xl">{plan.name}</CardTitle>
                  <CardDescription>{plan.highlight}</CardDescription>
                  <div className="mt-6 flex items-baseline gap-2">
                    <span className="text-4xl font-semibold text-neutral-900">{plan.price}</span>
                    <span className="text-sm text-muted-foreground">{plan.cadence}</span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-6">
                  <ul className="space-y-3">
                    {plan.features.map((feature) => (
                      <li key={feature} className="flex items-start gap-3 text-sm text-neutral-600">
                        <Check className="mt-0.5 h-4 w-4 text-blue-600" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>

                  <Button
                    variant={plan.popular ? "default" : "outline"}
                    className={`w-full ${plan.popular ? "bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500" : ""}`}
                  >
                    {plan.cta}
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        <div className="mt-12 flex flex-col items-center gap-3 text-sm text-muted-foreground">
          <div className="flex items-center gap-2 rounded-full border border-border px-3 py-1 text-xs uppercase tracking-wide">
            <Sparkles className="h-3.5 w-3.5 text-blue-600" />
            Volume discounts available • Migration support included
          </div>
          <p>
            Need a custom plan? <span className="font-medium text-neutral-900">Book a strategy session</span> with our solutions team.
          </p>
        </div>
      </div>
    </section>
  );
}
