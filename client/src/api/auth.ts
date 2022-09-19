import { setAuthTokens, clearAuthTokens } from 'axios-jwt'
import { axiosInstance } from './axios'

// 4. Post email and password and get tokens in return. Call setAuthTokens with the result.
const login = async (params: object) => {
  const response = await axiosInstance.post('/token', params)
  
  setAuthTokens({
    accessToken: response.data.access,
    refreshToken: response.data.refresh
  })

  return response.data.access
}

// 5. Clear the auth tokens from localstorage
const logout = () => clearAuthTokens()

export {login, logout}