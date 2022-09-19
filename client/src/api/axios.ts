import { IAuthTokens, TokenRefreshRequest, applyAuthTokenInterceptor } from 'axios-jwt'
import axios from 'axios'
import router from '@/router'



const BASE_URL = 'http://127.0.0.1:8000/api'

export const axiosInstance = axios.create({ baseURL: BASE_URL })

axiosInstance.interceptors.response.use(
  (response) => {
      return response;
  },
  async function (error) {
      // if the backend server is inactive, redirect to the 500 error page
      if (error.code === 'ERR_NETWORK') {
          router.push({name:"E500"})
          return Promise.reject(error);
      }

  }
);

const requestRefresh: TokenRefreshRequest = async (refreshToken: string): Promise<IAuthTokens | string> => {
  // a refresh token will be requested if the access token has expired
  const response = await axios.post(`${BASE_URL}/token/refresh`, { refresh: refreshToken })

  return response.data.access
}

applyAuthTokenInterceptor(axiosInstance, {
  requestRefresh,
  header:"Authorization",  
  headerPrefix:"Bearer", 
})
