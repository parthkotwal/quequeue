/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#121212',       
        accent: '#FFD700',        
        accentLight: '#FFEC99',   
        secondaryText: '#B3B3B3', 
        divider: '#2C2C2C',       
      },
      fontFamily: {
        silkscreen: ['Silkscreen', 'sans-serif'], 
        inconsolata: ['Inconsolata', 'sans-serif'],      
      },
    },
  },
  plugins: [],
}

