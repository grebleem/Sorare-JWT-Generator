loginQuery = """
mutation SignInMutation($input: signInInput!, $aud: String!) {
  signIn(input: $input) {
    currentUser {
      slug
    }
    jwtToken(aud: $aud) {
      token
      expiredAt
    }
    errors {
      message
    }
  }
}
"""

loginOtp = """
mutation SignInMutationOTP($input: signInInput!, $aud: String!) { 
    signIn(input: $input) { 
        currentUser { 
            slug 
        } 
        jwtToken(aud: $aud) { 
            token 
            expiredAt 
        } 
        otpSessionChallenge
        errors { 
            message 
        } 
    } 
}
"""