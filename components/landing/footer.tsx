import Link from "next/link";
import { Github, Twitter, Linkedin } from "lucide-react";
import { Separator } from "@/components/ui/separator";

export function Footer() {
  const footerLinks = {
    Product: [
      { label: "Overview", href: "#hero" },
      { label: "Dashboard", href: "#dashboard" },
      { label: "Features", href: "#features" },
      { label: "Playground", href: "#playground" },
    ],
    Resources: [
      { label: "Documentation", href: "#docs" },
      { label: "Pricing", href: "#pricing" },
      { label: "Early access", href: "#signin" },
      { label: "Status", href: "#dashboard" },
    ],
    Company: [
      { label: "About", href: "#hero" },
      { label: "Partners", href: "#features" },
      { label: "Contact", href: "#signin" },
      { label: "Support", href: "#signin" },
    ],
    Legal: [
      { label: "Privacy", href: "#pricing" },
      { label: "Terms", href: "#pricing" },
      { label: "Security", href: "#docs" },
      { label: "Cookie Policy", href: "#pricing" },
    ],
  };

  const socialLinks = [
    { icon: Github, href: "https://github.com", label: "GitHub" },
    { icon: Twitter, href: "https://twitter.com", label: "Twitter" },
    { icon: Linkedin, href: "https://linkedin.com", label: "LinkedIn" },
  ];

  return (
    <footer className="bg-neutral-50 border-t border-border">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-5 lg:gap-12">
          <div className="col-span-2">
            <Link href="/" className="flex items-center space-x-2 mb-4">
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                SelamAI
              </span>
            </Link>
            <p className="text-sm text-muted-foreground max-w-xs">
              Your unified gateway to modern AI. Access all the leading AI models from OpenAI, Anthropic, Google, and more through a single platform.
            </p>
            <div className="flex space-x-4 mt-6">
              {socialLinks.map((social) => (
                <Link
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-white text-muted-foreground transition-colors hover:bg-neutral-100 hover:text-foreground"
                  aria-label={social.label}
                >
                  <social.icon className="h-4 w-4" />
                </Link>
              ))}
            </div>
          </div>

          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h3 className="font-semibold text-sm text-foreground mb-4">{category}</h3>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link.label}>
                    <Link
                      href={link.href}
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <Separator className="my-8" />

        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} SelamAI. All rights reserved.
          </p>
          <div className="flex gap-6">
            <Link href="#privacy" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Privacy Policy
            </Link>
            <Link href="#terms" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Terms of Service
            </Link>
            <Link href="#cookies" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Cookie Settings
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
