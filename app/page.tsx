import {
  Header,
  Hero,
  DashboardPreview,
  FeatureHighlights,
  PlaygroundPreview,
  DocumentationSection,
  PricingSection,
  EarlyAccess,
  Footer,
} from "@/components/landing";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <DashboardPreview />
      <FeatureHighlights />
      <PlaygroundPreview />
      <DocumentationSection />
      <PricingSection />
      <EarlyAccess />
      <Footer />
    </main>
  );
}
