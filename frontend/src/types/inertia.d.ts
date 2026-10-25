export type RolUsuario = "votante" | "administrador"

export interface AuthUser {
  id: number
  nombre: string
  email: string
  rol: RolUsuario
}

export interface FlashMessages {
  success?: string
  error?: string
  info?: string
}

export interface SharedUrls {
  inicio: string
  registro: string
  ingresar: string
  salir: string
  categorias: string
  recuperar: string
  panel: string
  panel_categorias: string
  panel_votaciones: string
  panel_usuarios: string
  panel_resultados: string
  panel_actividad: string
}

export interface SharedProps {
  auth: {
    user: AuthUser | null
  }
  flash: FlashMessages
  urls: SharedUrls
  errors?: Record<string, string | string[]>
}

declare module "@inertiajs/core" {
  interface PageProps extends SharedProps {}
}
