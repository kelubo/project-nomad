/**
 * [zh-cn patch] 轻量 i18n 框架
 * ------------------------------------------------------------
 * 设计目标：
 *  - 不引入第三方依赖（避免改 package.json，降低合并上游冲突）
 *  - t('English text') 直接用英文原文做 key；语言包里没翻译的 key
 *    原样返回英文，因此逐页汉化可渐进推进，永远不会白屏
 *  - 支持 {name} 形式的插值：t('Hello {name}', { name: 'World' })
 *  - 语言偏好存 localStorage，默认中文（zh-cn 定制版）
 *
 * 用法：
 *   import { useI18n } from '~/lib/i18n'
 *   const { t } = useI18n()
 *   <p>{t('Dashboard')}</p>
 */
import { createContext, useContext, useMemo, useState, type ReactNode } from 'react'
import { zhCN } from '~/locales/zh-CN'

type Dict = Record<string, string>
type TranslateVars = Record<string, string | number>

type Locale = 'zh-CN' | 'en'

interface I18nContextValue {
  locale: Locale
  setLocale: (l: Locale) => void
  t: (key: string, vars?: TranslateVars) => string
}

const STORAGE_KEY = 'nomad_locale'

const I18nContext = createContext<I18nContextValue | null>(null)

const dictionaries: Record<Locale, Dict> = {
  'zh-CN': zhCN,
  en: {}, // 英文即原文
}

function interpolate(text: string, vars?: TranslateVars): string {
  if (!vars) return text
  return text.replace(/\{(\w+)\}/g, (m, k: string) => (k in vars ? String(vars[k]) : m))
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY) as Locale | null
      // 仅接受支持的语种；未设置时默认中文（zh-cn 定制版）
      if (saved === 'zh-CN' || saved === 'en') return saved
    } catch {
      /* localStorage 不可用时忽略 */
    }
    return 'zh-CN'
  })

  const setLocale = (l: Locale) => {
    setLocaleState(l)
    try {
      localStorage.setItem(STORAGE_KEY, l)
    } catch {
      /* ignore */
    }
  }

  const t = useMemo(() => {
    const dict = dictionaries[locale] ?? {}
    return (key: string, vars?: TranslateVars) => interpolate(dict[key] ?? key, vars)
  }, [locale])

  return (
    <I18nContext.Provider value={{ locale, setLocale, t }}>
      {children}
    </I18nContext.Provider>
  )
}

export function useI18n(): I18nContextValue {
  const ctx = useContext(I18nContext)
  if (!ctx) {
    // 未包在 Provider 里时降级为原样返回，保证任何组件都能安全调用
    return { locale: 'en', setLocale: () => {}, t: (k) => k }
  }
  return ctx
}

/** 非组件环境（如常量定义）里用的全局翻译函数，读取当前 localStorage 语种 */
export function tGlobal(key: string, vars?: TranslateVars): string {
  let locale: Locale = 'zh-CN'
  try {
    const saved = localStorage.getItem(STORAGE_KEY) as Locale | null
    if (saved === 'zh-CN' || saved === 'en') locale = saved
  } catch {
    /* ignore */
  }
  const dict = dictionaries[locale] ?? {}
  return interpolate(dict[key] ?? key, vars)
}
