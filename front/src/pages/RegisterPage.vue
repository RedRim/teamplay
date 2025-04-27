<template>
  <h2>Регистрация</h2>
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
    
    <div class="p-inputgroup flex-1">
      <span class="p-inputgroup-addon">
          <i class="pi pi-at"></i>
      </span>
      <InputText type="text" v-model="name" placeholder="Имя" />
    </div>
    
    <div class="p-inputgroup flex-1">
      <span class="p-inputgroup-addon">
          <i class="pi pi-at"></i>
      </span>
      <InputText type="text" v-model="last_name" placeholder="Фамилия" />
    </div>
    <Loader v-if="authStore.loader"/>
    <div v-else class="flex flex-column gap-3">
      <Button label="Зарегистрироваться" @click="signup"/>
      <span>Уже есть аккаунт? <router-link to="/login">Войти</router-link></span>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useRegisterStore } from '@/stores/register';

import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Message from 'primevue/message';

import Loader from '@/components/Loader.vue'

const authStore = useRegisterStore();

const username = ref();
const password = ref();
const name = ref();
const last_name = ref();

const signup = async () => {
    await authStore.signup({
      username: username.value,
      password: password.value,
      name: name.value,
      last_name: last_name.value,
    })
}
</script>

<style>

</style>