/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    fontFamily: {
      sans: ['Lexend, sans-serif'],
      serif: ['Merriweather, serif'],
      mono: ['"Martian Mono", monospace']
    },
    listStyleType: {
      none: 'none',
      disc: 'disc',
      decimal: 'decimal',
      square: 'square',
      roman: 'lower-roman',
    },
    extend: {
      colors: {
        crosewater: '#f5e0dc',
        cflamingo: '#f2cdcd',
        cpink: '#f5c2e7',
        cmauve: '#cba6f7',
        cred: '#f38ba8',
        cmaroon: '#eba0ac',
        cpeach: '#fab387',
        cyellow: '#f9e2af',
        cgreen: '#a6e3a1',
        cteal: '#94e2d5',
        csky: '#89dceb',
        csapphire: '#74c7ec',
        cblue: '#89b4fa',
        clavender: '#b4befe',
        ctext: '#cdd6f4',
        csubtext1: '#bac2de',
        csubtext0: '#a6adc8',
        coverlay2: '#9399b2',
        coverlay1: '#7f849c',
        coverlay0: '#6c7086',
        csurface2: '#585b70',
        csurface1: '#45475a',
        csurface0: '#313244',
        cbase: '#1e1e2e',
        cmantle: '#181825',
        ccrust: '#11111b'
      }
    }
  },
  plugins: [],
}
