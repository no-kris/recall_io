import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import tseslint from "typescript-eslint";
import { defineConfig, globalIgnores } from "eslint/config";

export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      globals: globals.browser,
      parser: tseslint.parser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        project: "./tsconfig.json",
      },
    },
    plugins: {
      "@typescript-eslint": tseslint.plugin,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...tseslint.configs.recommended.rules,
      ...reactHooks.configs.flat.recommended.rules,
      ...reactRefresh.configs.vite.rules,
    },
  },
  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      globals: globals.browser,
    },
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...reactHooks.configs.flat.recommended.rules,
      ...reactRefresh.configs.vite.rules,
    },
  },
]);
