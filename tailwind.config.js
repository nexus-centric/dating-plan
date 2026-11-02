export default { content: ['./index.html','./src/**/*.{ts,tsx}'], theme: { extend: {
  colors: {
    // pastel pink (sampled from MB Bank pink theme reference) + sage/mint green accent
    blush: { 50: '#fdf6f7', 100: '#fce8ec', 200: '#f9d3da', 300: '#f6b4bf', 400: '#f4899c', 500: '#e9667f', 600: '#d74562', 700: '#b3364f', 800: '#8f2b40', 900: '#6e2232' },
    mint: { 50: '#effaf5', 100: '#d8f3e6', 200: '#b3e6cf', 300: '#84d4b2', 400: '#52bf92', 500: '#2fa87a', 600: '#218a63', 700: '#1c6e51', 800: '#185841', 900: '#134736' },
  },
  keyframes: { pop: {'0%':{opacity:0,transform:'translateY(8px) scale(.98)'},'100%':{opacity:1,transform:'none'}} },
  animation: { pop: 'pop .35s ease-out both' } } }, plugins: [] }
