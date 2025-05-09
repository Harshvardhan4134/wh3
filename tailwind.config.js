/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#1E88E5",
        secondary: "#f8f9fa",
        error: "#e5383b",
        success: "#38b000",
        warning: "#FFA000",
        darkGreen: "#2E7D32",
        darkRed: "#C62828",
        darkBlue: "#1E3A8A",
        lightGray: "#6c757d"
      },
      boxShadow: {
        card: "0 2px 5px rgba(0,0,0,0.05)",
      },
    },
  },
  plugins: [],
};