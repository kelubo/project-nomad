import { tGlobal as t } from '~/lib/i18n'

export default function ServerError(props: { error: any }) {
  return (
    <>
      <div className="container">
        <div className="title">{t('Server Error')}</div>

        <span>{props.error.message}</span>
      </div>
    </>
  )
}