import { setAuthTokens, clearAuthTokens } from 'axios-jwt'
import { axiosInstance } from './axios'

// points to access token and refresh token retrieval
const login = async (params: object) => {
  const response = await axiosInstance.post('api/token', params)
  
  // sets the tokens in local storage
  setAuthTokens({
    accessToken: response.data.access,
    refreshToken: response.data.refresh
  })

  return response.data.access
}

// Clear the auth tokens from localstorage
const logout = () => clearAuthTokens()

export {login, logout}