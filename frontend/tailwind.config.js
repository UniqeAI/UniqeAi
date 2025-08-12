export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        primary: '#8e44ad',
        secondary: '#f4efff',
        'chat-user': '#6366f1',
        'chat-bot': '#f8fafc',
        'chat-bot-dark': '#1e293b',
        'message-shadow': 'rgba(0, 0, 0, 0.1)',
        'message-shadow-dark': 'rgba(0, 0, 0, 0.3)',
      },
      boxShadow: {
        'message': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'message-dark': '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
      }
    }
  },
  plugins: []
}