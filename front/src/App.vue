<template>
    <div class="menu">
        <router-link class="menu__link" to="/">Home</router-link>
        <router-link class="menu__link" to="/login" v-if="!token">Вход</router-link>
        <router-link class="menu__link" to="/posts" v-if="token">Посты</router-link>
    </div>
    <div class="app">
        <Router-View />
    </div>
</template>

<script setup>
import { computed } from 'vue';

import { useLoginStore } from '@/stores/login';

const loginStore = useLoginStore();
const token = computed(() => loginStore.userInfo.access_token)

const checkUser = () => {
    const tokens = JSON.parse(localStorage.getItem('userTokens'));
    if (tokens) {
        loginStore.userInfo.access_token = tokens.access_token;
        loginStore.userInfo.refresh_token = tokens.refresh_token;
    }
    console.log()
}

checkUser()
</script>

<style scoped>

/* * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
} */

.app {
    margin: auto;
    /* padding: 20px; */
    text-align: center;
    max-width: 700px;
}

.menu {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
    font-size: 20px;
}

.menu__link {
    color: #000;
    margin: 0 20px;
    font-family: 'Arial', sans-serif;
}
</style>