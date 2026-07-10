import { useSelector, useDispatch } from 'react-redux'
import { updateField } from '../store/form_slice'

export default function InteractionForm() {
  const dispatch = useDispatch()
  const formData = useSelector((state) => state.form)

  const handleChange = (key) => (e) =>
    dispatch(updateField({ key, value: e.target.value }))

  return (
    <div className="flex h-full w-[40%] bg-secondary rounded-md flex-col overflow-y-auto p-5 space-y-4">
      <h2 className="text-3xl font-bold text-clinical-100 uppercase tracking-wide text-[var(--clinical)]">
        Interaction
      </h2>

      <label className="block">
        <span className="mb-1 block text-xs text-ink-faint">HCP Name</span>
        <input
          value={formData.hcp_name || ''}
          onChange={handleChange('hcp_name')}
          className="w-full rounded-lg border border-ink-faint text-surface outline-0  px-3 py-2 text-sm font-sans"
          placeholder='Enter the name of the Health Care professional you meet'
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs  text-ink-faint">Specialty</span>
        <input
          value={formData.specialty || ''}
          onChange={handleChange('specialty')}
          className="w-full rounded-lg border border-ink-faint text-surface outline-0   px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-ink-faint">Hospital</span>
        <input
          value={formData.hospital || ''}
          onChange={handleChange('hospital')}
          className="w-full rounded-lg border border-ink-faint text-surface outline-0 px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-ink-faint">City</span>
        <input
          value={formData.city || ''}
          onChange={handleChange('city')}
          className="w-full rounded-lg border border-ink-faint text-surface outline-0 px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-ink-faint">Interaction Type</span>
        <select
          value={formData.interaction_type || ''}
          onChange={handleChange('interaction_type')}
          className="w-full rounded-lg border border-ink-faint text-surface outline-0  px-3 py-2 text-sm"
        >
          <option value="">Select…</option>
          <option value="Meeting">Meeting</option>
          <option value="Call">Call</option>
          <option value="Email">Email</option>
          <option value="Conference">Conference</option>
        </select>
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-ink-faint">Products Discussed</span>
        <input
          value={formData.products_discussed || ''}
          onChange={handleChange('products_discussed')}
          className="w-full rounded-lg border border-ink-faint text-surface outline-0  px-3 py-2 text-sm"
        />
      </label>

      <label className="block">
        <span className="mb-1 block text-xs text-ink-faint">Notes</span>
        <textarea
          rows={4}
          value={formData.notes || ''}
          onChange={handleChange('notes')}
          className="w-full resize-none rounded-lg border border-ink-faint text-surface outline-0  px-3 py-2 text-sm"
        />
      </label>
    </div>
  )
}