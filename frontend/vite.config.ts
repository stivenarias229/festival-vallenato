/// <reference types="vitest/config" />
import path from "node:path"
import tailwindcss from "@tailwindcss/vite"
import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "./src"),
    },
  },
  base: "/static/",
  server: {
    host: "localhost",
    port: 5173,
    strictPort: true,
    origin: "http://localhost:5173",
    cors: true,
  },
  build: {
    manifest: "manifest.json",
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: "src/main.ts",
    },
  },
  test: {
    environment: "jsdom",
    include: ["src/**/*.spec.ts"],
  },
})
