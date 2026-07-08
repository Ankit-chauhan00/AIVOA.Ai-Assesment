import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  hcp_name: '',
  specialty: '',
  hospital: '',
  city: '',
  interaction_type: '',
  products_discussed: '',
  notes: '',
}

const formSlice = createSlice({
  name: 'form',
  initialState,
  reducers: {
    updateField: (state, action) => {
      const { key, value } = action.payload
      state[key] = value
    },
    setFormData: (state, action) => {
      return { ...state, ...action.payload }
    },
    resetForm: () => initialState,
  },
})

export const { updateField, setFormData, resetForm } = formSlice.actions
export default formSlice.reducer