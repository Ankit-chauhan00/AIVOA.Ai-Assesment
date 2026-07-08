import { useSelector, useDispatch } from 'react-redux'
import { updateField } from '../store/form_slice'

export default function InteractionForm() {
  const dispatch = useDispatch()
  const formData = useSelector((state) => state.form)

  const handleChange = (key) => (e) =>
    dispatch(updateField({ key, value: e.target.value }))

  return (
    <div className="flex h-full flex-col overflow-y-auto p-5 space-y-4">
      <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--clinical)]">
        Interaction
      </h2>

      <label className="block">
        <span className="mb-1 block text-xs text-[var(--ink-muted)]">HCP Name</span>
        <input
          value={formData.hcp_name || ''}
          onChange={handleChange('hcp_name')}
          className="w-full rounded-lg border border-[var(--border)] px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-[var(--ink-muted)]">Specialty</span>
        <input
          value={formData.specialty || ''}
          onChange={handleChange('specialty')}
          className="w-full rounded-lg border border-[var(--border)] px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-[var(--ink-muted)]">Hospital</span>
        <input
          value={formData.hospital || ''}
          onChange={handleChange('hospital')}
          className="w-full rounded-lg border border-[var(--border)] px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-[var(--ink-muted)]">City</span>
        <input
          value={formData.city || ''}
          onChange={handleChange('city')}
          className="w-full rounded-lg border border-[var(--border)] px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-[var(--ink-muted)]">Interaction Type</span>
        <select
          value={formData.interaction_type || ''}
          onChange={handleChange('interaction_type')}
          className="w-full rounded-lg border border-[var(--border)] px-3 py-2 text-sm"
        >
          <option value="">Select…</option>
          <option value="Meeting">Meeting</option>
          <option value="Call">Call</option>
          <option value="Email">Email</option>
          <option value="Conference">Conference</option>
        </select>
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-[var(--ink-muted)]">Products Discussed</span>
        <input
          value={formData.products_discussed || ''}
          onChange={handleChange('products_discussed')}
          className="w-full rounded-lg border border-[var(--border)] px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-[var(--ink-muted)]">Notes</span>
        <textarea
          rows={4}
          value={formData.notes || ''}
          onChange={handleChange('notes')}
          className="w-full resize-none rounded-lg border border-[var(--border)] px-3 py-2 text-sm"
        />
      </label>
    </div>
  )
}