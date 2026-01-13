/** @type {import('tailwindcss').Config} */
module.exports = {
  // Garante que o Tailwind escaneie seus arquivos (ajuste os caminhos se necessário)
  content: ["./App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Cores da Identidade Visual (Baseado no visual-mobile.md)
        primary: '#4F46E5',   // Indigo-600 (Ações principais, botões, ícones ativos)
        secondary: '#4338CA', // Indigo-700 (Hover/Press state)
        
        background: '#F8FAFC', // Slate-50 (Fundo padrão de todas as telas)
        surface: '#FFFFFF',    // White (Cards, inputs, barra de navegação)
        
        text: {
          primary: '#0F172A',   // Slate-900 (Títulos, texto forte)
          secondary: '#64748B', // Slate-500 (Subtítulos, legendas)
          muted: '#94A3B8',     // Slate-400 (Ícones inativos, placeholders)
        },

        status: {
          success: '#10B981', // Emerald-500 (Aprovado, check)
          error: '#EF4444',   // Red-500 (Reprovado, erro)
          warning: '#F59E0B', // Amber-500 (Avisos, estrelas)
        }
      },
      fontFamily: {
        // Usa a fonte do sistema por padrão, mas mapeada para 'sans'
        sans: ['System', 'sans-serif'],
      }
    },
  },
  plugins: [],
}