import { tGlobal as t } from '~/lib/i18n'
import AppLayout from '~/layouts/AppLayout'

export default function About() {
  return (
    <AppLayout>
      <div className="p-2">{t('Hello from About!')}</div>
    </AppLayout>
  )
}
