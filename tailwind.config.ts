import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/modules/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1E40AF",
        primaryHover: "#1D4ED8",

        bg: "#F8FAFC",
        card: "#FFFFFF",
        border: "#E5E7EB",

        textPrimary: "#111827",
        textSecondary: "#6B7280",

        success: "#16A34A",
        successBg: "#DCFCE7",

        warning: "#F59E0B",
        warningBg: "#FEF3C7",

        danger: "#EF4444",
        dangerBg: "#FEE2E2",

        info: "#2563EB",
        infoBg: "#DBEAFE",
      },
    },
  },
  plugins: [],
};

export default config;