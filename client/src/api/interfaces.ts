// all interfaces use due to TS

export interface DecodedTokenObject {
    exp: number,
    ist: number,
    jti: string,
    token_type: string,
    user_id:string
  }