/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          700: "#0F5F5C",
          500: "#15847F",
          100: "#DDF4F2",
        },
        customBlue: {
          600: "#2563EB",
          100: "#DBEAFE",
        },
        success: {
          600: "#15803D",
        },
        warning: {
          600: "#D97706",
        },
        danger: {
          600: "#DC2626",
        },
        neutralGray: {
          950: "#111827",
          700: "#374151",
          500: "#6B7280",
          200: "#E5E7EB",
          50: "#F9FAFB",
        }
      },
      fontFamily: {
        sans: ["Inter", "Manrope", "system-ui", "sans-serif"],
      }
    },
  },
  plugins: [],
}
