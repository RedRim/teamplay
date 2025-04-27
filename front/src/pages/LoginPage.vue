<template>
    <h2>Вход</h2>
    <form class="flex flex-column gap-3">
      <Message v-if="authStore.error" severity="warn">{{ authStore.error }}</Message>
      <div class="p-inputgroup flex-1">
        <span class="p-inputgroup-addon">
            <i class="pi pi-user"></i>
        </span>
        <InputText type="username" v-model="username" placeholder="Логин" />
      </div>
  
      <div class="p-inputgroup flex-1">
        <span class="p-inputgroup-addon">
            <i class="pi pi-at"></i>
        </span>
        <InputText type="password" v-model="password" placeholder="Пароль" />
      </div>
      
      <Loader v-if="authStore.loader"/>
      <div v-else class="flex flex-column gap-3">
        <Button label="Войти" @click="login"/>
        <span>Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></span>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useLoginStore } from '@/stores/login';
  import { useRouter } from 'vue-router';
  
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  import Message from 'primevue/message';
  
  import Loader from '@/components/Loader.vue'
  
  const authStore = useLoginStore();
  const router = useRouter();
  
  const username = ref();
  const password = ref();
  
  const login = async () => {
    try {
        await authStore.login({
            username: username.value,
            password: password.value,
        });
        router.push('/posts');
    } catch (error) {
        console.error('Ошибка входа:', error);
    }
  }
  </script>
  
  <style>
  
  </style>