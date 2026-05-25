import { createRouter, createWebHistory } from "vue-router";
import axios from "axios";

// Seguridad de rutas
import { useAuthStore } from '@/stores/authStore';

// Rutas de las vistas
import PresentationView from "../views/Presentation/PresentationView.vue";
import AboutView from "../views/LandingPages/AboutUs/AboutView.vue";
import ContactView from "../views/LandingPages/ContactUs/ContactView.vue";
import AuthorView from "../views/LandingPages/Author/AuthorView.vue";
import SignInBasicView from "../views/LandingPages/SignIn/BasicView.vue";
import SignUp from "../views/LandingPages/Signup/SignUp.vue";
import PageHeaders from "../layouts/sections/page-sections/page-headers/HeadersView.vue";
import PageFeatures from "../layouts/sections/page-sections/features/FeaturesView.vue";
import NavigationNavbars from "../layouts/sections/navigation/navbars/NavbarsView.vue";
import NavigationNavTabs from "../layouts/sections/navigation/nav-tabs/NavTabsView.vue";
import NavigationPagination from "../layouts/sections/navigation/pagination/PaginationView.vue";
import InputAreasInputs from "../layouts/sections/input-areas/inputs/InputsView.vue";
import InputAreasForms from "../layouts/sections/input-areas/forms/FormsView.vue";
import ACAlerts from "../layouts/sections/attention-catchers/alerts/AlertsView.vue";
import ACModals from "../layouts/sections/attention-catchers/modals/ModalsView.vue";
import ACTooltipsPopovers from "../layouts/sections/attention-catchers/tooltips-popovers/TooltipsPopoversView.vue";
import ElAvatars from "../layouts/sections/elements/avatars/AvatarsView.vue";
import ElBadges from "../layouts/sections/elements/badges/BadgesView.vue";
import ElBreadcrumbs from "../layouts/sections/elements/breadcrumbs/BreadcrumbsView.vue";
import ElButtons from "../layouts/sections/elements/buttons/ButtonsView.vue";
import ElButtonGroups from "../layouts/sections/elements/button-groups/ButtonGroupsView.vue";
import ElDropdowns from "../layouts/sections/elements/dropdowns/DropdownsView.vue";
import ElProgressBars from "../layouts/sections/elements/progress-bars/ProgressBarsView.vue";
import ElToggles from "../layouts/sections/elements/toggles/TogglesView.vue";
import ElTypography from "../layouts/sections/elements/typography/TypographyView.vue";
import BasicViewVue from "../views/LandingPages/SignIn/BasicView.vue";
import DashboardLayout from "../layouts/dashboard/DashboardLayout.vue";
import Dashboard from "../views/Dashboard/Dashboard.vue";
import Draw from "../views/Dashboard/draw.vue";
import AnimacionSorteoView from "@/views/Dashboard/AnimacionSorteoView.vue";
import ProfileView from "@/views/profile/Profile.vue";

const router = createRouter({
  history: createWebHistory(/*import.meta.env.BASE_URL*/),
  routes: [
    {
      path: "/",
      name: "presentation",
      component: PresentationView,
    },
    {
      path: "/pages/landing-pages/sign-in",
      alias: ['/signin'],
      name: "signin",
      component: BasicViewVue,
    },
    {
      path: "/pages/landing-pages/sign-up",
      alias: ['/signup'],
      name: "signup",
      component: SignUp,
    },
    {
      path:"/dashboard-layout",
      alias: ['/dashboard'],
      name: "dashboardLayout",
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: "",
          name: "Dashboard",
          component: Dashboard,
        },
        {
          path: "draw",
          name: "Draws",
          component: Draw,
        },
        {
          path: "profile",
          name: "Profile",
          component: ProfileView,
          alias: ["/profile"],
          props: (route) => ({
            twitchOAuth: route.query.twitch_oauth ?? '',
          }),
        },
      ],
    },
    {
      path: "/pages/landing-pages/about-us",
      name: "about",
      component: AboutView,
    },
    {
      path: "/pages/landing-pages/contact-us",
      name: "contactus",
      component: ContactView,
    },
    {
      path: "/pages/landing-pages/author",
      name: "author",
      component: AuthorView,
    },
    {
      path: "/pages/landing-pages/basic",
      name: "signin-basic",
      component: SignInBasicView,
    },
    {
      path: "/sections/page-sections/page-headers",
      name: "page-headers",
      component: PageHeaders,
    },
    {
      path: "/sections/page-sections/features",
      name: "page-features",
      component: PageFeatures,
    },
    {
      path: "/sections/navigation/navbars",
      name: "navigation-navbars",
      component: NavigationNavbars,
    },
    {
      path: "/sections/navigation/nav-tabs",
      name: "navigation-navtabs",
      component: NavigationNavTabs,
    },
    {
      path: "/sections/navigation/pagination",
      name: "navigation-pagination",
      component: NavigationPagination,
    },
    {
      path: "/sections/input-areas/inputs",
      name: "inputareas-inputs",
      component: InputAreasInputs,
    },
    {
      path: "/sections/input-areas/forms",
      name: "inputareas-forms",
      component: InputAreasForms,
    },
    {
      path: "/sections/attention-catchers/alerts",
      name: "ac-alerts",
      component: ACAlerts,
    },
    {
      path: "/sections/attention-catchers/modals",
      name: "ac-modals",
      component: ACModals,
    },
    {
      path: "/sections/attention-catchers/tooltips-popovers",
      name: "ac-tooltips-popovers",
      component: ACTooltipsPopovers,
    },
    {
      path: "/sections/elements/avatars",
      name: "el-avatars",
      component: ElAvatars,
    },
    {
      path: "/sections/elements/badges",
      name: "el-badges",
      component: ElBadges,
    },
    {
      path: "/sections/elements/breadcrumbs",
      name: "el-breadcrumbs",
      component: ElBreadcrumbs,
    },
    {
      path: "/sections/elements/buttons",
      name: "el-buttons",
      component: ElButtons,
    },
    {
      path: "/sections/elements/button-groups",
      name: "el-button-groups",
      component: ElButtonGroups,
    },
    {
      path: "/sections/elements/dropdowns",
      name: "el-dropdowns",
      component: ElDropdowns,
    },
    {
      path: "/sections/elements/progress-bars",
      name: "el-progress-bars",
      component: ElProgressBars,
    },
    {
      path: "/sections/elements/toggles",
      name: "el-toggles",
      component: ElToggles,
    },
    {
      path: "/sections/elements/typography",
      name: "el-typography",
      component: ElTypography,
    },
    {
      path: '/overlay/:overlayToken',
      name: 'Overlay',
      component: () => import('@/views/Overlay/OverlayView.vue'),
      meta: { public: true },
    },
    {
    path: "/dashboard-layout/draw/animation",
      name: "DrawAnimation",
      component: AnimacionSorteoView,
    },
  ],
});


// Protección de rutas
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const token = authStore.loadTokenFromStorage();

  if (to.meta?.public) {
    next();
    return;
  }

  const privateRouteNames = [
    'testdashboard',
    'page-headers',
    'page-features',
    'navigation-navbars',
    'navigation-navtabs',
    'inputareas-inputs',
    'inputareas-forms',
    'ac-alerts',
    'ac-modals',
    'ac-tooltips-popovers',
    'el-avatars',
    'el-badges',
    'el-breadcrumbs',
    'el-buttons',
    'el-button-groups',
    'el-dropdowns',
    'el-progress-bars',
    'el-toggles',
    'el-typography',
    'dashboardLayout',
    'Dashboard',
    'Draws',
    'DrawAnimation',
    'Profile',
  ];

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth) || privateRouteNames.includes(to.name);

  try {
    if (requiresAuth) {
      if (!token) return next({ name: 'signin' });
      const session = await authStore.checkSession();
      if (!session) return next({ name: 'signin' });
    }

    if ((to.name === 'signin' || to.name === 'signup') && token) {
      const session = await authStore.checkSession();
      if (session) return next({ path: '/dashboard' });
    }

    return next();
  } catch (error) {
    const unauthorized = axios.isAxiosError(error) && error.response?.status === 401;
    if (unauthorized) {
      authStore.logout();
      return next({ name: 'signin' });
    }

    console.error('Error de navegación/autenticación:', error);
    if (requiresAuth) return next({ name: 'signin' });
    return next();
  }
});

export default router;
