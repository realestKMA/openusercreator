/* eslint-disable */
import { reactive, ref } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";
import VueCookies from 'vue-cookies';
import { useAppStore } from "./apps";

export const useAuthStore = defineStore("auth", () => {
  // router
  const router = useRouter()

  // stores
  const appStore = useAppStore()

  ////////////////////////////////////////////
  // app notification functionality
  ////////////////////////////////////////////
  const notify = reactive({open: false, detail: null, state: null})

  const isAuthenticated = ref(JSON.parse(localStorage.getItem('is_auth')))

  ////////////////////////////////////////////
  // sign up functionalitiy
  ////////////////////////////////////////////
  const signUp = reactive({loading: false, username: null, email: null, error: null})

  function resetSignUp() {
    signUp.loading = false
    signUp.username = signUp.email = signUp.error = null
  }

  async function submitSignUp(data) {
    signUp.loading = true
    signUp.username = signUp.email = signUp.error = null

    await axios.post("api/v1/creators/new/", data)
      .then((resp) => {
        signUp.loading = false
        signUp.username = signUp.email = signUp.error = null

        // set cookies
        VueCookies.set("access", resp.data['tokens']['access'], "12h")
        VueCookies.set("refresh", resp.data['tokens']['refresh'], "1d")

        // save user data in localStorage
        userProfile.value = resp.data['user']
        localStorage.setItem("user_profile", JSON.stringify(resp.data['user']))
        localStorage.setItem("is_auth", JSON.stringify(true))
        isAuthenticated.value = true

        // navigate to dashboard
        router.push({name :'dashboard', params: {username: resp.data['user']['username']}})

        // update notify
        notify.open = true
        notify.detail = resp.data['user']['username'] + ", welcome to Open User Data"
        notify.state = "good"
    
        setTimeout(() => {
          notify.open = false
          notify.detail = notify.state = null
        }, 5000);
      })
      .catch((err) => {
        if (err.response) {
          signUp.loading = isAuthenticated.value = false
          'username' in err.response.data ? signUp.username = err.response.data['username'][0]:''
          'email' in err.response.data ? signUp.email = err.response.data['email'][0]:''
        }
        else {
          signUp.error = "An error occured, please try again."
          signUp.loading = isAuthenticated.value = false
        }
      })
  }

  ////////////////////////////////////////////
  // sign in functionality
  ////////////////////////////////////////////
  const signIn = reactive({loading: false, username: null, password: null, error: null})

  function resetSignIn() {
    signIn.loading = false
    signIn.username = signIn.password = signIn.error = null
  }

  async function submitSignIn(data) {
    signIn.loading = true
    signIn.username = signIn.password = signIn.error = null

    await axios.post("api/v1/auth/login/token/", data)
      .then((resp) => {
        signIn.loading = false
        signIn.username = signIn.password = signIn.error = null

        // set auth cookies
        VueCookies.set("access", resp.data['access'], "12h")
        VueCookies.set("refresh", resp.data['refresh'], "1d")

        // set localStorage
        data['rememberMe'] ? localStorage.setItem("remember_me", data['username']) :
        localStorage.removeItem("remember_me")
        localStorage.setItem("is_auth", JSON.stringify(true))

        // get the authenticated users profile
        getUserProfile()
        isAuthenticated.value = true

        // update notify
        notify.open = true
        notify.detail = "Signed in successfully"
        notify.state = "good"
    
        setTimeout(() => {
          notify.open = false
          notify.detail = notify.state = null
        }, 5000);

        // the system will automatically sign the user out in the nest 12 hours
        setTimeout(() => {
          submitSignOut()
        }, 43200000);
      })
      .catch((err) => {
        if (err.response) {
          signIn.loading = isAuthenticated.value = false
          'username' in err.response.data ? signIn.username = err.response.data['username'][0]:''
          'password' in err.response.data ? signIn.password = err.response.data['password'][0]:''
          'detail' in err.response.data ? signIn.error = 'Wrong username or password provided':''
        }
        else {
          signIn.loading = isAuthenticated.value = false
          signIn.error = "An error occured, please try again."
        }
      })
  }

  ////////////////////////////////////////////
  // social authentication functionality
  ///////////////////////////////////////////
  const social = ref(JSON.parse(localStorage.getItem('auth_social')));
  const socialData = reactive({
    loading: false,
    error: null,
    data: JSON.parse(localStorage.getItem("auth_social_data"))
  })

  function setSocial(value) {
    social.value = value
    localStorage.setItem('auth_social', JSON.stringify(value))
  }

  async function getUserDataViaSocialProvider(url, data) {
    socialData.loading = true
    socialData.error = null
    
    await axios.get(`${url}${data}`)
      .then((resp) => {
        socialData.loading = false
        socialData.error = null
        socialData.data = resp.data

        // save to localStorage
        localStorage.setItem("auth_social_data", JSON.stringify(resp.data))
      })
      .catch((err) => {
        socialData.loading = false

        if (err.response) {
          if (err.response.status == 400) socialData.error = err.response.data['error']
          if (err.response.status == 500) socialData.error = "Link expired"
          else socialData.error = err.response.data['error']
        }
        else socialData.error = "An error occured"
      })
  }

  ////////////////////////////////////////////
  // GITHUB auth functionallity
  ////////////////////////////////////////////
  const socialGithub = reactive({loading: false, url: null, error: null})

  async function getGithubUrl() {
    socialGithub.loading = true
    socialGithub.error = socialGithub.url = null

    await axios.get("api/v1/auth/github/generate/url/")
      .then((resp) => {
        socialGithub.loading = false
        socialGithub.error = null
        socialGithub.url = resp.data['url']
      })
      .catch(() => {
        socialGithub.loading = false
        socialGithub.url = null
        socialGithub.error = "An error occured, please try again"
      })
  }

  ////////////////////////////////////////////
  // GOOGLE auth functionallity
  ////////////////////////////////////////////
  const socialGoogle = reactive({loading: false, url: null, error: null})

  async function getGoogleUrl() {
    socialGoogle.loading = true
    socialGoogle.error = socialGoogle.url = null

    await axios.get("api/v1/auth/google/generate/url/")
      .then((resp) => {
        socialGoogle.loading = false
        socialGoogle.error = null
        socialGoogle.url = resp.data['url']
      })
      .catch(() => {
        socialGoogle.loading = false
        socialGoogle.url = null
        socialGoogle.error = "An error occured, please try again"
      })
  }

  ////////////////////////////////////////////
  // TWITTER auth functionallity
  ////////////////////////////////////////////
  const socialTwitter = reactive({loading: false, url: null, error: null})

  async function getTwitterUrl() {
    socialTwitter.loading = true
    socialTwitter.error = socialTwitter.url = null

    await axios.get("api/v1/auth/twitter/generate/url/")
      .then((resp) => {
        socialTwitter.loading = false
        socialTwitter.error = null
        socialTwitter.url = resp.data['url']
      })
      .catch(() => {
        socialTwitter.loading = false
        socialTwitter.url = null
        socialTwitter.error = "An error occured, please try again"
      })
  }

  ////////////////////////////////////////////
  // social sign up functionalitiy
  ////////////////////////////////////////////
  const signUpSocial = reactive({loading: false, username: null, email: null, error: null})

  function resetSignUpSocila() {
    signUpSocial.loading = false
    signUpSocial.username = signUpSocial.email = signUpSocial.error = null
  }

  async function submitSignUpSocial(data) {
    signUpSocial.loading = true
    signUpSocial.username = signUpSocial.email = signUpSocial.error = null

    await axios.post("api/v1/auth/social/create/", data)
      .then((resp) => {
        signUpSocial.loading = false
        signUpSocial.username = signUpSocial.email = signUpSocial.error = null

        // set cookies
        VueCookies.set("access", resp.data['tokens']['access'], "12h")
        VueCookies.set("refresh", resp.data['tokens']['refresh'], "1d")

        // save user data in localStorage
        userProfile.value = resp.data['user']
        localStorage.setItem("user_profile", JSON.stringify(resp.data['user']))
        localStorage.setItem("is_auth", JSON.stringify(true))
        isAuthenticated.value = true

        // clear social data
        localStorage.removeItem("auth_social_data")
        socialData.data = null

        // navigate to dashboard
        router.push({name :'dashboard', params: {username: resp.data['user']['username']}})

        // update notify
        notify.open = true
        notify.detail = resp.data['user']['username'] + ", welcome to Open User Data"
        notify.state = "good"
    
        setTimeout(() => {
          notify.open = false
          notify.detail = notify.state = null
        }, 10000);
      })
      .catch((err) => {
        if (err.response) {
          signUpSocial.loading = isAuthenticated.value = false
          'username' in err.response.data ? signUpSocial.username = err.response.data['username'][0]:''
          'email' in err.response.data ? signUpSocial.email = err.response.data['email'][0]:''
        }
        else {
          signUpSocial.error = "An error occured, please try again."
          signUpSocial.loading = isAuthenticated.value = false
        }
      })
  }


  ////////////////////////////////////////////
  // user profiles functionality
  ////////////////////////////////////////////
  const userProfile = ref(JSON.parse(localStorage.getItem("user_profile")))
  const getUser = reactive({loading: false, error: null})

  async function getUserProfile() {
    getUser.loading = true
    getUser.error = null

    await axios.get("api/v1/creators/me/", {headers: {'Authorization': `Bearer ${VueCookies.get('access')}` }})
      .then((resp) => {
        getUser.loading = false
        getUser.error = null
        userProfile.value = resp.data
        localStorage.setItem("user_profile", JSON.stringify(resp.data))

        // navigate to users dashboard
        router.push({name: 'dashboard', params: {username: resp.data['username']}})
      })
      .catch((err) => {
        if (err.response) {
          getUser.loading = false
          err.response.status == 401 ? getUser.error = 'Token expired, please log in':'Connection error'
          submitSignOut()
        }
        else {
          getUser.error = "An error occured, please try again."
          getUser.loading = false
        }
      })
  }

  ////////////////////////////////////////////
  // sign out functionality
  ////////////////////////////////////////////
  const signOut = ref(false)

  function submitSignOut() {
    // close signOut modal
    signOut.value = false

    // clear localStorage data
    localStorage.removeItem("user_profile")
    localStorage.removeItem("user_apps")
    localStorage.removeItem("app_in_view")
    localStorage.setItem("is_auth", JSON.stringify(false))
    isAuthenticated.value = false
    appStore.myApps.data = JSON.parse(localStorage.getItem("user_apps"))
    
    // clear cookies data also
    VueCookies.remove("access")
    VueCookies.remove("refresh")
    
    // navigate to home page
    router.push({name: 'home'})
  }

  ////////////////////////////////////////////
  // forgot password functionality
  ////////////////////////////////////////////
  const forgotPassword = reactive({loading: false, success: false, error: null})

  async function submitForgotPassword(data) {
    forgotPassword.loading = true
    forgotPassword.error = null

    await axios.post("api/auth/help/forgot/password/", data)
      .then((resp) => {
        forgotPassword.loading = false
        forgotPassword.success = true
        forgotPassword.error = null

        setTimeout(() => {
          forgotPassword.success = false
          router.push({name: 'home'})
        }, 5000);
      })
      .catch((err) => {
        forgotPassword.loading = false
        forgotPassword.success = false
        forgotPassword.error = "An error occured."
      })
  }

  ////////////////////////////////////////////
  // Reset password functionality
  ////////////////////////////////////////////
  const resetPassword = reactive({loading: false, error: null})

  async function submitResetPassword(uid, token, data) {
    resetPassword.loading = true
    resetPassword.success = resetPassword.error = null

    await axios.post(`api/auth/help/password/reset/confirm/${uid}/${token}/`, data)
      .then((resp) => {
        resetPassword.loading = false
        resetPassword.error = null

        // update notify
        notify.open = true
        notify.detail = resp.data['detail']
        notify.state = "good"
    
        setTimeout(() => {
          notify.open = false
          notify.detail = notify.state = null
        }, 10000);

        // navigate to sign in page
        setTimeout(() => {
          router.push({name: 'signin'})
        }, 3000);
      })
      .catch((err) => {
        resetPassword.loading = false
        if (err.response) {
          'uid' in err.response.data ? resetPassword.error = `uid : ${err.response.data['uid'][0]}`:''
          'token' in err.response.data ? resetPassword.error = `Token expired, please request a new password reset link`:''
          'new_password1' in err.response.data ? resetPassword.error = `${err.response.data['new_password1'][0]}`:''
          'new_password2' in err.response.data ? resetPassword.error = `${err.response.data['new_password2'][0]}`:''
        }
        else resetPassword.error = "An error occured"
      })
  }


  ////////////////////////////////////////////
  // Verify email functionality
  ////////////////////////////////////////////
  const verifyEmail = reactive({loading: false, data: null, error: null})

  async function submitVerifyEmail(token) {
    verifyEmail.loading = true
    verifyEmail.data = verifyEmail.error = null

    axios.get(`api/v1/creators/verify-email/${token}`)
      .then((resp) => {
        verifyEmail.loading = false
        verifyEmail.data = resp.data['detail']
        verifyEmail.error = null

        setTimeout(() => {
          router.push({name: 'home'})
        }, 5000);
      })
      .catch((err) => {
        if (err.response.status == 400) verifyEmail.error = err.response.data['error']
        else if (err.response.status == 404) verifyEmail.error = "Not Found"
        else verifyEmail.error = "An error occured, Login to your dashboard and request new verification link"
      })
  }

  return {
    isAuthenticated, social, setSocial, signUp, submitSignUp, resetSignUp,
    signIn, submitSignIn, resetSignIn, getUser, userProfile, getUserProfile, signOut,
    submitSignOut, notify, socialData, socialGithub, socialGoogle,
    socialTwitter, getGithubUrl, getUserDataViaSocialProvider, getGoogleUrl,
    getTwitterUrl, signUpSocial, submitSignUpSocial, resetSignUpSocila, verifyEmail,
    submitVerifyEmail, forgotPassword, submitForgotPassword, resetPassword,
    submitResetPassword
  };
});
