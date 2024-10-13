import reactRefresh from "eslint-plugin-react-refresh";
import globals from "globals";
import tsParser from "@typescript-eslint/parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all
});

export default [
    {
        ignores: ["**/dist", "**/.eslintrc.cjs"],
    },
    ...compat.extends("eslint:recommended", "plugin:@typescript-eslint/recommended"),
    {
        plugins: {
            "react-refresh": reactRefresh,
        },
        files: ["**/*.ts", "**/*.tsx"],
        languageOptions: {
            globals: {
                ...globals.browser,
            },
            parser: tsParser,
        },
        rules: {
            "react-refresh/only-export-components": ["warn", {
                allowConstantExport: true,
            }],
        },
    }
];