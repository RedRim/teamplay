import Main from '@/pages/Main';
import { createRouter, createWebHistory } from 'vue-router';
import PostPage from "@/pages/PostPage";
import About from "@/pages/About";
import PostIdPage from '@/pages/PostIdPage.vue';
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import { useLoginStore } from '@/stores/login';
import { _ } from 'core-js';


const routes = [
    {
        path: '/',
        component: Main,
    },
    {
        path: '/register',
        component: RegisterPage,
        meta: {
            auth: false
        }
    },
    {
        path: '/login',
        component: LoginPage,
        meta: {
            auth: false
        }
    },
    {
        path: '/posts',
        component: PostPage,
        meta: {
            auth: true
        }
    },
    {
        path: '/about',
        component: About
    },
    {
        path: '/posts/:id',
        component: PostIdPage
    },
]

const router = createRouter({
    routes,
    history: createWebHistory(process.env.BASE_URL)
})

router.beforeEach((to, from, next) => {
    const loginStore = useLoginStore();

    if (to.meta.auth && !loginStore.userInfo.access_token) {
        next('/login')
    } else {
        next();
    }
})

export default router;