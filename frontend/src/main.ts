import { createInertiaApp } from "@inertiajs/vue3"
import { createApp, h, type DefineComponent } from "vue"
import "vite/modulepreload-polyfill"
import "./style.css"

document.addEventListener("DOMContentLoaded", () => {
  createInertiaApp({
    http: {
      xsrfCookieName: "csrftoken",
      xsrfHeaderName: "X-CSRFToken",
    },
    title: (title) => (title ? `${title} · Aplicación` : "Aplicación"),
    resolve: (name) => {
      const pages = import.meta.glob<DefineComponent>("./pages/**/*.vue", {
        eager: true,
      })
      const page = pages[`./pages/${name}.vue`]

      if (!page) {
        throw new Error(`No se encontró la página ${name}`)
      }

      return page
    },
    setup({ el, App, props, plugin }) {
      createApp({ render: () => h(App, props) }).use(plugin).mount(el)
    },
  })
})
