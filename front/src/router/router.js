import Main from '@/pages/Main';
import { createRouter, createWebHistory } from 'vue-router';
import PostPage from "@/pages/PostPage";
import About from "@/pages/About";
import PostIdPage from '@/pages/PostIdPage.vue';
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'


const routes = [
    {
        path: '/',
        component: Main,
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

export default router;