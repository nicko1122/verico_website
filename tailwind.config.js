/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js,njk,md}",
    "./static/**/*.{html,js,njk,md}"
  ],
  theme: {
    extend: {
      colors: {
        'verico-primary': '#1a1a1a',
        'verico-secondary': '#f8f9fa',
        'verico-accent': '#007bff'
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'display': ['Poppins', 'system-ui', 'sans-serif']
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
} 