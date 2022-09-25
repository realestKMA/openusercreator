/* eslint-disable */
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AuthView from "../views/AuthView.vue";
import DashboardView from "../views/DashboardView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/dashboard",
      name: "dashboard",
      redirect: {name: 'dashboarduser'},
      component: DashboardView,
      children: [
        {
          path: "",
          name: "dashboarduser",
          component: () =>  import("../components/AppDashboard.vue")
        },
        {
          path: "settings",
          name: "dashboardusersettings",
          component: () =>  import("../components/AppDashboardSettings.vue")
        },
        {
          path: "app",
          name: "dashboardapp",
          component: () =>  import("../components/AppDashboardApp.vue")
        },
        {
          path: "app/create",
          name: "dashboardappcreate",
          component: () =>  import("../components/AppDashboardAppCreate.vue")
        },
        {
          path: "app/settings",
          name: "dashboardappsettings",
          component: () =>  import("../components/AppDashboardAppSettings.vue")
        },
      ]
    },
    {
      path: "/auth",
      name: "auth",
      component: AuthView,
      children: [
        {
          path: "signup",
          name: "signup",
          component: () => import("../components/AppSignUp.vue")
        },
        {
          path: "signup/social",
          name: "signupsocial",
          component: () => import("../components/AppSignUpSocial.vue")
        },
        {
          path: "signin",
          name: "signin",
          component: () => import("../components/AppSignIn.vue")
        },
        {
          path: "help/forgot-password",
          name: "forgotpassword",
          component: () => import("../components/AppForgotPassword.vue")
        },
        {
          path: "help/success/reset-password",
          name: "resetpassword",
          component: () => import("../components/AppResetPassword.vue")
        },
      ]
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) return {el: to.hash,  behavior: "smooth"}
    else return { top: 0, behavior: "smooth" }
  }
});

export default router;
