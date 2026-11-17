import { tGlobal as t } from '~/lib/i18n'

export default function NotFound() {
  return (
    <>
      <div className="container">
        <div className="title">{t('Page not found')}</div>

        <span>{t('This page does not exist.')}</span>
      </div>
    </>
  )
}