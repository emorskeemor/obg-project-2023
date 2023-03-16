import { IAuthTokens, TokenRefreshRequest, applyAuthTokenInterceptor } from 'axios-jwt'
import axios from 'axios'
import router from '@/router'


// base url of the server
const BASE_URL = 'http://10.20.12.92:8080'

export const axiosInstance = axios.create({ baseURL: BASE_URL })

// create an interceptor which will intercept all error responses raised by the server.
// We are interested in 500 errors which is most likely due to a programming error but we
// may also want to redirect certain 400 errors too. e.g. forbidden or permission denied
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
      return Promise.reject(error);

  }
);

const requestRefresh: TokenRefreshRequest = async (refreshToken: string): Promise<IAuthTokens | string> => {
  // a refresh token will be requested if the access token has expired
  const response = await axios.post(`${BASE_URL}/api/token/refresh`, { refresh: refreshToken })

  return response.data.access
}

applyAuthTokenInterceptor(axiosInstance, {
  requestRefresh,
  // header:"Authorization",  
  // headerPrefix:"Bearer", 
})
