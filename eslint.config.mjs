// eslint.config.mjs
import js from '@eslint/js';
import { FlatCompat } from '@eslint/eslintrc';
import tseslint from 'typescript-eslint';
import nextPlugin from '@next/eslint-plugin-next';
import unusedImports from 'eslint-plugin-unused-imports';

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
  // Let compat supply eslint:recommended when needed
  recommendedConfig: js.configs.recommended,
});

export default [
  // 1) Ignore globs (flat config replaces .eslintignore)
  {
    ignores: [
      '.next/**',
      'node_modules/**',
      'dist/**',
      'coverage/**',
      'out/**',
    ],
  },

  // 2) Next.js presets (core web vitals + TS integration)
  ...compat.config({
    extends: ['next/core-web-vitals', 'next/typescript'],
  }),

  // 3) TypeScript: enable type-aware linting (reads your tsconfig)
  ...tseslint.configs.recommendedTypeChecked,

  // 4) Project-wide language options for TS type-aware rules
  {
    languageOptions: {
      parserOptions: {
        // Prefer projectService in flat config (faster + auto tsconfig discovery)
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },

  // 5) Plugins & custom rules
  {
    plugins: {
      '@next/next': nextPlugin,
      'unused-imports': unusedImports,
    },
    rules: {
      // Auto-remove unused imports on --fix
      'unused-imports/no-unused-imports': 'error',
      // Warn on unused vars; allow `_placeholder` and ignore rest siblings
      'unused-imports/no-unused-vars': [
        'warn',
        {
          vars: 'all',
          varsIgnorePattern: '^_',
          argsIgnorePattern: '^_',
          ignoreRestSiblings: true,
        },
      ],

      // Nice TS quality-of-life extras
      '@typescript-eslint/consistent-type-imports': [
        'warn',
        { prefer: 'type-imports' },
      ],
      '@typescript-eslint/no-misused-promises': [
        'error',
        { checksVoidReturn: { attributes: false } },
      ],
    },
  },

  // 6) Disable formatting conflicts; keep Prettier as your formatter
  ...compat.config({ extends: ['prettier'] }),
];
